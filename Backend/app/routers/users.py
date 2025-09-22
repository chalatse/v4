from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pw = "not_really_hashed_" + user.password  # replace with real hashing
    db_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
