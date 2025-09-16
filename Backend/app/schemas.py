from pydantic import BaseModel

class UserCreate(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    email:str
    class Config:
        orm_mode = True

class PetrolStationBase(BaseModel):
    name:str
    location:str
    price_per_litre:float

class PetrolStationResponse(BaseModel):
    id:int
    class Config:
        orm_mode = True
    