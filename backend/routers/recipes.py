from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, and_, or_, select
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
    query: str = Query(default=None),
    source_filter: str = Query(default=None),
    db_session: Session = Depends(get_session),
):

    # Source filter, which will check if the source is inside of the URL
    source_condition = True
    if source_filter:
        source_condition = Recipe.url.ilike(f"%{source_filter}%")

    if query:
        # Create OR conditions for keyword being inside of either title or description
        conditions = [
            or_(
                Recipe.title.ilike(f"%{keyword}%"),
                Recipe.description.ilike(f"%{keyword}%"),
            )
            for keyword in query.split()
        ]
        recipes = db_session.exec(
            select(Recipe)
            .filter(and_(*conditions))
            .filter(source_condition)
            .offset(skip)
            .limit(limit)
        ).all()
    else:
        recipes = db_session.exec(
            select(Recipe).filter(source_condition).offset(skip).limit(limit)
        ).all()

    return recipes
