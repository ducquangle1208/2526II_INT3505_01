# Demo sinh code và test với OpenAPI

Thư mục này minh họa cách dùng file OpenAPI để:

- sinh mã client hoặc server stub
- sinh Postman collection
- chạy test tự động dựa trên schema

File đầu vào chính:

- `../0_OpenAPI/library.openapi.yaml`

## Nội dung thư mục

- `commands.md`: các lệnh mẫu để sinh code và test
- `pytest_api_test.py`: test API cơ bản cho demo Flask
- `schemathesis.md`: cách chạy test sinh tự động từ OpenAPI

## Cách demo nhanh

1. Chạy ứng dụng Flask trong `../demo-flask-openapi`.
2. Dùng các lệnh trong `commands.md` để sinh client, server stub hoặc Postman collection.
3. Chạy `pytest` hoặc `schemathesis` để kiểm thử API theo đặc tả OpenAPI.

## Ý nghĩa

Điểm chính cần nhấn mạnh khi demo:

- OpenAPI không chỉ là tài liệu.
- Từ cùng một file đặc tả có thể sinh nhiều đầu ra khác nhau.
- Có thể dùng đặc tả để kiểm thử tự động và phát hiện lệch giữa tài liệu và implementation.
