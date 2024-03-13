from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from models.Ingredient import IngredientGroup, Ingredient
from models.Recipe import Recipe
from database import get_session

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


def get_full_recipe(recipe: Recipe):
    # extract the ingredients
    ingredient_groups = [
        {
            **group.model_dump(),
            "ingredients": [ingredient for ingredient in group.ingredients],
        }
        for group in recipe.ingredient_groups
    ]

    # extract the instructions
    instruction_groups = [
        {
            **group.model_dump(),
            "instructions": [instruction for instruction in group.instructions],
        }
        for group in recipe.instruction_groups
    ]

    return {
        **recipe.model_dump(),
        "nutrients": [nutrient for nutrient in recipe.nutrients],
        "resources": [resource for resource in recipe.resources],
        "ingredient_groups": ingredient_groups,
        "instruction_groups": instruction_groups,
    }


@router.get("/{id}")
def get_recipe_by_id(id: int, db_session: Session = Depends(get_session)):
    recipe = db_session.exec(select(Recipe).where(Recipe.id == id)).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found.")

    return get_full_recipe(recipe)


@router.get("/", response_model=List[Recipe])
def get_recipes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
    db_session: Session = Depends(get_session),
):
    return db_session.exec(select(Recipe).offset(skip).limit(limit)).all()
