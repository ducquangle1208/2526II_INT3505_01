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


@app.route('/api/v3/project-tasks/<int:task_id>/status', methods=['PUT'])
def v3_update_task_status(task_id):
    payload = request.get_json(silent=True)
    task = next((t for t in PROJECT_TASKS if t['id'] == task_id), None)

    if not task:
        return format_response(
            error={
                "code": "TASK_NOT_FOUND",
                "message": f"Không tìm thấy task với ID {task_id}. Vui lòng tải lại trang để lấy danh sách ID mới nhất."
            },
            status_code=404
        )

    task['status'] = payload.get('status', task['status'])
    return format_response(data=task, status_code=200)

if __name__ == "__main__":
    app.run(debug=True)