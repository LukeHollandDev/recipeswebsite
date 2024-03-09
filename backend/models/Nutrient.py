from typing import Optional
from sqlmodel import SQLModel, Field


class Nutrient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(index=True)
    amount: Optional[float]
    unit: Optional[str]
    recipe_id: int = Field(foreign_key="recipe.id")
