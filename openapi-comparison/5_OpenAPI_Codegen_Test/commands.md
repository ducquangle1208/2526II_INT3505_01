# Các lệnh demo với OpenAPI

## 1. Sinh Python client

Yêu cầu: đã cài `openapi-generator-cli`

```bash
openapi-generator-cli generate ^
  -i openapi-comparison/0_OpenAPI/library.openapi.yaml ^
  -g python ^
  -o openapi-comparison/5_OpenAPI_Codegen_Test/generated/python-client
```

Kết quả mong đợi:

- sinh ra model `Book`, `Member`, `Loan`
- sinh các hàm gọi API tương ứng

## 2. Sinh Flask server stub

```bash
openapi-generator-cli generate ^
  -i openapi-comparison/0_OpenAPI/library.openapi.yaml ^
  -g python-flask ^
  -o openapi-comparison/5_OpenAPI_Codegen_Test/generated/flask-server
```

Kết quả mong đợi:

- sinh route stub cho `/books`, `/members`, `/loans`
- sinh khung model/schema để implement tiếp

## 3. Sinh Postman collection

Yêu cầu: đã cài `openapi2postmanv2`

```bash
openapi2postmanv2 ^
  -s openapi-comparison/0_OpenAPI/library.openapi.yaml ^
  -o openapi-comparison/5_OpenAPI_Codegen_Test/generated/postman/library.postman.json ^
  -p
```

Kết quả mong đợi:

- import được vào Postman
- chạy thử các request theo tài liệu API

## 4. Chạy pytest với Flask demo

```bash
cd openapi-comparison/demo-flask-openapi
pytest ..\5_OpenAPI_Codegen_Test\pytest_api_test.py
```

## 5. Chạy Schemathesis từ OpenAPI

Yêu cầu: Flask app đang chạy tại `http://localhost:5000`

```bash
schemathesis run ^
  --url http://localhost:5000 ^
  openapi-comparison/0_OpenAPI/library.openapi.yaml
```

Hoặc test trực tiếp từ spec app public ra:

```bash
schemathesis run http://localhost:5000/openapi
```

## 6. Các package thường dùng

```bash
pip install openapi-generator-cli
pip install pytest requests schemathesis
npm install -g openapi2postmanv2
```
