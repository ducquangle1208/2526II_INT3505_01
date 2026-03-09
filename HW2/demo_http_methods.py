from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "An"},
    {"id": 2, "name": "Binh"}
]

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    for user in users:
        if user["id"] == id:
            return jsonify(user)
    return {"error": "User not found"}, 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = {
        "id": len(users) + 1,
        "name": data["name"]
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    for user in users:
        if user["id"] == id:
            user["name"] = data["name"]
            return jsonify(user)
    return {"error": "User not found"}, 404

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    for user in users:
        if user["id"] == id:
            users.remove(user)
            return {"message": "User deleted"}
    return {"error": "User not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)