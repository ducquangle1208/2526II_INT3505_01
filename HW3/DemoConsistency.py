from flask import Flask, request, jsonify

app = Flask(__name__)

PROJECT_TASKS = [
    {"id": 1, "title": "Thiết kế Database", "status": "done"},
    {"id": 2, "title": "Viết API Authentication", "status": "in_progress"},
    {"id": 3, "title": "Viết Unit Test", "status": "todo"}
]


def format_response(data=None, error=None, status_code=200):
    if error:
        return jsonify({"error": error}), status_code
    return jsonify({"data": data}), status_code


@app.route('/api/v2/project-tasks', methods=['POST'])
def v2_create_task():
    payload = request.get_json(silent=True)
    if not payload or 'title' not in payload:
        return format_response(
            error={"code": "BAD_REQUEST", "message": "Thiếu trường 'title' bắt buộc."},
            status_code=400
        )

    new_task = {"id": len(PROJECT_TASKS) + 1, "title": payload['title'], "status": "todo"}
    PROJECT_TASKS.append(new_task)

    return format_response(data=new_task, status_code=201)

if __name__ == "__main__":
    app.run(debug=True)