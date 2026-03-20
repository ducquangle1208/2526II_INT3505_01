import "@typespec/http";
import "@typespec/openapi3";

using TypeSpec.Http;

@service({
  title: "Library Management API"
})
namespace Library;

model Book {
  id: int32;
  title: string;
  author: string;
  available: boolean;
}

model CreateBookRequest {
  title: string;
  author: string;
}

model Member {
  id: int32;
  name: string;
  email: string;
}

model CreateMemberRequest {
  name: string;
  email: string;
}

model Loan {
  id: int32;
  bookId: int32;
  memberId: int32;
  status: "borrowed" | "returned";
}

model CreateLoanRequest {
  bookId: int32;
  memberId: int32;
}

model ErrorResponse {
  message: string;
}

@route("/books")
interface BooksApi {
  @get
  listBooks(): Book[];

  @post
  @statusCode _: 201;
  createBook(@body body: CreateBookRequest): Book | ErrorResponse;
}

@route("/books/{bookId}")
interface BookDetailApi {
  @get
  getBook(@path bookId: int32): Book | ErrorResponse;
}

@route("/members")
interface MembersApi {
  @get
  listMembers(): Member[];

  @post
  @statusCode _: 201;
  createMember(@body body: CreateMemberRequest): Member;
}

@route("/loans")
interface LoansApi {
  @post
  @statusCode _: 201;
  createLoan(@body body: CreateLoanRequest): Loan | ErrorResponse;
}

@route("/loans/{loanId}/return")
interface ReturnLoanApi {
  @patch
  returnLoan(@path loanId: int32): Loan | ErrorResponse;
}
