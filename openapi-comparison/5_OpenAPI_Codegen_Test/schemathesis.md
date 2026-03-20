# Demo test tự động với Schemathesis

Schemathesis là công cụ đọc file OpenAPI và tự sinh test HTTP để kiểm tra API có tuân thủ đặc tả hay không.

## Bước 1. Cài đặt

```bash
pip install schemathesis
```

## Bước 2. Chạy Flask demo

```bash
cd openapi-comparison/demo-flask-openapi
python app.py
```

## Bước 3. Chạy test từ file OpenAPI

```bash
schemathesis run ^
  --url http://localhost:5000 ^
  openapi-comparison/0_OpenAPI/library.openapi.yaml
```

## Bước 4. Hoặc chạy từ endpoint OpenAPI của app

```bash
schemathesis run http://localhost:5000/openapi
```

## Giá trị trình bày

Khi demo, có thể giải thích ngắn gọn:

- Schemathesis đọc schema request/response từ OpenAPI.
- Tự sinh request hợp lệ và cả trường hợp biên.
- Kiểm tra mã trạng thái và cấu trúc response.
- Giúp phát hiện sự sai lệch giữa tài liệu và code thật.
