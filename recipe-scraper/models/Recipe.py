from typing import List, Optional, Union
from pydantic import BaseModel


class Nutrient(BaseModel):
    name: Optional[str]
    amount: Optional[float]
    unit: Optional[str]

    class Config:
        extra = "ignore"


class Ingredient(BaseModel):
    name: str
    amount_lower: Optional[float]
    amount_upper: Optional[float]
    unit: Optional[str]
    note: Optional[str]


class IngredientGroup(BaseModel):
    name: Optional[str]
    ingredients: List[Ingredient]


class Instruction(BaseModel):
    index: int
    text: str
    image: Optional[str]


class InstructionGroup(BaseModel):
    name: Optional[str]
    instructions: List[Instruction]


class Resource(BaseModel):
    name: Optional[str]
    type: Optional[str]
    value: Optional[str]


class Recipe(BaseModel):
    id: str
    title: str
    description: str
    url: Optional[str]
    image: Optional[str]
    cuisine: Optional[str]
    prepTime: Optional[int]
    totalTime: Optional[int]
    servings: Optional[float]
    nutrition: List[Nutrient]
    ingredients: List[IngredientGroup]
    instructions: List[InstructionGroup]
    additional_resources: List[Resource]

    class Config:
        extra = "ignore"
