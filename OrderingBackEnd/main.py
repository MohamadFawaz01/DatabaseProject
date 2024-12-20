from multiprocessing import get_context
import bcrypt
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, List, Optional
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
    allow_origins=["http://localhost:5173",
                   "http://localhost:5174"],  # Frontend URL
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


#delete food item from the database
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


# Pydantic model for login request
class AdminLoginRequest(BaseModel):
    username: str
    password: str

# Pydantic model for login response
class AdminLoginResponse(BaseModel):
    success: bool
    message: str
    token: str | None = None


@app.post("/api/admin/login", response_model=AdminLoginResponse, status_code=status.HTTP_200_OK)
def login_admin(login_request: AdminLoginRequest, db: Session = Depends(get_db)):
    """
    Admin login that retrieves credentials from the database without password hashing.
    """
    # Query the database for the user
    admin_user = db.query(models.Admin).filter(models.Admin.username == login_request.username).first()
    
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    # Compare passwords directly (plaintext)
    if login_request.password != admin_user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    # Generate token (replace with proper JWT token generation)
    token = "dummy-token-for-now"

    return AdminLoginResponse(success=True, message="Login successful", token=token)

