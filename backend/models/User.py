from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from models import Favourite, RecipeListItem


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: Optional[str]
    password_hash: str
    recipe_list: List[RecipeListItem.RecipeListItem] = Relationship()
    favourite_recipes: List[Favourite.Favourite] = Relationship()


class UserRegister(SQLModel):
    username: str
    email: str
    password: str


class UserLogin(SQLModel):
    username: str
    password: str
