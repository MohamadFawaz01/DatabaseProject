from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import bcrypt
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    phone_number: str
    address: str

# Create user (signup endpoint)
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: db_dependency):
    # Check if the username already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username unavailable")

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
    return {"message": f"User '{user.username}' created successfully"}

# Login (authentication endpoint)
@app.post("/login/")
async def login(user: LoginRequest, db: db_dependency):
    # Query the database for the user
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    # Verify password
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": f"Welcome, {db_user.username}!"}
