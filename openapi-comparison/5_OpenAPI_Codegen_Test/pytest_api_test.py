import requests


BASE_URL = "http://localhost:5000"


def test_list_books():
    response = requests.get(f"{BASE_URL}/books", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "title" in data[0]


def test_create_member():
    payload = {
        "name": "Le Thi C",
        "email": "c@example.com",
    }
    response = requests.post(f"{BASE_URL}/members", json=payload, timeout=5)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]


def test_create_and_return_loan():
    new_book = {
        "title": "Designing Data-Intensive Applications",
        "author": "Martin Kleppmann",
    }
    book_response = requests.post(f"{BASE_URL}/books", json=new_book, timeout=5)
    assert book_response.status_code == 201
    book = book_response.json()

    member_payload = {
        "name": "Pham Van D",
        "email": "d@example.com",
    }
    member_response = requests.post(f"{BASE_URL}/members", json=member_payload, timeout=5)
    assert member_response.status_code == 201
    member = member_response.json()

    loan_payload = {
        "bookId": book["id"],
        "memberId": member["id"],
    }
    loan_response = requests.post(f"{BASE_URL}/loans", json=loan_payload, timeout=5)
    assert loan_response.status_code == 201
    loan = loan_response.json()
    assert loan["status"] == "borrowed"

    return_response = requests.patch(
        f"{BASE_URL}/loans/{loan['id']}/return",
        timeout=5,
    )
    assert return_response.status_code == 200
    returned_loan = return_response.json()
    assert returned_loan["status"] == "returned"
