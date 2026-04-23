from typing import List, Optional

from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag
from pydantic import BaseModel, ConfigDict, Field, RootModel


info = Info(
    title="Library Management API",
    version="1.0.0",
    description="Demo 5 endpoint API quan ly thu vien bang Flask",
)

app = OpenAPI(__name__, info=info)
CORS(app)

library_tag = Tag(name="Library", description="Cac endpoint quan ly sach")


class BookPath(BaseModel):
    book_id: int = Field(..., description="ID cua sach")


class BookInput(BaseModel):
    title: str = Field(..., description="Ten sach")
    author: str = Field(..., description="Tac gia")
    published_year: int = Field(..., ge=0, description="Nam xuat ban")
    genre: Optional[str] = Field(default="", description="The loai")
    available: bool = Field(default=True, description="Trang thai san sang")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "published_year": 2008,
                "genre": "Programming",
                "available": True,
            }
        }
    )


class Book(BookInput):
    id: int


class MessageResponse(BaseModel):
    message: str


class DeleteResponse(MessageResponse):
    id: int


class BookList(RootModel):
    root: List[Book]


books_db = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "published_year": 2008,
        "genre": "Programming",
        "available": True,
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt",
        "published_year": 1999,
        "genre": "Software Development",
        "available": True,
    },
]


@app.get("/books", tags=[library_tag], summary="Lay danh sach sach", responses={"200": BookList})
def get_books():
    return books_db


@app.get(
    "/books/<int:book_id>",
    tags=[library_tag],
    summary="Lay chi tiet sach theo ID",
    responses={"200": Book, "404": MessageResponse},
)
def get_book(path: BookPath):
    book = next((item for item in books_db if item["id"] == path.book_id), None)
    if not book:
        return {"message": "Book not found"}, 404
    return book


@app.post("/books", tags=[library_tag], summary="Them sach moi", responses={"201": Book})
def create_book(body: BookInput):
    new_book = {
        "id": books_db[-1]["id"] + 1 if books_db else 1,
        "title": body.title,
        "author": body.author,
        "published_year": body.published_year,
        "genre": body.genre or "",
        "available": body.available,
    }
    books_db.append(new_book)
    return new_book, 201


@app.put(
    "/books/<int:book_id>",
    tags=[library_tag],
    summary="Cap nhat thong tin sach",
    responses={"200": Book, "404": MessageResponse},
)
def update_book(path: BookPath, body: BookInput):
    book = next((item for item in books_db if item["id"] == path.book_id), None)
    if not book:
        return {"message": "Book not found"}, 404

    book["title"] = body.title
    book["author"] = body.author
    book["published_year"] = body.published_year
    book["genre"] = body.genre or ""
    book["available"] = body.available
    return book


@app.delete(
    "/books/<int:book_id>",
    tags=[library_tag],
    summary="Xoa sach",
    responses={"200": DeleteResponse, "404": MessageResponse},
)
def delete_book(path: BookPath):
    global books_db

    book = next((item for item in books_db if item["id"] == path.book_id), None)
    if not book:
        return {"message": "Book not found"}, 404

    books_db = [item for item in books_db if item["id"] != path.book_id]
    return {"message": "Book deleted", "id": path.book_id}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
