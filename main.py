from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import database_models
from models import Books
from database import LocalSession, engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

default_books = [
    Books(name="The Great Gatsby", author="F. Scott Fitzgerald", status="available", borrower=None),
    Books(name="To Kill a Mockingbird", author="Harper Lee", status="borrowed", borrower="John Doe"),
    Books(name="1984", author="George Orwell", status="available", borrower=None)
]


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def init_db():
    db = LocalSession()
    try:
        count = db.query(database_models.Books).count()
        if count == 0:
            db_books = [database_models.Books(**book.model_dump()) for book in default_books]
            db.add_all(db_books)
            db.commit()
            print("Database seeded with default books!")
    finally:
        db.close()

@app.get("/")
def greet():
    return {"message": "Welcome to the Library System API"}

@app.get("/books")
def all_books(db: Session = Depends(get_db)):
    return db.query(database_models.Books).all()

@app.post("/books")
def add_books(book: Books, db: Session = Depends(get_db)):
    # Check if   already exists
    db_book = db.query(database_models.Books).filter(database_models.Books.name == book.name).first()
    if db_book:
        return "Book already exists"  
    else:  
        book.status = "available" 
        db_book = database_models.Books(**book.model_dump())
        db.add(db_book)
        db.commit()
        return db_book

@app.delete("/books/{name}")
def delete_books(name: str, db: Session = Depends(get_db)):
    db_book = db.query(database_models.Books).filter(database_models.Books.name == name).first()
    if db_book:        
        db.delete(db_book)
        db.commit()
        return "Book deleted successfully"
    else:
        return "Book not found"

@app.put("/books/{name}")
def update_books(name: str, book: Books, db: Session = Depends(get_db)):
    db_book = db.query(database_models.Books).filter(database_models.Books.name == name).first()
    if db_book:        
        db_book.name = book.name
        db_book.author = book.author
        db_book.status = book.status
        db_book.borrower = book.borrower
        db.commit()
        return "Book updated succesfully"
    else:
        return "Book not found"


@app.put("/books/{name}/borrow")
def borrow_book(name: str, borrower_name: str, db: Session = Depends(get_db)):
    db_book = db.query(database_models.Books).filter(database_models.Books.name == name).first()
    if not db_book:
        return "Book not found"
    if db_book.status == "borrowed":
        return "Book is already borrowed"
    else:    
        db_book.status = "borrowed"
        db_book.borrower = borrower_name
        db.commit()
    return "Book borrowed successfully"

@app.put("/books/{name}/return")
def return_book(name: str, db: Session = Depends(get_db)):
    db_book = db.query(database_models.Books).filter(database_models.Books.name == name).first()
    if not db_book:
        return "Book not found"        
    db_book.status = "available"
    db_book.borrower = None
    db.commit()
    return "Book returned successfully"