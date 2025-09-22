from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    locations = relationship("LocationHistory", back_populates="user")



class LocationHistory(Base):
    __tablename__ = "location_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="locations")


class TrafficReport(Base):
    __tablename__ = "traffic_reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")

class PetrolStation(Base):
    __tablename__ = "petrol_stations"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    price_per_litre = Column(Float)

    @property
    def location(self):
        return f"{self.latitude},{self.longitude}"

