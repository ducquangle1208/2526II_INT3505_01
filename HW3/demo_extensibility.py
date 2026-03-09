import random
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

app = Flask(__name__)

STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"]
CUSTOMER_ORDERS = []
base_time = datetime.now()

for i in range(1, 101):
    CUSTOMER_ORDERS.append({
        "id": 1000 + i,
        "customer_id": random.randint(1, 20),
        "total_amount": round(random.uniform(15.0, 999.0), 2),
        "status": random.choice(STATUSES),
        "created_at": (base_time - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%dT%H:%M:%SZ")
    })

def success_response(data, meta=None):
    res = {"data": data}
    if meta:
        res["meta"] = meta
    return jsonify(res), 200

def error_response(code, message, status_code):
    return jsonify({"error": {"code": code, "message": message}}), status_code

@app.route('/api/v1/customer-orders', methods=['GET'])
def get_orders():

    # các tham số mở rộng
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    status_filter = request.args.get('status')
    sort_by = request.args.get('sort')
    fields = request.args.get('fields')

    if page < 1 or limit < 1:
        return error_response("INVALID_PAGINATION", "Page và limit phải lớn hơn 0.", 400)

    result = CUSTOMER_ORDERS

    # lọc trạng thái
    if status_filter:
        result = [o for o in result if o['status'] == status_filter]

    # sắp xếp giảm dần
    if sort_by:
        desc = sort_by.startswith('-')
        key = sort_by.lstrip('-')
        if key in result[0] if result else False:
            result = sorted(result, key=lambda x: x[key], reverse=desc)

    # phân trang
    total_items = len(result)
    start = (page - 1) * limit
    end = start + limit
    paginated_result = result[start:end]

    if fields:
        field_list = fields.split(',')
        paginated_result = [
            {k: v for k, v in item.items() if k in field_list}
            for item in paginated_result
        ]

    meta = {
        "total_items": total_items,
        "current_page": page,
        "items_per_page": limit,
        "total_pages": (total_items + limit - 1) // limit
    }

    return success_response(paginated_result, meta)

if __name__ == '__main__':
    app.run(debug=True, port=5000)