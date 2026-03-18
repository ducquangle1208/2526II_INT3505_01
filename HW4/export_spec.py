import yaml
from app import app

def export_openapi_yaml():
    print("⏳ Đang trích xuất cấu hình OpenAPI...")

    with app.test_client() as client:
        response = client.get('/openapi/openapi.json')

        if response.status_code == 200:
            spec_dict = response.get_json()

            try:
                with open('openapi.yaml', 'w', encoding='utf-8') as f:
                    yaml.dump(
                        spec_dict,
                        f,
                        allow_unicode=True,
                        sort_keys=False,
                        default_flow_style=False
                    )
                print("Thành công! File 'openapi.yaml' đã được tạo mới/cập nhật.")
            except Exception as e:
                print(f"Có lỗi trong quá trình ghi file: {e}")
        else:
            print(f"Thất bại! Server trả về mã lỗi HTTP: {response.status_code}")
            print(f"Chi tiết lỗi: {response.text}")

if __name__ == '__main__':
    export_openapi_yaml()