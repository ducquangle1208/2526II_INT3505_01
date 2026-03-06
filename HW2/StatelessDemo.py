from flask import Flask, request, jsonify
from datetime import datetime, timedelta, timezone
import jwt

app = Flask(__name__)
SECRET_KEY = "fhaosifj;kladmsgfhiua;jokmdsojfdlmksa"

users = {"quang": "123456"}


@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    if not username or users.get(username) != password:
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "user": username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})


@app.route("/profile")
def profile():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header missing or invalid"}), 401

    token = auth_header.split(" ")[1]

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"user": data["user"], "status": "Authenticated"})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


if __name__ == "__main__":
    app.run(debug=True)