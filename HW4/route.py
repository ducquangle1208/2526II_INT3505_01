from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 2, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"}
]

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    return jsonify({"message": "Book not found"}), 404


@app.route('/books', methods=['POST'])
def create_book():
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
    data = request.json
    book = next((b for b in books if b["id"] == book_id), None)

    if not book:
        return jsonify({"message": "Book not found"}), 404

    book["title"] = data.get("title", book["title"])
    book["author"] = data.get("author", book["author"])

    return jsonify(book)


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted"})


if __name__ == '__main__':
    app.run(debug=True)