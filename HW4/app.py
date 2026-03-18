from flask_openapi3 import OpenAPI, Info, Tag, Server
from pydantic import BaseModel, Field, RootModel, ConfigDict
from typing import List

#Metadata trong SwaggerUI
info = Info(
    title="Books Management API",
    description="API quản lý sách sử dụng Flask-OpenAPI3 và Pydantic",
    version="1.0.0"
)
servers = [Server(url="http://localhost:5000", description="Local Server")]

#Dùng OpenAPI() thay Flask() -> tự động sinh spec
app = OpenAPI(__name__, info=info, servers=servers)
book_tag = Tag(name="Books", description="Các thao tác quản lý sách")

#Định nghĩa Schema bằng Pydantic
#Path param
class BookPath(BaseModel):
    book_id: int = Field(..., description="ID của cuốn sách")

#RequestBody
class BookInput(BaseModel):
    title: str = Field(..., description="Tên cuốn sách")
    author: str = Field(..., description="Tên tác giả")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Clean Architecture",
                "author": "Robert C. Martin"
            }
        }
    )

#Response Model
class Book(BaseModel):
    id: int
    title: str
    author: str

#Message
class MessageResponse(BaseModel):
    message: str

#Danh sách book
class BookList(RootModel):
    root: List[Book]

books_db = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"}
]

@app.get('/books', tags=[book_tag], summary="Lấy danh sách tất cả các sách", responses={"200": BookList})
def get_books():
    return books_db

@app.get('/books/<int:book_id>', tags=[book_tag], summary="Lấy thông tin sách theo ID", responses={"200": Book, "404": MessageResponse})
def get_book(path: BookPath):
    book = next((b for b in books_db if b["id"] == path.book_id), None)
    if book:
        return book
    return {"message": "Book not found"}, 404

@app.post('/books', tags=[book_tag], summary="Thêm sách mới", responses={"201": Book})
def create_book(body: BookInput):
    new_book = {
        "id": books_db[-1]["id"] + 1 if books_db else 1,
        "title": body.title,
        "author": body.author
    }
    books_db.append(new_book)
    return new_book, 201

@app.put('/books/<int:book_id>', tags=[book_tag], summary="Cập nhật thông tin sách", responses={"200": Book, "404": MessageResponse})
def update_book(path: BookPath, body: BookInput):
    book = next((b for b in books_db if b["id"] == path.book_id), None)
    if not book:
        return {"message": "Book not found"}, 404

    book["title"] = body.title
    book["author"] = body.author
    return book

@app.delete('/books/<int:book_id>', tags=[book_tag], summary="Xóa sách", responses={"200": MessageResponse, "404": MessageResponse})
def delete_book(path: BookPath):
    global books_db
    book = next((b for b in books_db if b["id"] == path.book_id), None)
    if not book:
        return {"message": "Book not found"}, 404

    books_db = [b for b in books_db if b["id"] != path.book_id]
    return {"message": "Book deleted"}

if __name__ == '__main__':
    app.run(debug=True)