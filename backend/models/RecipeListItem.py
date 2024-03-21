from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from models.Recipe import Recipe


class RecipeListItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    recipe_id: int = Field(foreign_key="recipe.id")
    added_time: datetime = Field(default=datetime.now())
    recipe: Recipe = Relationship()
