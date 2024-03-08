from typing import Optional
from sqlmodel import SQLModel, Field


class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    type: Optional[str] = Field(index=True)
    value: Optional[str]
