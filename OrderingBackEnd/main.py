import bcrypt
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from datetime import date
import models
from database import SessionLocal, engine

# Create the database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}

# Pydantic models for user operations
class UserCreate(BaseModel):
    username: str
    password: str
    phone_number: str
    address: str

class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/api/user/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: db_dependency):
    # Check if the username already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        return {"success": False, "message": "Username unavailable"}

    # Hash the user's password
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    # Create the user
    db_user = models.User(
        username=user.username,
        password=hashed_password.decode("utf-8"),
        phone_number=user.phone_number,
        address=user.address,
    )
    db.add(db_user)
    db.commit()

    # Return success with a dummy token
    return {
        "success": True,
        "token": "dummy-token",
        "message": f"User '{user.username}' created successfully"
    }


@app.post("/api/user/login")
async def login_user(user: LoginRequest, db: db_dependency):
    # Query the database for the user
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    # Verify password
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
        return {"success": False, "message": "Invalid username or password"}

    # Login successful - return a dummy token
    return {
        "success": True,
        "token": "dummy-token",
        "message": f"Welcome, {db_user.username}!"
    }
