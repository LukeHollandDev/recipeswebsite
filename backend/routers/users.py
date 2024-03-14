from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from models import User
from database import get_session

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def authenticate(req: Request):
    token = req.headers["Authorization"].replace("Bearer ", "")
    # Add code to decode this token, raise errors if invalid or expired
    # Look for the user_id inside of the token
    # if it's there query the user and return User object
    

@router.get("/list")
def get_user_recipe_list(
    db_session: Session = Depends(get_session), user: User = Depends(authenticate)
):
    # Add code to get user's list
    # Authenticated route
    pass


@router.post("/add_recipe/{recipe_id}")
def add_recipe_to_list(
    recipe_id: int,
    db_session: Session = Depends(get_session),
    user: User = Depends(authenticate),
):
    # Add code to add a recipe to the user's list
    # Authenticated route
    pass


@router.get("/favourites")
def get_user_favourites(
    db_session: Session = Depends(get_session), user: User = Depends(authenticate)
):
    # Add code to get user's favourites
    # Authenticated route
    pass


@router.post("/favourite_recipe/{recipe_id}")
def favourite_recipe(
    recipe_id: int,
    db_session: Session = Depends(get_session),
    user: User = Depends(authenticate),
):
    # Add code to favorite a recipe
    # Authenticated route
    pass


@router.post("/register")
def register_user():
    # Add code for user registration
    pass


@router.post("/login")
def login_user():
    # Add code for user login
    pass


@router.get("/{user_id}")
def get_user_by_id(user_id: int, db_session: Session = Depends(get_session)):
    # Add code to get a user by id
    pass
