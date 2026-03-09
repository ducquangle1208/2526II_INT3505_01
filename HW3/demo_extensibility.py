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


@app.route('/api/v4/project-tasks', methods=['GET'])
def v4_get_tasks_extensible():

    status_filter = request.args.get('status')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    filtered = [t for t in PROJECT_TASKS if t['status'] == status_filter] if status_filter else PROJECT_TASKS

    start_idx = (page - 1) * limit
    paginated_tasks = filtered[start_idx: start_idx + limit]

    response = {
        "data": paginated_tasks,
        "meta": {
            "total_items": len(filtered),
            "current_page": page,
            "items_per_page": limit,
            "has_next": (start_idx + limit) < len(filtered)
        }
    }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True)