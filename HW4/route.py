from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)

openapi_template = {
    "openapi": "3.0.0",
    "info": {
        "title": "Books Management API",
        "description": "API quản lý sách cơ bản viết bằng Flask",
        "version": "1.0.0"
    },
    "servers": [
        {
            "url": "http://localhost:5000",
            "description": "Local server"
        }
    ]
}

swagger = Swagger(app, template=openapi_template)


books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"}
]

@app.route('/books', methods=['GET'])
def get_books():
    """
    Lấy danh sách tất cả các sách
    ---
    responses:
      200:
        description: Một danh sách chứa các cuốn sách
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              author:
                type: string
    """
    return jsonify(books)


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Lấy thông tin một cuốn sách theo ID
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID của cuốn sách cần tìm
    responses:
      200:
        description: Thông tin cuốn sách
      404:
        description: Không tìm thấy sách
    """
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"message": "Book not found"}), 404


@app.route('/books', methods=['POST'])
def create_book():
    """
    Thêm một cuốn sách mới
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Design Patterns"
            author:
              type: string
              example: "Erich Gamma"
    responses:
      201:
        description: Sách đã được tạo thành công
    """
    data = request.json
    new_book = {
        "id": books[-1]["id"] + 1 if books else 1,
        "title": data.get("title"),
        "author": data.get("author")
    }
    books.append(new_book)
    return jsonify(new_book), 201


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Cập nhật thông tin một cuốn sách
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID của cuốn sách cần cập nhật
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
    responses:
      200:
        description: Sách đã được cập nhật
      404:
        description: Không tìm thấy sách
    """
    data = request.json
    book = next((b for b in books if b["id"] == book_id), None)

    if not book:
        return jsonify({"message": "Book not found"}), 404

    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])

    return jsonify(book)


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Xóa một cuốn sách
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
        description: ID của cuốn sách cần xóa
    responses:
      200:
        description: Đã xóa sách thành công
    """
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted"})


if __name__ == '__main__':
    app.run(debug=True)