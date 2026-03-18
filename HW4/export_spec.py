import yaml
from route import app

def export_yaml():
    with app.test_client() as client:
        response = client.get('/apispec_1.json')

        if response.status_code == 200:
            spec_dict = response.get_json()

            with open('openapi.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(
                    spec_dict,
                    f,
                    allow_unicode=True,
                    sort_keys=False,
                    default_flow_style=False
                )
            print("Đã tự động tạo file 'openapi.yaml' thành công!")
        else:
            print("Không lấy được dữ liệu Swagger.")

if __name__ == '__main__':
    export_yaml()