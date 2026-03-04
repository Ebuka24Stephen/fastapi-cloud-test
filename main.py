from db.database import BookTable 
from services.routes import book_router



from fastapi import FastAPI
from contextlib import asynccontextmanager 
from db.engine import engine
from sqlmodel import text, SQLModel

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Starting up: Connecting to database")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    print("Shutting down")

app = FastAPI(lifespan=lifespan)
app.include_router(book_router, prefix="/books", tags=['books'])