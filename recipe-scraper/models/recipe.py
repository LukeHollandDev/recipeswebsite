from pydantic import BaseModel
from typing import List, Optional


class Allergen(BaseModel):
    id: str
    name: str


class Cuisine(BaseModel):
    id: str
    name: str


class Ingredient(BaseModel):
    id: str
    name: str
    imageLink: Optional[str]
    imagePath: Optional[str]
    allergens: List[str]


class Nutrition(BaseModel):
    name: str
    amount: float
    unit: str


class Step(BaseModel):
    index: int
    instructions: str
    instructionsHTML: Optional[str]
    ingredients: List[str]
    utensils: List[str]
    timers: List[str]
    images: List[str]
    videos: List[str]


class Yield(BaseModel):
    yields: int
    ingredients: List[dict]


class Utensils(BaseModel):
    id: str
    name: str


class Recipe(BaseModel):
    id: str
    allergens: List[Allergen]
    cardLink: Optional[str]
    cuisines: List[Cuisine]
    description: str
    descriptionHTML: str
    headline: str
    imageLink: Optional[str]
    imagePath: Optional[str]
    ingredients: List[Ingredient]
    link: Optional[str]
    name: str
    nutrition: List[Nutrition]
    prepTime: str
    servingSize: int
    steps: List[Step]
    totalTime: str
    utensils: List[str]
    websiteUrl: Optional[str]
    yields: List[Yield]
