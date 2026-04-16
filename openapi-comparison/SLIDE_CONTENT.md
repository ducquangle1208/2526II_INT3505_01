# Nội dung slide trình bày

## Slide 1. Tiêu đề

**So sánh OpenAPI với các format/công cụ mô tả API tương tự**

Nội dung trình bày:

- Giới thiệu chủ đề: đặc tả API và vai trò trong phát triển phần mềm.
- Phạm vi so sánh: OpenAPI, API Blueprint, RAML, TypeSpec và typed API DSL.
- Bài toán minh họa: ứng dụng quản lý thư viện.

## Slide 2. API specification là gì

Nội dung trình bày:

- API specification là tài liệu mô tả cách client và server giao tiếp với nhau.
- Nó thường mô tả endpoint, method, tham số, request body, response, status code và schema dữ liệu.
- API specification giúp giảm hiểu nhầm giữa người thiết kế, người lập trình và người kiểm thử.

Ý chính cần nhấn mạnh:

- Không chỉ là tài liệu để đọc.
- Có thể dùng cho code generation, documentation và testing.

## Slide 3. Vì sao cần đặc tả API

Nội dung trình bày:

- Giúp chuẩn hóa giao tiếp giữa frontend, backend, mobile và QA.
- Hỗ trợ quy trình design-first thay vì chỉ code-first.
- Cho phép sinh tài liệu tự động.
- Có thể sinh client SDK, server stub và test từ cùng một nguồn.

Ví dụ thực tế:

- Frontend biết chính xác request/response cần dùng.
- QA có thể viết test dựa trên schema.
- Backend có thể dùng đặc tả làm hợp đồng kỹ thuật.

## Slide 4. Vì sao chọn OpenAPI làm mốc so sánh

Nội dung trình bày:

- OpenAPI là chuẩn phổ biến nhất hiện nay cho REST API.
- Hệ sinh thái tooling rất mạnh.
- Được hỗ trợ tốt bởi Swagger UI, OpenAPI Generator, Postman, Schemathesis và nhiều framework backend.
- Dễ áp dụng trong cả tài liệu hóa lẫn triển khai thực tế.

Kết luận ngắn:

- OpenAPI là mốc so sánh hợp lý vì vừa phổ biến vừa có ứng dụng thực tế cao.

## Slide 5. Bài toán dùng để so sánh

**Ứng dụng quản lý thư viện**

Nội dung trình bày:

- Quản lý sách
- Quản lý độc giả
- Quản lý phiếu mượn và trả sách

Các thực thể chính:

- `Book`
- `Member`
- `Loan`

Lý do chọn bài toán này:

- Đủ đơn giản để dễ theo dõi
- Đủ nhiều endpoint để so sánh cách mô tả API
- Có quan hệ nghiệp vụ rõ ràng giữa các đối tượng

## Slide 6. Phạm vi API được mô tả

Các endpoint chính:

- `GET /books`
- `POST /books`
- `GET /books/{bookId}`
- `GET /members`
- `POST /members`
- `POST /loans`
- `PATCH /loans/{loanId}/return`

Ý nghĩa:

- Bao phủ thao tác đọc danh sách, tạo mới, xem chi tiết và cập nhật trạng thái.
- Đủ để kiểm tra khả năng mô tả schema, path parameter, request body và response của từng format.

## Slide 7. Tiêu chí so sánh

Nội dung trình bày:

- Độ dễ đọc
- Độ dễ viết
- Độ rõ ràng khi mô tả request/response
- Khả năng tổ chức schema
- Tooling và hệ sinh thái hỗ trợ
- Khả năng sinh code
- Khả năng sinh tài liệu
- Khả năng kiểm thử
- Mức độ phù hợp với dự án thực tế

Lưu ý:

- Không đặt mục tiêu tìm ra một format "tốt nhất tuyệt đối".
- Mục tiêu là xem format nào phù hợp với nhu cầu nào.

## Slide 8. OpenAPI là gì

Nội dung trình bày:

- OpenAPI là chuẩn mô tả REST API theo cấu trúc có tổ chức.
- Thường viết bằng YAML hoặc JSON.
- Mô tả được endpoint, schema, authentication, request body, response, tags, examples.

Điểm mạnh:

- Chuẩn hóa cao
- Phổ biến
- Dễ tích hợp với nhiều công cụ

Tài liệu trong bài:

- `0_OpenAPI/library.openapi.yaml`

## Slide 9. OpenAPI trong bài toán thư viện

Nội dung trình bày:

- Mô tả đầy đủ các endpoint của ứng dụng quản lý thư viện.
- Định nghĩa rõ `Book`, `Member`, `Loan`, request model và error response.
- Có thể dùng trực tiếp làm đầu vào cho code generation hoặc testing.

Điểm cần nhấn mạnh:

- Đây là format hoàn chỉnh và thực dụng nhất trong bộ ví dụ.

## Slide 10. API Blueprint là gì

Nội dung trình bày:

- API Blueprint là ngôn ngữ mô tả API thiên về tính dễ đọc cho con người.
- Có cú pháp gần với Markdown.
- Phù hợp khi ưu tiên trình bày tài liệu dễ tiếp cận.

Ưu điểm:

- Dễ đọc
- Dễ viết ở mức cơ bản
- Phù hợp cho tài liệu trình bày

Hạn chế:

- Không mạnh bằng OpenAPI về ecosystem và code generation

Tài liệu trong bài:

- `1_APIBlueprint/library.apib`

## Slide 11. RAML là gì

Nội dung trình bày:

- RAML là một ngôn ngữ mô tả REST API theo hướng có cấu trúc, viết bằng YAML.
- Có khả năng tổ chức tài nguyên và kiểu dữ liệu khá tốt.
- Từng được dùng nhiều trong các hệ sinh thái API design-first.

Ưu điểm:

- Cấu trúc rõ ràng
- Tách loại dữ liệu và resource hợp lý

Hạn chế:

- Độ phổ biến hiện tại thấp hơn OpenAPI
- Tooling thực tế không mạnh bằng OpenAPI

Tài liệu trong bài:

- `2_RAML/library.raml`

## Slide 12. TypeSpec là gì

Nội dung trình bày:

- TypeSpec là công cụ mô tả API bằng ngôn ngữ thiên về type system.
- Gần với cách suy nghĩ của lập trình viên hơn so với YAML thuần.
- Có thể compile sang OpenAPI.

Ưu điểm:

- Phù hợp với hệ sinh thái typed
- Khá mạnh khi muốn mô hình hóa schema phức tạp

Hạn chế:

- Phải học thêm cú pháp riêng
- Thường cần bước compile trước khi dùng với hệ sinh thái OpenAPI

Tài liệu trong bài:

- `3_TypeSpec/main.tsp`

## Slide 13. Typed API DSL là gì

Nội dung trình bày:

- Đây là cách mô tả API theo kiểu DSL gắn với type system, gần phong cách TypeScript.
- Không phải một chuẩn phổ biến như OpenAPI hay RAML.
- Chủ yếu dùng để minh họa tư duy "mô tả API bằng type".

Ý nghĩa trong bài:

- Giúp đối chiếu giữa chuẩn tài liệu hóa và cách mô tả gắn với code/type.

Tài liệu trong bài:

- `4_TypeAPI/library.typeapi.ts`

## Slide 14. So sánh nhanh 5 lựa chọn

Nội dung trình bày:

- OpenAPI: mạnh nhất về chuẩn hóa, tooling, codegen, testgen
- API Blueprint: dễ đọc, hợp tài liệu trình bày
- RAML: có cấu trúc rõ, nhưng ít phổ biến hơn
- TypeSpec: mạnh khi đi theo typed design, có thể sinh OpenAPI
- Typed API DSL: linh hoạt theo code, nhưng phụ thuộc công cụ riêng

Kết luận ngắn:

- Nếu cần tính thực dụng và hệ sinh thái mạnh, OpenAPI thường là lựa chọn tốt nhất.

## Slide 15. Bảng so sánh tổng hợp

Có thể trình bày dạng bảng theo các cột:

- Format
- Dễ đọc
- Dễ viết
- Tooling
- Code generation
- Test generation
- Độ phổ biến
- Phù hợp sử dụng

Nhận xét mẫu:

- OpenAPI dẫn đầu về ứng dụng thực tế.
- API Blueprint nổi bật ở khả năng trình bày dễ hiểu.
- TypeSpec phù hợp khi muốn thiết kế API bằng ngôn ngữ typed.

## Slide 16. Demo thực tế với Flask OpenAPI

Nội dung trình bày:

- Trong thư mục `demo-flask-openapi`, ứng dụng Flask được xây dựng theo cùng bài toán thư viện.
- Ứng dụng dùng `flask-openapi3`.
- Các route trong code bám theo tài liệu OpenAPI.

Điểm cần nói:

- Đặc tả API không chỉ để viết báo cáo.
- Nó có thể đi thẳng vào implementation thực tế.

## Slide 17. Demo sinh code từ OpenAPI

Nội dung trình bày:

- Dùng file `0_OpenAPI/library.openapi.yaml` làm đầu vào.
- Có thể sinh Python client bằng `openapi-generator-cli`.
- Có thể sinh Flask server stub.
- Có thể sinh Postman collection.

Thư mục minh họa:

- `5_OpenAPI_Codegen_Test`

Điểm cần nhấn mạnh:

- Một file đặc tả có thể tái sử dụng cho nhiều mục đích khác nhau.

## Slide 18. Demo kiểm thử từ OpenAPI

Nội dung trình bày:

- Có thể viết test thường bằng `pytest` dựa trên API đã mô tả.
- Có thể dùng `Schemathesis` để sinh test tự động từ OpenAPI.
- Việc này giúp kiểm tra code thật có đang tuân thủ tài liệu hay không.

Giá trị:

- Phát hiện lệch giữa implementation và schema
- Tăng độ tin cậy khi tích hợp frontend/backend

## Slide 19. Ý nghĩa của phần demo

Nội dung trình bày:

- OpenAPI không chỉ là tài liệu tĩnh.
- Nó là nguồn trung tâm cho tài liệu, codegen và test.
- Đây là điểm khiến OpenAPI mạnh hơn nhiều lựa chọn khác trong thực tế.

Thông điệp chính:

- Giá trị lớn nhất của OpenAPI nằm ở hệ sinh thái đi kèm, không chỉ ở cú pháp.
