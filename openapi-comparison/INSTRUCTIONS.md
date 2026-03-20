# Hướng dẫn thực hiện

## 1. Mục đích

Tài liệu này được tạo ra để giúp người xem hiểu rõ:

- OpenAPI là gì và vì sao nó phổ biến trong thiết kế REST API.
- Các format/công cụ khác có chức năng tương tự OpenAPI gồm API Blueprint, RAML, TypeSpec và mô hình mô tả typed API.
- Điểm giống, điểm khác nhau và tính ứng dụng thực tế của từng lựa chọn.

Mục tiêu cuối cùng không chỉ là liệt kê định dạng, mà là so sánh trên cùng một bài toán API cụ thể để rút ra nhận xét có cơ sở.

## 2. Yêu cầu

Người thực hiện cần đảm bảo các nội dung sau:

- Sử dụng cùng một bài toán API để mô tả bằng nhiều format khác nhau.
- Chọn một domain đơn giản, dễ hiểu và có đủ endpoint để so sánh.
- Mỗi format phải mô tả cùng một tập tài nguyên và thao tác chính.
- Có ít nhất một bản demo thực thi được để cho thấy từ tài liệu API có thể đi đến phần implement.
- Tổng hợp nhận xét cuối cùng theo tiêu chí rõ ràng, không chỉ mô tả cảm tính.

Trong thư mục này, bài toán được chọn là ứng dụng quản lý thư viện với các thực thể chính:

- `books`
- `members`
- `loans`

## 3. Phương pháp so sánh

Để việc so sánh công bằng và dễ theo dõi, cần áp dụng cùng một cách tiếp cận cho tất cả format.

### 3.1. Thống nhất phạm vi API

Tất cả các format đều mô tả cùng một tập endpoint:

- `GET /books`
- `POST /books`
- `GET /books/{bookId}`
- `GET /members`
- `POST /members`
- `POST /loans`
- `PATCH /loans/{loanId}/return`

### 3.2. Thống nhất mô hình dữ liệu

Tất cả các định dạng đều mô tả cùng các model chính:

- `Book`
- `Member`
- `Loan`
- request model cho thao tác tạo mới
- response lỗi có trường `message`

### 3.3. Tiêu chí so sánh

Khi đánh giá từng format, nên dựa trên các tiêu chí sau:

- Độ dễ đọc đối với con người.
- Độ rõ ràng khi mô tả endpoint, schema, request, response.
- Khả năng tái sử dụng và tổ chức schema.
- Mức độ hỗ trợ tool ecosystem.
- Khả năng sinh code, sinh tài liệu, validate.
- Mức độ phù hợp với quy mô dự án nhỏ và lớn.
- Độ gần gũi với quy trình implement thực tế.

### 3.4. Cách rút ra kết luận

Không nên kết luận theo kiểu "format nào tốt nhất trong mọi trường hợp". Thay vào đó, cần trả lời:

- Format nào dễ học và dễ đọc nhất.
- Format nào mạnh về mô tả API một cách chuẩn hóa.
- Format nào hợp với workflow design-first.
- Format nào hợp với hệ sinh thái typed hoặc code-first.
- Khi nào OpenAPI là lựa chọn hợp lý nhất.

## 4. Dàn ý chung cho báo cáo hoặc bài thuyết trình

Có thể trình bày theo bố cục sau:

### Phần 1. Giới thiệu vấn đề

- API specification là gì.
- Vì sao cần đặc tả API trước hoặc song song với lúc lập trình.
- Lý do chọn OpenAPI làm mốc so sánh.

### Phần 2. Mô tả bài toán chung

- Giới thiệu ứng dụng quản lý thư viện.
- Liệt kê các tài nguyên và endpoint.
- Mô tả nhanh luồng nghiệp vụ mượn/trả sách.

### Phần 3. Trình bày từng format

Với mỗi format, nên trình bày:

- Khái niệm ngắn gọn.
- Cú pháp cơ bản.
- Cách mô tả endpoint và schema.
- Ưu điểm.
- Hạn chế.

Thứ tự gợi ý:

1. OpenAPI
2. API Blueprint
3. RAML
4. TypeSpec
5. TypeAPI hoặc typed API DSL

### Phần 4. So sánh tổng hợp

Nên có bảng hoặc phần tổng hợp theo các tiêu chí:

- dễ đọc
- dễ viết
- dễ maintain
- tooling
- validate
- code generation
- mức độ phổ biến
- phù hợp bối cảnh sử dụng

### Phần 5. Demo thực tế

- Giới thiệu demo Flask sử dụng OpenAPI.
- Chỉ ra mối liên hệ giữa file đặc tả OpenAPI và các endpoint đã implement.
- Nếu có thể, mở Swagger Docs để minh họa giá trị của OpenAPI trong thực tế.

### Phần 6. Kết luận

- Tổng kết điểm mạnh của OpenAPI.
- Nêu tính bổ trợ của các format khác.
- Đề xuất format phù hợp theo từng mục tiêu học tập, tài liệu hóa hoặc phát triển hệ thống.

## 5. Đầu ra mong đợi

Sau khi hoàn thành, người xem cần nắm được:

- Bản chất của API specification.
- Cách cùng một API có thể được mô tả bằng nhiều format.
- Lý do OpenAPI thường được chọn trong hệ sinh thái web hiện nay.
- Sự khác biệt giữa các lựa chọn theo góc nhìn tài liệu, tooling và implement.

## 6. Ghi chú sử dụng thư mục

- `0_OpenAPI`: đặc tả chuẩn OpenAPI 3.1
- `1_APIBlueprint`: phiên bản API Blueprint của cùng API
- `2_RAML`: phiên bản RAML của cùng API
- `3_TypeSpec`: phiên bản TypeSpec của cùng API
- `4_TypeAPI`: phiên bản typed DSL để đối chiếu
- `demo-flask-openapi`: ứng dụng Flask nhỏ để demo cách đưa OpenAPI vào implement
