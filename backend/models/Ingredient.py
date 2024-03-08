from typing import Optional
from sqlmodel import SQLModel, Field


class Ingredient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    amount_lower: Optional[float]
    amount_upper: Optional[float]
    unit: Optional[str] = Field(index=True)
    note: Optional[str]


class IngredientGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    # add list of ingredients
