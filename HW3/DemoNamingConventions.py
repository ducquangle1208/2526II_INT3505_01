from flask import Flask, request, jsonify

app = Flask(__name__)

PROJECT_TASKS = [
    {"id": 1, "title": "Thiết kế Database", "status": "done"},
    {"id": 2, "title": "Viết API Authentication", "status": "in_progress"},
    {"id": 3, "title": "Viết Unit Test", "status": "todo"}
]

@app.route('/api/v1/project-tasks', methods=['GET'])
def v1_get_tasks():
    return jsonify(PROJECT_TASKS), 200

if __name__ == "__main__":
    app.run(debug=True)