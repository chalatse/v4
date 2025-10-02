from pydantic import BaseModel, EmailStr,Field, model_validator
from datetime import datetime

# ----- User -----
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id:int
    EmailStr: EmailStr
    google_id: str | None = None
    class Config:
        orm_mode = True

# ----- Google User ------
class GoogleUser(BaseModel):
    email: EmailStr
    sub: str

# ----- Petrol Station -----
class PetrolStationBase(BaseModel):
    name: str
    location: str  
    price_per_litre: float

class PetrolStationResponse(PetrolStationBase):
    id: int
    model_config = {"from_attributes": True}


# ----- Location -----
class LocationBase(BaseModel):
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    user_id: int
    timestamp: datetime

    model_config = {"from_attributes": True}


# ----- Traffic Report -----
class TrafficReportBase(BaseModel):
    type: str  
    longitude: float

class TrafficReportCreate(TrafficReportBase):
    pass

class TrafficReport(TrafficReportBase):
    id: int
    user_id: int
    timestamp: datetime
    model_config = {"from_attributes": True}


class PetrolStationSchema(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    price_per_litre: float
    map_url: str = None  

    model_config = {
        "from_attributes": True  
    }

    @model_validator(mode="after")
    def add_map_url(cls, model):
        model.map_url = f"https://www.google.com/maps?q={model.latitude},{model.longitude}"
        return model
