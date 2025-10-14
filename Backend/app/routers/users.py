from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from passlib.context import CryptContext

router = APIRouter()

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
