import re, os
from fastapi import Depends, HTTPException, Request
from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime, timedelta, UTC
from passlib.context import CryptContext
from sqlmodel import Session, or_, select
from models import User
from database import get_session

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
