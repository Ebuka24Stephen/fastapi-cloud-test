from fastapi import APIRouter, status, Depends 
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookUpdate, BookCreate, BookRead
from sqlmodel import text, select, desc
import uuid
from typing import List
from db.engine import get_session
from services.service import BookService
from db.database import BookTable


book_router = APIRouter()
book_service = BookService()

@book_router.get("/", response_model=list[BookRead])
async def get_all_books(session:AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookRead)
async def create_book(book_data:BookCreate, session:AsyncSession=Depends(get_session)) -> dict:
    book = await book_service.create_book(book_data, session)
    return book 

@book_router.get("/{book_uid}", response_model=BookRead, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_uid:uuid.UUID, session:AsyncSession=Depends(get_session)):
    book = await book_service.get_book_by_id(book_uid, session)
    if not book:
        raise HTTPException(status_code=404, detail='Book not found')
    return book 
    

@book_router.put("/{book_uid}", response_model=BookRead,status_code=status.HTTP_201_CREATED)
async def update_book(book_uid:uuid.UUID, update_book:BookUpdate, session:AsyncSession=Depends(get_session)):
    book = await book_service.update_book(book_uid, update_book, session)
    if not book:
        raise HTTPException(status_code=404, detail='Book not found')
    return book 

@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:uuid.UUID, session:AsyncSession=Depends(get_session)):
    book = await book_service.delete_book(book_id, session)
    if not book:
        raise HTTPException(status_code=404, detail='Not found!')
    return book