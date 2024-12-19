import re
from fastapi import APIRouter, FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional, List
import models
import schemas
import bcrypt
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import date
from fastapi.middleware.cors import CORSMiddleware # to join frontend and backend


app = FastAPI()

origins =[
    'http://localhost:5173' #another application is allowed to call our fastapi application only if it runs on 3000 which is the port of react
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
models.Base.metadata.create_all(bind=engine)

#for datavalidation

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API!"}


#create our pydantic models validate the request from the react application 
# Category
class CategoryBase(BaseModel):
    category_name: str
    addons: Optional[str]
    removable_items: Optional[str]


class CategoryCreate(CategoryBase):
    pass  # Use the same fields for creation


class CategoryResponse(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True


# FoodItem
class FoodItemBase(BaseModel):
    name: str
    price: int
    description: Optional[str]
    category_id: int
    price_to_make: int
    photo: Optional[str]


class FoodItemCreate(FoodItemBase):
    pass  # No additional fields


class FoodItemResponse(FoodItemBase):
    food_id: int

    class Config:
        from_attributes = True


# Feedback
class FeedbackBase(BaseModel):
    stars: int
    user_id: int
    food_id: int
    comment: Optional[str]


class FeedbackCreate(FeedbackBase):
    pass  # No additional fields


class FeedbackResponse(FeedbackBase):
    feedback_id: int

    class Config:
        from_attributes = True


# User
class UserBase(BaseModel):
    phone_number: str
    address: str


class UserCreate(UserBase):
    username: str
    phone_number: str
    password: str
    address: str

    # @field_validator('username')
    # def validate_username(cls, value):
    #   if not re.match("^[a-zA-Z0-9_]+$", value):
    #     raise ValueError("username must contain only alphanumeric charecters & underscores")
    #   if value in usernames:
    #     raise ValueError("usernanme must be unique")
        
    #   usernames.append(value)
    #   return value


class UserResponse(UserBase):
    user_id: int
    username: str

    class Config:
        from_attributes = True


# Orders
class OrdersBase(BaseModel):
    user_id: int
    promo_code: Optional[str]
    total_food_price: int
    delivery_fee: int
    status: str
    order_date: date
    payment_id: Optional[int]


class OrdersCreate(OrdersBase):
    pass  # No additional fields


class OrdersResponse(OrdersBase):
    order_id: int

    class Config:
        from_attributes = True


# OrderDetails
class OrderDetailsBase(BaseModel):
    order_id: int
    food_id: int
    quantity: int


class OrderDetailsCreate(OrderDetailsBase):
    pass  # No additional fields


class OrderDetailsResponse(OrderDetailsBase):
    class Config:
        from_attributes = True


# Stats
class StatsBase(BaseModel):
    total_income: int
    plate_of_the_day: int
    net_income: int


class StatsResponse(StatsBase):
    stats_id: int

    class Config:
        from_attributes = True


# ItemOfMonth
class ItemOfMonthBase(BaseModel):
    month: str
    plate_of_month: int


class ItemOfMonthResponse(ItemOfMonthBase):
    class Config:
        from_attributes = True


# Admin
class AdminBase(BaseModel):
    username: str


class AdminCreate(AdminBase):
    password: str  # Password is only required during creation


class AdminResponse(AdminBase):
    admin_id: int

    class Config:
        from_attributes = True


# Payment
class PaymentBase(BaseModel):
    payment_method: str
    payment_status: str
    transaction_id: str


class PaymentCreate(PaymentBase):
    pass  # No additional fields


class PaymentResponse(PaymentBase):
    payment_id: int

    class Config:
        from_attributes = True


# PromoCode
class PromoCodeBase(BaseModel):
    discount: int
    valid_from: date
    valid_to: date


class PromoCodeCreate(PromoCodeBase):
    pass  # No additional fields


class PromoCodeResponse(PromoCodeBase):
    code: str

    class Config:
        from_attributes = True


# #Create user or sign up backend
# dependency injection try to create a database connection whether request is succeful or not close database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: db_dependency):
    # Check if the username already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username unavailable")

    # Hash the user's password before storing it
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    # Proceed to create the user with the hashed password
    db_user = models.User(
        username=user.username,
        password=hashed_password.decode("utf-8"),  # Decode to store as a string
        phone_number=user.phone_number,
        address=user.address,
    )
    db.add(db_user)
    db.commit()
    return {"message": f"User '{user.username}' created successfully"}


# #login backend:
# Pydantic model for login request
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login/")
async def login(user: LoginRequest, db: Session = Depends(get_db)):
    # Query the database for the user
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    # If user does not exist or password does not match
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Login successful
    return {"message": f"Welcome, {db_user.username}!"}





class FoodItemCreate(BaseModel):
    name: str
    price: int
    description: str
    category_id: int
    price_to_make: int
    photo: str

@app.post("/fooditems/", status_code=status.HTTP_201_CREATED)
async def create_food_item(food_item: FoodItemCreate, db: Session = Depends(get_db)):
    
        # Check if the food item name already exists
        existing_food_item = db.query(models.FoodItem).filter(models.FoodItem.name == food_item.name).first()
        if existing_food_item:
            raise HTTPException(status_code=400, detail="A food item with this name already exists.")

        # Create a new FoodItem instance
        db_food_item = models.FoodItem(
            name=food_item.name,
            price=food_item.price,
            description=food_item.description,
            category_id=food_item.category_id,
            price_to_make=food_item.price_to_make,
            photo=food_item.photo
        )

        db.add(db_food_item)
        db.commit()
        db.refresh(db_food_item)

        return {
            "food_id": db_food_item.food_id,
            "name": db_food_item.name,
            "price": db_food_item.price,
            "description": db_food_item.description,
            "category_id": db_food_item.category_id,
            "price_to_make": db_food_item.price_to_make,
            "photo": db_food_item.photo,
        }



#getting all fooditems from the database to show them for the admin

class FoodItemResponse(BaseModel):
    food_id: int
    name: str
    price: int
    description: str
    category_id: int
    price_to_make: int
    photo: str

@app.get("/fooditems/", response_model=List[FoodItemResponse])
def get_all_food_items(db: Session = Depends(get_db)):
    # Query all food items from the database
    food_items = db.query(models.FoodItem).all()
    return food_items


@app.delete("/fooditems/{food_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_food_item(food_id: int, db: Session = Depends(get_db)):
    # Retrieve the food item from the database
    food_item = db.query(models.FoodItem).filter(models.FoodItem.food_id == food_id).first()

    # If the food item does not exist, raise a 404 error
    if not food_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Food item with ID {food_id} not found."
        )

    # Remove the food item from the database
    db.delete(food_item)
    db.commit()

    return {"message": f"Food item with ID {food_id} has been deleted successfully"}



#change the payment status of an order:
class OrderStatusUpdate(BaseModel):
    status: str

@app.put("/orders/{order_id}/status", status_code=status.HTTP_200_OK)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    # Retrieve the order from the database
    order = db.query(models.Orders).filter(models.Orders.order_id == order_id).first()

    # If the order does not exist, raise a 404 error
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found."
        )

    # Update the status of the order
    order.status = status_update.status
    db.commit()  # Persist the changes in the database
    db.refresh(order)  # Refresh the order instance

    return {"message": f"Order {order_id} status updated to '{status_update.status}'"}
    
# add promocode
#create promocode
class PromoCodeCreate(BaseModel):
    code: str
    discount: int
    valid_from: date
    valid_to: date

@app.post("/promocodes/", status_code=status.HTTP_201_CREATED)
def create_promo_code(promo_code: PromoCodeCreate, db: Session = Depends(get_db)):
    # Check if a promo code with the same code already exists
    existing_promo = db.query(models.PromoCode).filter(models.PromoCode.code == promo_code.code).first()
    if existing_promo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Promo code '{promo_code.code}' already exists."
        )

    # Create a new PromoCode instance
    db_promo = models.PromoCode(
        code=promo_code.code,
        discount=promo_code.discount,
        valid_from=promo_code.valid_from,
        valid_to=promo_code.valid_to
    )

    # Add and commit to the database
    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)

    return {"message": f"Promo code '{promo_code.code}' created successfully"}

# @app.post("/additem", response_model=FoodItemCreate, status_code=status.HTTP_201_CREATED)
# def create_food_item(
#     item: FoodItemCreate, 
#     db: Session = Depends(get_db), 
# ):
#     # Check if a food item with the same name already exists
#     existing_item = db.query(models.FoodItem).filter(models.FoodItem.name == item.name).first()
#     if existing_item:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="A food item with this name already exists."
#         )
    
#     # Create a new FoodItem instance
#     new_food_item = models.FoodItem(
#         name=item.name,
#         price=item.price,
#         description=item.description,
#         category_id=item.category_id,
#         price_to_make=item.price_to_make,
#         photo=item.photo
#     )

#     db.add(new_food_item)
#     db.commit()
#     db.refresh(new_food_item)

#     # Return the newly created item
#     return item








# from fastapi import FastAPI, HTTPException, Depends, status
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from database import SessionLocal, engine
# import models
# import bcrypt
# from pydantic import BaseModel
# from typing import Annotated

# app = FastAPI()

# # CORS configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],  # React frontend's URL
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods
#     allow_headers=["*"],  # Allow all headers
# )

# # Create database tables
# models.Base.metadata.create_all(bind=engine)

# # Dependency to get a database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session, Depends(get_db)]

# # Pydantic models
# class LoginRequest(BaseModel):
#     username: str
#     password: str

# class UserCreate(BaseModel):
#     username: str
#     password: str
#     phone_number: str
#     address: str

# # Create user (signup endpoint)
# @app.post("/users/", status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserCreate, db: db_dependency):
#     # Check if the username already exists
#     existing_user = db.query(models.User).filter(models.User.username == user.username).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username unavailable")

#     # Hash the user's password
#     hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

#     # Create the user
#     db_user = models.User(
#         username=user.username,
#         password=hashed_password.decode("utf-8"),
#         phone_number=user.phone_number,
#         address=user.address,
#     )
#     db.add(db_user)
#     db.commit()
#     return {"message": f"User '{user.username}' created successfully"}

# # Login (authentication endpoint)
# @app.post("/login/")
# async def login(user: LoginRequest, db: db_dependency):
#     # Query the database for the user
#     db_user = db.query(models.User).filter(models.User.username == user.username).first()

#     # Verify password
#     if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
#         raise HTTPException(status_code=401, detail="Invalid username or password")

#     return {"message": f"Welcome, {db_user.username}!"}
