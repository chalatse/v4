from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import schemas
from . import models
import math

# List all stations
def get_stations(db: Session):
    return db.query(models.PetrolStation).all()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# New function to get a user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# Find nearby stations using Haversine formula
def get_nearby_stations(db: Session, lat, lon, radius=5000):
    all_stations = db.query(models.PetrolStation).all()
    nearby = []
    for station in all_stations:
        distance = haversine_distance(lat, lon, station.latitude, station.longitude)
        if distance <= radius:
            nearby.append(station)
    return nearby


# Haversine distance in meters
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
