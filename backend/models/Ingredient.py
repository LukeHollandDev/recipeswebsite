from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Ingredient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    amount_lower: Optional[float]
    amount_upper: Optional[float]
    unit: Optional[str] = Field(index=True)
    note: Optional[str]
    group_id: int = Field(foreign_key="ingredientgroup.id")
    group: "IngredientGroup" = Relationship(back_populates="ingredients")


class IngredientGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    ingredients: List[Ingredient] = Relationship(back_populates="group")
    recipe_id: int = Field(foreign_key="recipe.id")
