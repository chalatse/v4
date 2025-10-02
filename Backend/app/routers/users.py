from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from passlib.context import CryptContext

router = APIRouter()

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Existing create_user function
# def create_user(db: Session, user: schemas.UserCreate):
#     hashed_password = pwd_context.hash(user.password)
#     db_user = models.User(email=user.email, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# # New function to get a user by email
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()

# New function to create a user based on Google info
def create_google_user(db: Session, email: str, google_id: str):
    # In this case, there is no password, so you can set a placeholder or None
    db_user = models.User(
        email=email,
        google_id=google_id,
        hashed_password=None # Or a special value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
