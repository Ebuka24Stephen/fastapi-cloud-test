from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter
from typing import Annotated 
from sqlmodel import Field, SQLModel, Session, create_engine, select
from contextlib import asynccontextmanager 
from pydantic import BaseModel, ConfigDict

class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str 

class ItemResponse(BaseModel):
    name: str 
    age: int | None = None
    secret_name: str
    id: int
    model_config = ConfigDict(from_attributes=True)

class ItemCreate(BaseModel):
    name: str 
    age: int | None = None
    secret_name: str

class ItemUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

root_router = APIRouter()

@root_router.post("/item/", response_model=ItemResponse)
async def create_item(item:ItemCreate, session:SessionDep):
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@root_router.get("/item/{item_id}/", response_model=ItemResponse)
async def get_item(item_id:int, session:SessionDep):
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@root_router.get("/item/", response_model=list[ItemResponse])
async def get_items(session:SessionDep):
    return session.exec(select(Item)).all()











app = FastAPI(lifespan=lifespan)
app.include_router(root_router)