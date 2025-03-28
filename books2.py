from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: str
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="ID is not needed on create",
        default=None
    )
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "An author",
                "description": "description about the book",
                "rating": 5,
                "publised_date": 2000
            }
        }
    }

BOOKS = [
    Book(1, "Computer Science", "Author one", "A very nice book", 5, 2000),
    Book(2, "Math", "Author two", "A great book", 1, 2000),
    Book(3, "Physics", "Author three", "Amazing book", 4, 2002),
    Book(4, "History", "Author four", "Thrilling book", 3, 2003),
    Book(5, "Football", "Author five", "Exciting book", 2, 2004),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/books/")
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    book_to_returns = []
    for book in BOOKS:
        if book_rating == book.rating:
            book_to_returns.append(book)
    
    return book_to_returns


@app.get("/books/publish/")
async def read_book_by_published_date(
    published_date: int = Query(gt=1999, lt=2031)
):
    
    books_to_return = (
        book for book in BOOKS
        if published_date == book.published_date
    )

    return books_to_return


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if book_id == BOOKS[i].id:
            BOOKS.pop(i)
            book_changed = True
            break
    
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book
