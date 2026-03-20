export type Id = number;

export interface Book {
  id: Id;
  title: string;
  author: string;
  available: boolean;
}

export interface CreateBookRequest {
  title: string;
  author: string;
}

export interface Member {
  id: Id;
  name: string;
  email: string;
}

export interface CreateMemberRequest {
  name: string;
  email: string;
}

export interface Loan {
  id: Id;
  bookId: Id;
  memberId: Id;
  status: "borrowed" | "returned";
}

export interface CreateLoanRequest {
  bookId: Id;
  memberId: Id;
}

export interface ErrorResponse {
  message: string;
}

export const LibraryApi = {
  listBooks: {
    method: "GET",
    path: "/books",
    response: [] as Book[],
  },
  createBook: {
    method: "POST",
    path: "/books",
    body: {} as CreateBookRequest,
    response: {} as Book,
  },
  getBook: {
    method: "GET",
    path: "/books/:bookId",
    params: { bookId: 0 as Id },
    response: {} as Book | ErrorResponse,
  },
  listMembers: {
    method: "GET",
    path: "/members",
    response: [] as Member[],
  },
  createMember: {
    method: "POST",
    path: "/members",
    body: {} as CreateMemberRequest,
    response: {} as Member,
  },
  createLoan: {
    method: "POST",
    path: "/loans",
    body: {} as CreateLoanRequest,
    response: {} as Loan | ErrorResponse,
  },
  returnLoan: {
    method: "PATCH",
    path: "/loans/:loanId/return",
    params: { loanId: 0 as Id },
    response: {} as Loan | ErrorResponse,
  },
} as const;
