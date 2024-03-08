from typing import Optional
from sqlmodel import SQLModel, Field
from . import Nutrient, Ingredient, Instruction, Resource


class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_other: str = Field(index=True)
    description: str
    url: Optional[str]
    image: Optional[str]
    cuisine: Optional[str] = Field(index=True)
    prepTime: Optional[str]
    totalTime: Optional[str]
    servings: Optional[float]
    # add list of nutrition
    # add list of ingredients
    # add list of instructions
    # add list of resources
