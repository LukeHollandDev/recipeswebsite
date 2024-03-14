from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Favourite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    recipe_id: int = Field(foreign_key="recipe.id")
    added_time: datetime = Field(default=datetime.now())
