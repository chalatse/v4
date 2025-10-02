from fastapi import FastAPI
from sqlalchemy import inspect
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
import os

from .database import engine
from . import models
from .routers import users, petrol, locations, traffic, chatbot, auth  # Add auth here

# Load environment variables
load_dotenv()

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Navify API")

# Add session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET"))

# Configure Authlib OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)
app.state.oauth = oauth

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Navify API"}

# Include all routers
app.include_router(auth.router)  # Add this line - no prefix needed since it's in the router
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(petrol.router, prefix="/petrol", tags=["Petrol Stations"])
app.include_router(locations.router, prefix="/locations", tags=["Locations"])
app.include_router(traffic.router, prefix="/traffic", tags=["Traffic Reports"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])

# Debug: print tables
inspector = inspect(engine)
print("Tables created:", inspector.get_table_names())