from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import text, select, desc
from db.database import BookTable
import uuid
from .schemas import BookUpdate, BookCreate, BookRead
from datetime import datetime 

class BookService:
    async def get_all_books(self, session:AsyncSession):
        statement = select(BookTable).order_by(BookTable.created_at.desc())
        result = await session.exec(statement)
        return result.all()

    async def get_book_by_id(self, book_uid:uuid.UUID, session:AsyncSession):
        book = await session.get(BookTable, book_uid)
        return book

    async def create_book(self, book_data:BookCreate, session:AsyncSession):
        new_book = BookTable(**book_data.model_dump())
        new_book.created_at = datetime.utcnow()
        try:
            session.add(new_book)
            await session.commit()
            await session.refresh(new_book)
            return new_book
        except Exception:
            await session.rollback()
            raise

    async def update_book(self, book_uid:uuid.UUID, update_data:BookUpdate, session:AsyncSession):
        book = await session.get(BookTable, book_uid)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        data = update_data.model_dump(exclude_unset=True, exclude_none=True)
        for k, v in data.items():
            setattr(book, k, v)
            book.updated_at = datetime.utcnow()
            try:
                session.add(book)
                await session.commit()
                await session.refresh(book)
                return book
            except Exception:
                await session.rollback()
                raise



    async def delete_book(self, book_uid:uuid.UUID, session:AsyncSession):
        book = await session.get(BookTable, book_uid)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        try:
            await session.delete(book)
            await session.commit()
            return {"deleted": True}
        except Exception:
            await session.rollback()
            raise