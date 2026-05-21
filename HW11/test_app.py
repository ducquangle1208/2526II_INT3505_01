import hashlib
import hmac
import json
import time
import unittest

import app as webhook_app


def stripe_signature(body, secret="whsec_demo_secret"):
    timestamp = int(time.time())
    signed_payload = f"{timestamp}.".encode("utf-8") + body
    digest = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


def github_signature(body, secret="github_demo_secret"):
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


class WebhookAppTestCase(unittest.TestCase):
    def setUp(self):
        webhook_app.events_store.clear()
        webhook_app.notifications_store.clear()
        self.client = webhook_app.app.test_client()

    def test_stripe_webhook_creates_notification(self):
        body = json.dumps(
            {
                "id": "evt_test_1",
                "type": "payment_intent.succeeded",
                "data": {"object": {"id": "pi_test_1", "status": "succeeded"}},
            }
        ).encode("utf-8")

        response = self.client.post(
            "/webhooks/stripe",
            data=body,
            headers={"Stripe-Signature": stripe_signature(body)},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["created"])
        self.assertEqual(webhook_app.notifications_store[0]["provider"], "stripe")

    def test_github_webhook_rejects_bad_signature(self):
        body = b'{"repository":{"full_name":"demo/repo"},"sender":{"login":"alice"}}'

        response = self.client.post(
            "/webhooks/github",
            data=body,
            headers={
                "X-GitHub-Event": "push",
                "X-GitHub-Delivery": "delivery-1",
                "X-Hub-Signature-256": "sha256=bad",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)

    def test_github_webhook_is_idempotent_by_delivery_id(self):
        body = b'{"repository":{"full_name":"demo/repo"},"sender":{"login":"alice"}}'
        headers = {
            "X-GitHub-Event": "push",
            "X-GitHub-Delivery": "delivery-1",
            "X-Hub-Signature-256": github_signature(body),
        }

        first = self.client.post("/webhooks/github", data=body, headers=headers)
        second = self.client.post("/webhooks/github", data=body, headers=headers)

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        self.assertTrue(first.json["created"])
        self.assertFalse(second.json["created"])
        self.assertEqual(len(webhook_app.notifications_store), 1)


if __name__ == "__main__":
    unittest.main()
