from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/petrol", tags=["Petrol Stations"])

@router.get("/", response_model=list[schemas.PetrolStationResponse])
def list_stations(db: Session = Depends(database.SessionLocal)):
    return crud.get_stations(db)
