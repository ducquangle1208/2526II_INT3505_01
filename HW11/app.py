import hashlib
import hmac
import json
import os
import time
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify, request


app = Flask(__name__)

STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_demo_secret")
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "github_demo_secret")
SIGNATURE_TOLERANCE_SECONDS = int(os.getenv("SIGNATURE_TOLERANCE_SECONDS", "300"))

events_store = {}
notifications_store = []


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def parse_json_payload(raw_body):
    try:
        return json.loads(raw_body.decode("utf-8"))
    except json.JSONDecodeError:
        return None


def verify_stripe_signature(raw_body, signature_header, secret):
    if not signature_header:
        return False, "Missing Stripe-Signature header"

    parts = {}
    for item in signature_header.split(","):
        if "=" in item:
            key, value = item.split("=", 1)
            parts.setdefault(key, []).append(value)

    timestamps = parts.get("t", [])
    signatures = parts.get("v1", [])
    if not timestamps or not signatures:
        return False, "Stripe-Signature must include t and v1"

    try:
        timestamp = int(timestamps[0])
    except ValueError:
        return False, "Invalid Stripe timestamp"

    if abs(time.time() - timestamp) > SIGNATURE_TOLERANCE_SECONDS:
        return False, "Stripe signature timestamp is outside tolerance"

    signed_payload = f"{timestamp}.".encode("utf-8") + raw_body
    expected = hmac.new(
        secret.encode("utf-8"),
        signed_payload,
        hashlib.sha256,
    ).hexdigest()

    if not any(hmac.compare_digest(expected, signature) for signature in signatures):
        return False, "Stripe signature mismatch"

    return True, "ok"


def verify_github_signature(raw_body, signature_header, secret):
    if not signature_header:
        return False, "Missing X-Hub-Signature-256 header"

    expected = "sha256=" + hmac.new(
        secret.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature_header):
        return False, "GitHub signature mismatch"

    return True, "ok"


def build_notification(provider, event_type, payload):
    summary = {
        "provider": provider,
        "event_type": event_type,
        "created_at": utc_now_iso(),
        "message": f"Received {provider} event: {event_type}",
    }

    if provider == "stripe":
        obj = payload.get("data", {}).get("object", {})
        summary["source_id"] = payload.get("id")
        summary["message"] = (
            f"Stripe {event_type}: object {obj.get('id', 'unknown')} "
            f"status={obj.get('status', 'n/a')}"
        )
    elif provider == "github":
        repository = payload.get("repository", {}).get("full_name", "unknown/repo")
        sender = payload.get("sender", {}).get("login", "unknown")
        summary["source_id"] = request.headers.get("X-GitHub-Delivery")
        summary["message"] = f"GitHub {event_type}: {repository} by {sender}"

    return summary


def record_event(provider, event_id, event_type, payload):
    if event_id in events_store:
        return events_store[event_id], False

    notification = build_notification(provider, event_type, payload)
    event = {
        "id": event_id,
        "provider": provider,
        "event_type": event_type,
        "received_at": utc_now_iso(),
        "notification": notification,
    }
    events_store[event_id] = event
    notifications_store.append(notification)
    return event, True


@app.get("/")
def index():
    return jsonify(
        {
            "service": "HW11 Webhook Notification API",
            "endpoints": [
                "POST /webhooks/stripe",
                "POST /webhooks/github",
                "GET /notifications",
                "GET /events",
                "GET /health",
            ],
        }
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok", "time": utc_now_iso()})


@app.post("/webhooks/stripe")
def stripe_webhook():
    raw_body = request.get_data()
    is_valid, reason = verify_stripe_signature(
        raw_body,
        request.headers.get("Stripe-Signature"),
        STRIPE_WEBHOOK_SECRET,
    )
    if not is_valid:
        return jsonify({"error": reason}), 400

    payload = parse_json_payload(raw_body)
    if payload is None:
        return jsonify({"error": "Invalid JSON payload"}), 400

    event_id = payload.get("id") or f"stripe:{uuid.uuid4()}"
    event_type = payload.get("type", "unknown")
    event, created = record_event("stripe", event_id, event_type, payload)
    return jsonify({"received": True, "created": created, "event": event}), 200


@app.post("/webhooks/github")
def github_webhook():
    raw_body = request.get_data()
    is_valid, reason = verify_github_signature(
        raw_body,
        request.headers.get("X-Hub-Signature-256"),
        GITHUB_WEBHOOK_SECRET,
    )
    if not is_valid:
        return jsonify({"error": reason}), 403

    payload = parse_json_payload(raw_body)
    if payload is None:
        return jsonify({"error": "Invalid JSON payload"}), 400

    delivery_id = request.headers.get("X-GitHub-Delivery") or f"github:{uuid.uuid4()}"
    event_type = request.headers.get("X-GitHub-Event", "unknown")
    event, created = record_event("github", delivery_id, event_type, payload)
    return jsonify({"received": True, "created": created, "event": event}), 200


@app.get("/notifications")
def list_notifications():
    return jsonify({"count": len(notifications_store), "data": notifications_store})


@app.get("/events")
def list_events():
    return jsonify({"count": len(events_store), "data": list(events_store.values())})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
