from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from models.Ingredient import IngredientGroup
from models.Recipe import Recipe
from database import get_session

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


@router.get("/{id}", response_model=Recipe)
def get_recipe_by_id(id: int, db_session: Session = Depends(get_session)):
    recipe = db_session.exec(select(Recipe).where(Recipe.id == id)).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found.")

    return recipe


@router.get("/", response_model=List[Recipe])
def get_recipes(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1),
    db_session: Session = Depends(get_session),
):
    return db_session.exec(select(Recipe).offset(skip).limit(limit)).all()
