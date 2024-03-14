from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from models import Nutrient, Ingredient, Instruction, Resource


class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_other: str = Field(index=True)
    title: str = Field(index=True)
    description: str
    url: Optional[str]
    image: Optional[str]
    cuisine: Optional[str] = Field(index=True)
    prepTime: Optional[str]
    totalTime: Optional[str]
    servings: Optional[float]
    nutrients: List[Nutrient.Nutrient] = Relationship()
    ingredient_groups: List[Ingredient.IngredientGroup] = Relationship()
    instruction_groups: List[Instruction.InstructionGroup] = Relationship()
    resources: List[Resource.Resource] = Relationship()
