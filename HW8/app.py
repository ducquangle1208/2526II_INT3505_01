from typing import List, Optional

from flask import jsonify, make_response, request
from flask_cors import CORS
from flask_openapi3 import APIBlueprint, Info, OpenAPI, Tag
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


SUPPORTED_VERSIONS = {"v1", "v2"}
v1_api = APIBlueprint("v1_api", __name__, abp_tags=[library_tag])
v2_api = APIBlueprint("v2_api", __name__, abp_tags=[library_tag])


def normalize_version(raw_version: Optional[str]) -> Optional[str]:
    if raw_version is None:
        return None

    version = raw_version.strip().lower()
    if version in {"1", "v1"}:
        return "v1"
    if version in {"2", "v2"}:
        return "v2"
    return None


def version_error(raw_version: Optional[str]):
    return {
        "message": "Unsupported API version",
        "provided_version": raw_version,
        "supported_versions": sorted(SUPPORTED_VERSIONS),
    }, 400


def resolve_version_from_request():
    query_version = request.args.get("version")
    header_version = request.headers.get("X-API-Version")

    normalized_query = normalize_version(query_version) if query_version else None
    normalized_header = normalize_version(header_version) if header_version else None

    if query_version and not normalized_query:
        return None, None, version_error(query_version)

    if header_version and not normalized_header:
        return None, None, version_error(header_version)

    if normalized_query and normalized_header and normalized_query != normalized_header:
        return None, None, (
            {
                "message": "Conflicting API versions in query parameter and header",
                "query_version": query_version,
                "header_version": header_version,
            },
            400,
        )

    if normalized_header:
        return normalized_header, "header", None

    if normalized_query:
        return normalized_query, "query", None

    return "v1", "default", None


def build_response(payload, version: str, strategy: str, status_code: int = 200):
    response = make_response(jsonify(payload), status_code)
    response.headers["X-API-Version"] = version
    response.headers["X-Version-Strategy"] = strategy
    return response


def serialize_book(book: dict, version: str):
    serialized = dict(book)
    if version == "v2":
        serialized["status"] = "available" if book["available"] else "checked-out"
    return serialized


def serialize_books(version: str):
    return [serialize_book(book, version) for book in books_db]


def find_book(book_id: int):
    return next((item for item in books_db if item["id"] == book_id), None)


def create_book_record(body: BookInput):
    new_book = {
        "id": books_db[-1]["id"] + 1 if books_db else 1,
        "title": body.title,
        "author": body.author,
        "published_year": body.published_year,
        "genre": body.genre or "",
        "available": body.available,
    }
    books_db.append(new_book)
    return new_book


def update_book_record(book: dict, body: BookInput):
    book["title"] = body.title
    book["author"] = body.author
    book["published_year"] = body.published_year
    book["genre"] = body.genre or ""
    book["available"] = body.available
    return book


def delete_book_record(book_id: int):
    global books_db
    books_db = [item for item in books_db if item["id"] != book_id]


def list_books_response(version: str, strategy: str):
    return build_response(serialize_books(version), version, strategy)


def get_book_response(book_id: int, version: str, strategy: str):
    book = find_book(book_id)
    if not book:
        return build_response({"message": "Book not found"}, version, strategy, 404)
    return build_response(serialize_book(book, version), version, strategy)


def create_book_response(body: BookInput, version: str, strategy: str):
    new_book = create_book_record(body)
    return build_response(serialize_book(new_book, version), version, strategy, 201)


def update_book_response(book_id: int, body: BookInput, version: str, strategy: str):
    book = find_book(book_id)
    if not book:
        return build_response({"message": "Book not found"}, version, strategy, 404)

    updated_book = update_book_record(book, body)
    return build_response(serialize_book(updated_book, version), version, strategy)


def delete_book_response(book_id: int, version: str, strategy: str):
    book = find_book(book_id)
    if not book:
        return build_response({"message": "Book not found"}, version, strategy, 404)

    delete_book_record(book_id)
    return build_response({"message": "Book deleted", "id": book_id}, version, strategy)


@app.get("/books", tags=[library_tag], summary="Lay danh sach sach", responses={"200": BookList})
def get_books():
    version, strategy, error = resolve_version_from_request()
    if error:
        return error
    return list_books_response(version, strategy)


@app.get(
    "/books/<int:book_id>",
    tags=[library_tag],
    summary="Lay chi tiet sach theo ID",
    responses={"200": Book, "404": MessageResponse},
)
def get_book(path: BookPath):
    version, strategy, error = resolve_version_from_request()
    if error:
        return error
    return get_book_response(path.book_id, version, strategy)


@app.post("/books", tags=[library_tag], summary="Them sach moi", responses={"201": Book})
def create_book(body: BookInput):
    version, strategy, error = resolve_version_from_request()
    if error:
        return error
    return create_book_response(body, version, strategy)


@app.put(
    "/books/<int:book_id>",
    tags=[library_tag],
    summary="Cap nhat thong tin sach",
    responses={"200": Book, "404": MessageResponse},
)
def update_book(path: BookPath, body: BookInput):
    version, strategy, error = resolve_version_from_request()
    if error:
        return error
    return update_book_response(path.book_id, body, version, strategy)


@app.delete(
    "/books/<int:book_id>",
    tags=[library_tag],
    summary="Xoa sach",
    responses={"200": DeleteResponse, "404": MessageResponse},
)
def delete_book(path: BookPath):
    version, strategy, error = resolve_version_from_request()
    if error:
        return error
    return delete_book_response(path.book_id, version, strategy)


@v1_api.get("/books", summary="Lay danh sach sach v1", responses={"200": BookList})
def get_books_v1():
    return list_books_response("v1", "path")


@v1_api.get("/books/<int:book_id>", summary="Lay chi tiet sach theo ID v1", responses={"200": Book, "404": MessageResponse})
def get_book_v1(path: BookPath):
    return get_book_response(path.book_id, "v1", "path")


@v1_api.post("/books", summary="Them sach moi v1", responses={"201": Book})
def create_book_v1(body: BookInput):
    return create_book_response(body, "v1", "path")


@v1_api.put("/books/<int:book_id>", summary="Cap nhat thong tin sach v1", responses={"200": Book, "404": MessageResponse})
def update_book_v1(path: BookPath, body: BookInput):
    return update_book_response(path.book_id, body, "v1", "path")


@v1_api.delete("/books/<int:book_id>", summary="Xoa sach v1", responses={"200": DeleteResponse, "404": MessageResponse})
def delete_book_v1(path: BookPath):
    return delete_book_response(path.book_id, "v1", "path")


@v2_api.get("/books", summary="Lay danh sach sach v2", responses={"200": BookList})
def get_books_v2():
    return list_books_response("v2", "path")


@v2_api.get("/books/<int:book_id>", summary="Lay chi tiet sach theo ID v2", responses={"200": Book, "404": MessageResponse})
def get_book_v2(path: BookPath):
    return get_book_response(path.book_id, "v2", "path")


@v2_api.post("/books", summary="Them sach moi v2", responses={"201": Book})
def create_book_v2(body: BookInput):
    return create_book_response(body, "v2", "path")


@v2_api.put("/books/<int:book_id>", summary="Cap nhat thong tin sach v2", responses={"200": Book, "404": MessageResponse})
def update_book_v2(path: BookPath, body: BookInput):
    return update_book_response(path.book_id, body, "v2", "path")


@v2_api.delete("/books/<int:book_id>", summary="Xoa sach v2", responses={"200": DeleteResponse, "404": MessageResponse})
def delete_book_v2(path: BookPath):
    return delete_book_response(path.book_id, "v2", "path")


app.register_api(v1_api, url_prefix="/api/v1")
app.register_api(v2_api, url_prefix="/api/v2")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
