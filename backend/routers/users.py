import re, os
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session, select, or_, and_
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from models import User, Recipe, RecipeListItem, Favourite
from database import get_session

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Get SECRET KEY from environment variables
SECRET_KEY = os.environ.get("BACKEND_SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def is_valid_password(password):
    # Define regular expression pattern
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$"

    # Check if password matches the pattern
    if re.match(pattern, password):
        return True
    else:
        return False


def is_valid_email(email):
    # Define regular expression pattern for email validation
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Check if email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_username(username):
    # Define regular expression pattern for username validation
    pattern = r"^[a-zA-Z0-9]{2,}$"

    # Check if username matches the pattern
    if re.match(pattern, username):
        return True
    else:
        return False


def create_jwt(user: User, days=30):
    # Generate user JWT with a 30 day expiration date
    expiration_date = datetime.now(UTC) + timedelta(days=days)
    return jwt.encode(
        {"id": user.id, "username": user.username, "exp": expiration_date},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def authenticate(
    request: Request,
    db_session: Session = Depends(get_session),
):
    # Get token from request headers
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="No Authorization header provided.")

    # Decode the token
    try:
        decoded_token = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        username, id = decoded_token.get("username"), decoded_token.get("id")
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Access token has expired.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials.")

    # Check that username is valid
    if not is_valid_username(username):
        raise HTTPException(status_code=401, detail="Could not validate credentials.")

    # Get the user from the database
    user = db_session.exec(
        select(User.User).where(or_(User.User.username == username, User.User.id == id))
    ).first()
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate credentials.")

    return user


@router.get("/")
def get_current_user(user: User = Depends(authenticate)):
    return {**user.model_dump(exclude={"password_hash": True})}


@router.post("/register")
def register_user(
    user: User.UserRegister,
    response: Response,
    db_session: Session = Depends(get_session),
):
    # Check that username is valid
    if not is_valid_username(user.username):
        raise HTTPException(status_code=400, detail="Username is not valid.")

    # Check the email is a valid email
    if not is_valid_email(user.email):
        raise HTTPException(
            status_code=400, detail="Email is not a valid email address."
        )

    # Check the password meets requirements
    if not is_valid_password(user.password):
        raise HTTPException(
            status_code=400, detail="Password does not meet requirements."
        )

    # Check that username and email are not in use
    existing_user = db_session.exec(
        select(User.User).where(
            or_(User.User.username == user.username, User.User.email == user.email)
        )
    ).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email or password already in use.")

    # Hash the password
    password_hash = pwd_context.hash(user.password)

    # Save the user to the database
    new_user = User.User(
        username=user.username, email=user.email, password_hash=password_hash
    )
    db_session.add(new_user)
    db_session.commit()

    # Generate user JWT
    token = create_jwt(new_user)

    # Return user (without the password_hash) and set-cookie header with token
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return {**new_user.model_dump(exclude={"password_hash": True})}


@router.post("/login")
def login_user(
    user: User.UserLogin,
    response: Response,
    db_session: Session = Depends(get_session),
):
    # Check that username is valid
    if not is_valid_username(user.username):
        raise HTTPException(status_code=400, detail="Username is not valid.")

    # Get the user from the database
    existing_user = db_session.exec(
        select(User.User).where(User.User.username == user.username)
    ).first()
    if not existing_user:
        raise HTTPException(
            status_code=401, detail="Username or password is incorrect."
        )

    # Check if password provided is correct
    if not pwd_context.verify(user.password, existing_user.password_hash):
        raise HTTPException(
            status_code=401, detail="Username or password is incorrect."
        )

    # Generate user JWT
    token = create_jwt(existing_user)

    # Return user (without the password_hash) and set-cookie header with token
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return {**existing_user.model_dump(exclude={"password_hash": True})}


@router.get("/recipe_list")
def get_user_recipe_list(user: User = Depends(authenticate)):
    return [
        {**recipe_list_item.model_dump(), "recipe": recipe_list_item.recipe}
        for recipe_list_item in user.recipe_list
    ]


@router.post("/recipe_list/{recipe_id}")
def add_recipe_to_list(
    recipe_id: int,
    db_session: Session = Depends(get_session),
    user: User = Depends(authenticate),
):
    # Get the recipe from the database
    recipe = db_session.exec(
        select(Recipe.Recipe).where(Recipe.Recipe.id == recipe_id)
    ).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe does not exist.")

    # Check if user already has on their list
    recipe_list_item = db_session.exec(
        select(RecipeListItem.RecipeListItem).where(
            and_(
                RecipeListItem.RecipeListItem.recipe_id == recipe_id,
                RecipeListItem.RecipeListItem.user_id == user.id,
            )
        )
    ).first()
    if recipe_list_item:
        raise HTTPException(status_code=409, detail="Recipe is already on user's list")

    # Add recipe to the user's list
    db_session.add(RecipeListItem.RecipeListItem(user_id=user.id, recipe_id=recipe.id))
    db_session.commit()

    return {"message": "Successfully added recipe to list."}


@router.delete("/recipe_list/{recipe_id}")
def favourite_recipe(
    recipe_id: int,
    db_session: Session = Depends(get_session),
    user: User = Depends(authenticate),
):
    # Add code to remvove recipe from user's recipe list
    return {"message": "Successfully removed the recipe from the user's list."}


@router.get("/favourites")
def get_user_favourites(user: User = Depends(authenticate)):
    return [
        {**favourite_item.model_dump(), "recipe": favourite_item.recipe}
        for favourite_item in user.favourite_recipes
    ]


@router.post("/favourite/{recipe_id}")
def favourite_recipe(
    recipe_id: int,
    db_session: Session = Depends(get_session),
    user: User = Depends(authenticate),
):
    # Get the recipe from the database
    recipe = db_session.exec(
        select(Recipe.Recipe).where(Recipe.Recipe.id == recipe_id)
    ).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe does not exist.")

    # Check if user already has on their list
    favourite_item = db_session.exec(
        select(Favourite.Favourite).where(
            and_(
                Favourite.Favourite.recipe_id == recipe_id,
                Favourite.Favourite.user_id == user.id,
            )
        )
    ).first()
    if favourite_item:
        raise HTTPException(
            status_code=409, detail="User has already favourited this recipe."
        )

    # Add recipe to the user's favourites
    db_session.add(Favourite.Favourite(user_id=user.id, recipe_id=recipe.id))
    db_session.commit()

    return {"message": "Successfully favourited the recipe."}


@router.delete("/favourite/{recipe_id}")
def favourite_recipe(
    recipe_id: int,
    db_session: Session = Depends(get_session),
    user: User = Depends(authenticate),
):
    # Add code to 'unfavourite' a recipe
    return {"message": "Successfully unfavourited the recipe."}


@router.get("/id/{user_id}")
def get_user_by_id(user_id: int, db_session: Session = Depends(get_session)):
    # Get the user from the database
    user = db_session.exec(select(User.User).where(User.User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found with provided id.")

    return {**user.model_dump(exclude={"password_hash": True})}


@router.get("/username/{username}")
def get_user_by_id(username: str, db_session: Session = Depends(get_session)):
    # Get the user from the database
    user = db_session.exec(
        select(User.User).where(User.User.username == username)
    ).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found with provided username."
        )

    return {**user.model_dump(exclude={"password_hash": True})}
