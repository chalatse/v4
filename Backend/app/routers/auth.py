from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .. import crud, schemas, database, models

router = APIRouter(prefix="/auth", tags=["Auth"])

# Regular signup endpoint
# @router.post("/signup", response_model=schemas.UserResponse)
# def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
#     return crud.create_user(db, user)

@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        return crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    
# Google OAuth Login - initiates the OAuth flow
@router.get("/google/login")
async def google_login(request: Request):
    """Redirect to Google OAuth login"""
    oauth = request.app.state.oauth
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Google OAuth Callback - handles the response from Google
@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(database.get_db)):
    """Handle Google OAuth callback and create/login user"""
    try:
        oauth = request.app.state.oauth
        
        # Get token from Google
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user info from Google")
        
        # Check if user exists by email
        user = db.query(models.User).filter(
            models.User.email == user_info['email']
        ).first()
        
        # Create new user if doesn't exist
        if not user:
            user = models.User(
                email=user_info['email'],
                username=user_info.get('name', user_info['email'].split('@')[0]),
                google_id=user_info['sub'],
                profile_picture=user_info.get('picture'),
                # Set a random password or leave it nullable for OAuth users
                # hashed_password=None  # or generate a random one
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update google_id and profile picture if user exists but signed up via email
            if not user.google_id:
                user.google_id = user_info['sub']
            if user_info.get('picture'):
                user.profile_picture = user_info.get('picture')
            db.commit()
            db.refresh(user)
        
        # Store user info in session
        request.session['user'] = {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }
        
        # Return success response or redirect to frontend
        # For web app, you might want to redirect to your frontend:
        # return RedirectResponse(url=f"http://localhost:3000/dashboard?user_id={user.id}")
        
        return {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "profile_picture": user.profile_picture
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

# Get current logged-in user
@router.get("/me")
async def get_current_user(request: Request, db: Session = Depends(database.get_db)):
    """Get current logged-in user from session"""
    user_session = request.session.get('user')
    
    if not user_session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Optionally fetch fresh user data from database
    user = db.query(models.User).filter(models.User.id == user_session['id']).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "profile_picture": user.profile_picture
    }

# Logout endpoint
@router.post("/logout")
async def logout(request: Request):
    """Logout user by clearing session"""
    request.session.clear()
    return {"message": "Logged out successfully"}