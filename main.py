from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Library API")


class BookIn(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int = Field(ge=0, le=2100)


class Book(BookIn):
    id: int


books: list[Book] = []
next_id = 1


@app.get("/books")
def get_books():
    return books


@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", status_code=201)
def add_book(data: BookIn):
    global next_id
    book = Book(id=next_id, **data.model_dump())
    next_id += 1
    books.append(book)
    return book


@app.put("/books/{book_id}")
def update_book(book_id: int, data: BookIn):
    for i, book in enumerate(books):
        if book.id == book_id:
            books[i] = Book(id=book_id, **data.model_dump())
            return books[i]
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book.id == book_id:
            books.pop(i)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")