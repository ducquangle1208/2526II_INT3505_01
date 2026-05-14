from flask import Blueprint, jsonify

v2_bp = Blueprint('v2', __name__)

@v2_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_v2(user_id):
    # Giả lập data cấu trúc mới
    data = {
        "id": user_id,
        "first_name": "A",
        "last_name": "Nguyen Van",
        "email": "a.nguyen@example.com"
    }
    return jsonify(data)