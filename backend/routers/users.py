import re, os
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session, select, or_
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from models import User
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
    token = request.headers["Authorization"].replace("Bearer ", "")

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
