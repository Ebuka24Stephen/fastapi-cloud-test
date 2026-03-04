from sqlmodel import SQLModel, Field, Column
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from uuid import UUID

class BookTable(SQLModel, table=True):
    uid: UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str 
    description: str 
    author: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
