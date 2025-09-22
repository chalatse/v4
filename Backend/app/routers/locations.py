from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from .. import schemas, models, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Location)
def post_location(loc: schemas.LocationCreate, db: Session = Depends(get_db)):
    user_id = 1  # replace with JWT in production
    db_loc = models.LocationHistory(
        user_id=user_id,
        latitude=loc.latitude,
        longitude=loc.longitude,
        timestamp=datetime.utcnow()
    )
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

@router.get("/{user_id}", response_model=list[schemas.Location])
def get_location_history(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.LocationHistory).filter_by(user_id=user_id).all()

@router.get("/nearby", response_model=list[schemas.Location])
def get_nearby_users(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: float = Query(5000),
    db: Session = Depends(get_db)
):
    all_locations = db.query(models.LocationHistory).all()
    nearby = [
        loc for loc in all_locations
        if ((loc.latitude - lat)**2 + (loc.longitude - lon)**2)**0.5 * 111000 <= radius
    ]
    return nearby
