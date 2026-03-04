from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid
from uuid import UUID
from typing import Optional

class BookCreate(BaseModel):
    name: str
    description: str
    author: str

class BookUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None

class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    uid: UUID
    name: str
    description: str
    author: str
    created_at: datetime
    updated_at: datetime