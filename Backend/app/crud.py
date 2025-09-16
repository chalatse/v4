from sqlalchemy.orm import Session
from . import models,schemas
from passlib.hash import bcrypt

def create_user(db:Session,user:schemas.UserCreate):
    hashed_pw = bcrypt.hash(user.password)
    db_user = models.User(email=user.email, hash_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_stations(db:Session):
    return db.query(models.PetrolStations).all()

