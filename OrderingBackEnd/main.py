# import re
# from fastapi import FastAPI, HTTPException, Depends, status
# from pydantic import BaseModel, Field, field_validator
# from typing import Annotated, Optional, List
# import models
# import bcrypt
# from database import engine, SessionLocal
# from sqlalchemy.orm import Session
# from datetime import date
# from fastapi.middleware.cors import CORSMiddleware # to join frontend and backend


# app = FastAPI()

# origins =[
#     'http://localhost:5173' #another application is allowed to call our fastapi application only if it runs on 3000 which is the port of react
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )
# models.Base.metadata.create_all(bind=engine)

# #for datavalidation

# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the API!"}


# #create our pydantic models validate the request from the react application 
# # Category
# class CategoryBase(BaseModel):
#     category_name: str
#     addons: Optional[str]
#     removable_items: Optional[str]


# class CategoryCreate(CategoryBase):
#     pass  # Use the same fields for creation


# class CategoryResponse(CategoryBase):
#     category_id: int

#     class Config:
#         from_attributes = True


# # FoodItem
# class FoodItemBase(BaseModel):
#     name: str
#     price: int
#     description: Optional[str]
#     category_id: int
#     price_to_make: int
#     photo: Optional[str]


# class FoodItemCreate(FoodItemBase):
#     pass  # No additional fields


# class FoodItemResponse(FoodItemBase):
#     food_id: int

#     class Config:
#         from_attributes = True


# # Feedback
# class FeedbackBase(BaseModel):
#     stars: int
#     user_id: int
#     food_id: int
#     comment: Optional[str]


# class FeedbackCreate(FeedbackBase):
#     pass  # No additional fields


# class FeedbackResponse(FeedbackBase):
#     feedback_id: int

#     class Config:
#         from_attributes = True


# # User
# class UserBase(BaseModel):
#     phone_number: str
#     address: str


# class UserCreate(UserBase):
#     username: str
#     phone_number: str
#     password: str
#     address: str

#     # @field_validator('username')
#     # def validate_username(cls, value):
#     #   if not re.match("^[a-zA-Z0-9_]+$", value):
#     #     raise ValueError("username must contain only alphanumeric charecters & underscores")
#     #   if value in usernames:
#     #     raise ValueError("usernanme must be unique")
        
#     #   usernames.append(value)
#     #   return value


# class UserResponse(UserBase):
#     user_id: int
#     username: str

#     class Config:
#         from_attributes = True


# # Orders
# class OrdersBase(BaseModel):
#     user_id: int
#     promo_code: Optional[str]
#     total_food_price: int
#     delivery_fee: int
#     status: str
#     order_date: date
#     payment_id: Optional[int]


# class OrdersCreate(OrdersBase):
#     pass  # No additional fields


# class OrdersResponse(OrdersBase):
#     order_id: int

#     class Config:
#         from_attributes = True


# # OrderDetails
# class OrderDetailsBase(BaseModel):
#     order_id: int
#     food_id: int
#     quantity: int


# class OrderDetailsCreate(OrderDetailsBase):
#     pass  # No additional fields


# class OrderDetailsResponse(OrderDetailsBase):
#     class Config:
#         from_attributes = True


# # Stats
# class StatsBase(BaseModel):
#     total_income: int
#     plate_of_the_day: int
#     net_income: int


# class StatsResponse(StatsBase):
#     stats_id: int

#     class Config:
#         from_attributes = True


# # ItemOfMonth
# class ItemOfMonthBase(BaseModel):
#     month: str
#     plate_of_month: int


# class ItemOfMonthResponse(ItemOfMonthBase):
#     class Config:
#         from_attributes = True


# # Admin
# class AdminBase(BaseModel):
#     username: str


# class AdminCreate(AdminBase):
#     password: str  # Password is only required during creation


# class AdminResponse(AdminBase):
#     admin_id: int

#     class Config:
#         from_attributes = True


# # Payment
# class PaymentBase(BaseModel):
#     payment_method: str
#     payment_status: str
#     transaction_id: str


# class PaymentCreate(PaymentBase):
#     pass  # No additional fields


# class PaymentResponse(PaymentBase):
#     payment_id: int

#     class Config:
#         from_attributes = True


# # PromoCode
# class PromoCodeBase(BaseModel):
#     discount: int
#     valid_from: date
#     valid_to: date


# class PromoCodeCreate(PromoCodeBase):
#     pass  # No additional fields


# class PromoCodeResponse(PromoCodeBase):
#     code: str

#     class Config:
#         from_attributes = True


# # #Create user or sign up backend
# # dependency injection try to create a database connection whether request is succeful or not close database connection
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session, Depends(get_db)]

# @app.post("/users/", status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserCreate, db: db_dependency):
#     # Check if the username already exists
#     existing_user = db.query(models.User).filter(models.User.username == user.username).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username unavailable")

#     # Hash the user's password before storing it
#     hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

#     # Proceed to create the user with the hashed password
#     db_user = models.User(
#         username=user.username,
#         password=hashed_password.decode("utf-8"),  # Decode to store as a string
#         phone_number=user.phone_number,
#         address=user.address,
#     )
#     db.add(db_user)
#     db.commit()
#     return {"message": f"User '{user.username}' created successfully"}


# # #login backend:
# # Pydantic model for login request
# class LoginRequest(BaseModel):
#     username: str
#     password: str

# @app.post("/login/")
# async def login(user: LoginRequest, db: Session = Depends(get_db)):
#     # Query the database for the user
#     db_user = db.query(models.User).filter(models.User.username == user.username).first()

#     # If user does not exist or password does not match
#     if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
#         raise HTTPException(status_code=401, detail="Invalid username or password")

#     # Login successful
#     return {"message": f"Welcome, {db_user.username}!"}


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
