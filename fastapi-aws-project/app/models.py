from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    name: str = Field(index=True, min_length=1, max_length=120)
    email: str = Field(unique=True, index=True, min_length=3, max_length=255)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    email: Optional[str] = Field(default=None, min_length=3, max_length=255)


class BookBase(SQLModel):
    title: str = Field(index=True, min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=180)
    published_year: int = Field(ge=0, le=2100)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner: Optional[User] = Relationship(back_populates="books")


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int


class BookUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    author: Optional[str] = Field(default=None, min_length=1, max_length=180)
    published_year: Optional[int] = Field(default=None, ge=0, le=2100)
    user_id: Optional[int] = None

