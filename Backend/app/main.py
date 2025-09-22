from fastapi import FastAPI
from sqlalchemy import inspect
from .database import engine
from . import models
from .routers import users, petrol, locations, traffic, chatbot

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Navify API")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Navify API"}

# Include all routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(petrol.router, prefix="/petrol", tags=["Petrol Stations"])
app.include_router(locations.router, prefix="/locations", tags=["Locations"])
app.include_router(traffic.router, prefix="/traffic", tags=["Traffic Reports"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])

# Debug: print tables
inspector = inspect(engine)
print("Tables created:", inspector.get_table_names())
