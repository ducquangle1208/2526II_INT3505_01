import time
import uuid
from flask import request, jsonify, g
from flask_openapi3 import Info, OpenAPI, Tag
from pydantic import BaseModel
from typing import List
from prometheus_flask_exporter import PrometheusMetrics
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('hw10-flask')

# Thông tin API cho Swagger
info = Info(title="HW10 Product API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Prometheus Metrics
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')

# Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Tags cho Swagger
product_tag = Tag(name="Products", description="Quản lý danh sách sản phẩm")

# Pydantic Models cho Swagger & Validation
class Product(BaseModel):
    id: int
    name: str

class ProductResponse(BaseModel):
    success: bool
    data: List[Product]

@app.before_request
def before_request_logging():
    g.start_time = time.time()
    g.trace_id = request.headers.get('X-Trace-Id', str(uuid.uuid4()))
    logger.info(f"[TraceID: {g.trace_id}] Bắt đầu xử lý {request.method} {request.path}")

@app.after_request
def after_request_logging(response):
    duration = time.time() - getattr(g, 'start_time', time.time())
    logger.info(f"[TraceID: {getattr(g, 'trace_id', 'N/A')}] Hoàn thành {request.method} {request.path} - Status: {response.status_code} - Thời gian: {duration:.4f}s")
    
    response.headers['X-Trace-Id'] = getattr(g, 'trace_id', 'N/A')
    return response

@app.get('/products', tags=[product_tag], responses={200: ProductResponse})
@limiter.limit("100 per 15 minute")
@metrics.counter('get_products_counter', 'Số lượng gọi GET /products') 
def get_products():
    """
    Lấy danh sách sản phẩm
    Endpoint này trả về danh sách các sản phẩm mẫu trong hệ thống.
    """
    logger.info(f"[TraceID: {g.trace_id}] Đang truy vấn cơ sở dữ liệu lấy danh sách products...")
    
    products = [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Mouse"}]
    
    return jsonify({"success": True, "data": products}), 200

@app.errorhandler(429)
def ratelimit_handler(e):
    logger.error(f"[TraceID: {getattr(g, 'trace_id', 'N/A')}] Bị chặn do Rate Limit: {e.description}")
    return jsonify(error="Too many requests", description=str(e.description)), 429

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"[TraceID: {getattr(g, 'trace_id', 'N/A')}] Lỗi hệ thống: {str(e)}", exc_info=True)
    return jsonify(error="Internal Server Error"), 500

if __name__ == '__main__':
    logger.info("Khởi động server Flask tại port 8080")
    # Swagger UI sẽ khả dụng tại http://localhost:8080/openapi/swagger
    app.run(host="0.0.0.0", port=8080, debug=True)
