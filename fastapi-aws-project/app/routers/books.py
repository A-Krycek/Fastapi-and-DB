from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Book, BookCreate, BookRead, BookUpdate, User


router = APIRouter(prefix="/books", tags=["Books"])


def validate_user(user_id: int | None, session: Session) -> None:
    if user_id is not None and session.get(User, user_id) is None:
        raise HTTPException(status_code=404, detail="Usuario propietario no encontrado")


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    validate_user(book.user_id, session)
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.get("/", response_model=List[BookRead])
def read_books(
    offset: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    return session.exec(select(Book).offset(offset).limit(limit)).all()


@router.get("/{book_id}", response_model=BookRead)
def read_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book


@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    book_id: int, book_update: BookUpdate, session: Session = Depends(get_session)
):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    book_data = book_update.model_dump(exclude_unset=True)
    if "user_id" in book_data:
        validate_user(book_data["user_id"], session)
    db_book.sqlmodel_update(book_data)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    session.delete(book)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

