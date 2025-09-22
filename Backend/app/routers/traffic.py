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

@router.post("/", response_model=schemas.TrafficReport)
def report_traffic(report: schemas.TrafficReportCreate, db: Session = Depends(get_db)):
    user_id = 1
    db_report = models.TrafficReport(
        user_id=user_id,
        type=report.type,
        latitude=report.latitude,
        longitude=report.longitude,
        timestamp=datetime.utcnow()
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/nearby", response_model=list[schemas.TrafficReport])
def get_nearby_traffic(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: float = Query(5000),
    db: Session = Depends(get_db)
):
    all_reports = db.query(models.TrafficReport).all()
    nearby = [
        rep for rep in all_reports
        if ((rep.latitude - lat)**2 + (rep.longitude - lon)**2)**0.5 * 111000 <= radius
    ]
    return nearby
