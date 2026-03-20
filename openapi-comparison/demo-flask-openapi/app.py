from typing import Literal, List

from flask_openapi3 import Info, OpenAPI, Tag
from pydantic import BaseModel, EmailStr, RootModel

info = Info(title="Library Management API", version="1.0.0")
app = OpenAPI(__name__, info=info)

book_tag = Tag(name="Books", description="Quan ly sach")
member_tag = Tag(name="Members", description="Quan ly doc gia")
loan_tag = Tag(name="Loans", description="Quan ly muon tra")


class Book(BaseModel):
    id: int
    title: str
    author: str
    available: bool


class CreateBookRequest(BaseModel):
    title: str
    author: str


class BookPath(BaseModel):
    bookId: int


class Member(BaseModel):
    id: int
    name: str
    email: EmailStr


class CreateMemberRequest(BaseModel):
    name: str
    email: EmailStr


class Loan(BaseModel):
    id: int
    bookId: int
    memberId: int
    status: Literal["borrowed", "returned"]


class LoanPath(BaseModel):
    loanId: int


class CreateLoanRequest(BaseModel):
    bookId: int
    memberId: int


class ErrorResponse(BaseModel):
    message: str

class BookList(RootModel):
    root: List[Book]

class MemberList(RootModel):
    root: List[Member]


books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "available": True},
    {"id": 2, "title": "Refactoring", "author": "Martin Fowler", "available": True},
]

members = [
    {"id": 1, "name": "Nguyen Van A", "email": "a@example.com"},
]

loans = []


def find_book(book_id: int):
    return next((book for book in books if book["id"] == book_id), None)


def find_member(member_id: int):
    return next((member for member in members if member["id"] == member_id), None)


def find_loan(loan_id: int):
    return next((loan for loan in loans if loan["id"] == loan_id), None)


@app.get("/books", tags=[book_tag], responses={200: BookList})
def list_books():
    return books


@app.post("/books", tags=[book_tag], responses={201: Book})
def create_book(body: CreateBookRequest):
    book = {
        "id": len(books) + 1,
        "title": body.title,
        "author": body.author,
        "available": True,
    }
    books.append(book)
    return book, 201


@app.get(
    "/books/<int:bookId>",
    tags=[book_tag],
    responses={200: Book, 404: ErrorResponse},
)
def get_book(path: BookPath):
    book = find_book(path.bookId)
    if book is None:
        return {"message": "Book not found"}, 404
    return book


@app.get("/members", tags=[member_tag], responses={200: MemberList})
def list_members():
    return members


@app.post("/members", tags=[member_tag], responses={201: Member})
def create_member(body: CreateMemberRequest):
    member = {
        "id": len(members) + 1,
        "name": body.name,
        "email": body.email,
    }
    members.append(member)
    return member, 201


@app.post(
    "/loans",
    tags=[loan_tag],
    responses={201: Loan, 400: ErrorResponse},
)
def create_loan(body: CreateLoanRequest):
    book = find_book(body.bookId)
    if book is None:
        return {"message": "Book not found"}, 400

    if find_member(body.memberId) is None:
        return {"message": "Member not found"}, 400

    if not book["available"]:
        return {"message": "Book is not available"}, 400

    loan = {
        "id": len(loans) + 1,
        "bookId": body.bookId,
        "memberId": body.memberId,
        "status": "borrowed",
    }
    book["available"] = False
    loans.append(loan)
    return loan, 201


@app.patch(
    "/loans/<int:loanId>/return",
    tags=[loan_tag],
    responses={200: Loan, 404: ErrorResponse},
)
def return_loan(path: LoanPath):
    loan = find_loan(path.loanId)
    if loan is None:
        return {"message": "Loan not found"}, 404

    if loan["status"] == "returned":
        return loan

    loan["status"] = "returned"
    book = find_book(loan["bookId"])
    if book is not None:
        book["available"] = True
    return loan


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
