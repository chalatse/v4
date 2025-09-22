from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models import PetrolStation as PetrolStationModel
from app.schemas import PetrolStationSchema
from app.database import get_db
from typing import List
from app import crud, schemas 

router = APIRouter(prefix="/petrol", tags=["Petrol Stations"])

# Seed stations (run once at startup)
@router.on_event("startup")
def seed_stations():
    db = next(get_db())
    try:
        if not db.query(PetrolStationModel).first():
            stations = [
                PetrolStationModel(name="Shell Downtown", latitude=-26.2041, longitude=28.0473, price_per_litre=23.5),
                PetrolStationModel(name="BP Central", latitude=-26.2050, longitude=28.0450, price_per_litre=24.0),
            ]
            db.add_all(stations)
            db.commit()
    finally:
        db.close()


# List all petrol stations
@router.get("/", response_model=List[PetrolStationSchema])
def list_stations(db: Session = Depends(get_db)):
    stations = db.query(PetrolStationModel).all()
    return stations


# Nearby petrol stations
@router.get("/nearby", response_model=List[PetrolStationSchema])
def nearby_stations(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: float = Query(5000),
    db: Session = Depends(get_db)
):
    # Example: crud.get_nearby_stations already returns SQLAlchemy objects
    stations = crud.get_nearby_stations(db, lat, lon, radius)
    return stations


@router.get("/petrol/", response_model=list[PetrolStationSchema])
def get_petrol_stations(db: Session = Depends(get_db)):
    stations = db.query(PetrolStationModel).all()
    return stations  # Pydantic now adds `map_url` automatically

