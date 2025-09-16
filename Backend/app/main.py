from fastapi import FastAPI
# from .routers import auth, petrol
from app.routers import auth, petrol
from .database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Navify API")

app.include_router(auth.router)
app.include_router(petrol.router)

@app.get("/")
def root():
    return {"message": "Welcome to Navify API "}
