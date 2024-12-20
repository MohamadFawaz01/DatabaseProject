import bcrypt
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
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

#delete order from database cancel order

@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    # Retrieve the order from the database
    order = db.query(models.Orders).filter(models.Orders.order_id == order_id).first()

    # If the order does not exist, raise a 404 error
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found."
        )

    # Delete the order from the database
    db.delete(order)
    db.commit()

    return {"message": f"Order with ID {order_id} has been deleted successfully"}



# list all the orders in the database
class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    promo_code: Optional[str]
    total_food_price: int
    delivery_fee: int
    status: str
    order_date: date
    payment_id: Optional[int]

    class Config:
        orm_mode = True  # Enable ORM-to-JSON conversion


@app.get("/orders/", response_model=List[OrderResponse])
def list_all_orders(db: Session = Depends(get_db)):
    # Query all orders from the database
    orders = db.query(models.Orders).all()
    return orders


# get the best seller item from the last 7 days based on the order details table data
@app.get("/best-seller/")
def get_best_seller(db: Session = Depends(get_db)):
    # Calculate the date 7 days ago
    seven_days_ago = datetime.now().date() - timedelta(days=7)

    # Query to get the total quantity of each food item sold in the last 7 days
    best_seller_query = (
        db.query(
            models.OrderDetails.food_id,
            func.sum(models.OrderDetails.quantity).label("total_quantity")
        )
        .join(models.Orders, models.OrderDetails.order_id == models.Orders.order_id)
        .filter(models.Orders.order_date >= seven_days_ago)  # Filter by last 7 days
        .group_by(models.OrderDetails.food_id)  # Group by food_id
        .order_by(func.sum(models.OrderDetails.quantity).desc())  # Sort by total_quantity
        .first()  # Get the top result
    )

    # If no items were sold in the last 7 days
    if not best_seller_query:
        raise HTTPException(
            status_code=404, detail="No items sold in the last 7 days."
        )

    # Extract the best seller information
    food_id, total_quantity = best_seller_query

    # Query to get the food item details
    food_item = db.query(models.FoodItem).filter(models.FoodItem.food_id == food_id).first()
    if not food_item:
        raise HTTPException(
            status_code=404, detail=f"Food item with ID {food_id} not found."
        )

    # Return the best-seller details
    return {
        "food_id": food_id,
        "name": food_item.name,
        "total_quantity": total_quantity,
        "description": food_item.description,
        "price": food_item.price,
        "photo": food_item.photo,
    }


@app.post("/stats/calculate-daily-net-income/", status_code=201)
def calculate_daily_net_income(db: Session = Depends(get_db)):
    # Get today's date
    today = date.today()

    # Query to calculate total income (sum of price * quantity)
    total_income_query = (
        db.query(func.sum(models.FoodItem.price * models.OrderDetails.quantity))
        .join(models.OrderDetails, models.FoodItem.food_id == models.OrderDetails.food_id)
        .join(models.Orders, models.OrderDetails.order_id == models.Orders.order_id)
        .filter(models.Orders.order_date == today)  # Filter by today's date
        .scalar()
    )
    total_income = total_income_query or 0  # Handle null values

    # Query to calculate total cost (sum of price_to_make * quantity)
    total_cost_query = (
        db.query(func.sum(models.FoodItem.price_to_make * models.OrderDetails.quantity))
        .join(models.OrderDetails, models.FoodItem.food_id == models.OrderDetails.food_id)
        .join(models.Orders, models.OrderDetails.order_id == models.Orders.order_id)
        .filter(models.Orders.order_date == today)  # Filter by today's date
        .scalar()
    )
    total_cost = total_cost_query or 0  # Handle null values

    # Calculate net income
    net_income = total_income - total_cost

    # Query to determine the plate of the day (most ordered food item)
    plate_of_the_day_query = (
        db.query(
            models.OrderDetails.food_id,
            func.sum(models.OrderDetails.quantity).label("total_quantity")
        )
        .join(models.Orders, models.OrderDetails.order_id == models.Orders.order_id)
        .filter(models.Orders.order_date == today)  # Filter by today's date
        .group_by(models.OrderDetails.food_id)  # Group by food_id
        .order_by(func.sum(models.OrderDetails.quantity).desc())  # Sort by total_quantity
        .first()  # Get the top result
    )

    plate_of_the_day = plate_of_the_day_query[0] if plate_of_the_day_query else None

    # Create a new Stats record
    stats_entry = models.Stats(
        total_income=total_income,
        net_income=net_income,
        plate_of_the_day=plate_of_the_day
    )

    # Add and commit the new stats entry
    db.add(stats_entry)
    db.commit()
    db.refresh(stats_entry)

    return {
        "message": "Daily stats calculated and stored successfully.",
        "stats": {
            "total_income": total_income,
            "net_income": net_income,
            "plate_of_the_day": plate_of_the_day
        }
    }


