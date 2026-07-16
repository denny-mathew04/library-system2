from fastapi import FastAPI
from models import Books

app = FastAPI()

books = [
    Books(name="The Great Gatsby", author="F. Scott Fitzgerald", status="available", borrower=None),
    Books(name='To Kill a Mockingbird', author='Harper Lee', status='borrowed', borrower=None),
    Books(name='1984', author='George Orwell', status='available', borrower=None)
]
@app.get("/")
def greet():
    return "welcome"

@app.get("/books")
def all_books():
        return books

@app.get("/books/{name}")
def single_book(name:str):
    for book in books:
        return book

@app.post("/books")
def add_books(book:Books):
    books.append(book)
    return book

@app.put("/books/{name}")
def update_books(name:str,book:Books):
    for book in books:
        if book.name == name:
            book.name = book.name
            book.author = book.author
            book.status = book.status
            book.borrower = book.borrower
            return book

@app.delete("/books/{name}")
def delete_books(name:str,book:Books):
    for book in books:
        if book.name == name:
            books.remove(book)
            return book

@app.put("/books/{name}")
def update_status(name:str,status:str,borrower:str,book:Books):
    for book in books:
        if book.name == name:
            book.status = status
            if status == "borrowed":
                book.borrower = borrower
            return book




    
    