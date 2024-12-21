from multiprocessing import get_context
import os
import bcrypt
from fastapi import FastAPI, File, Form, HTTPException, Depends, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated, List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
import models
from database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles

# Create the database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"),name="static")

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



# add food item in the menu 
class FoodItemCreate(BaseModel):
    name: str
    price: int
    description: str
    category_name: str
    price_to_make: int
    photo: str

# Endpoint to create a food item
@app.post("/fooditems/", status_code=status.HTTP_201_CREATED)
async def create_food_item(
    name: str = Form(...),
    price: int = Form(...),
    description: str = Form(...),
    category_name: str = Form(...),
    price_to_make: int = Form(...),
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Check if the food item name already exists
    existing_food_item = db.query(models.FoodItem).filter(models.FoodItem.name == name).first()
    if existing_food_item:
        raise HTTPException(status_code=400, detail="A food item with this name already exists.")
    
    # Validate and save the uploaded file
    file_extension = os.path.splitext(photo.filename)[1].lower()
    if file_extension not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, JPEG, and PNG are allowed.")
    
    # Sanitize the file name
    sanitized_name = name.replace(" ", "_")
    file_name = f"{sanitized_name}.jpg"
    file_path = f"static/images/{file_name}"
    
    with open(file_path, "wb") as file:
        content = await photo.read()
        file.write(content)
    
    # Create a new FoodItem instance
    db_food_item = models.FoodItem(
        name=name,
        price=price,
        description=description,
        category_name=category_name,
        price_to_make=price_to_make,
        photo=f"/images/{file_name}",  # Save only the relative path
    )
    
    db.add(db_food_item)
    db.commit()
    db.refresh(db_food_item)
    
    return {
        "food_id": db_food_item.food_id,
        "name": db_food_item.name,
        "price": db_food_item.price,
        "description": db_food_item.description,
        "category_name": db_food_item.category_name,
        "price_to_make": db_food_item.price_to_make,
        "photo": db_food_item.photo,
    }


#getting all fooditems from the database to show them for the admin

class FoodItemResponse(BaseModel):
    food_id: int
    name: str
    price: int
    description: str
    category_name: str
    price_to_make: int
    photo: str

    class Config:
        orm_mode = True

@app.get("/api/food/list", response_model=dict)
def get_all_food_items(db: Session = Depends(get_db)):
    food_items = db.query(models.FoodItem).all()
    food_items_response = [
        FoodItemResponse(
            food_id=item.food_id,
            name=item.name,
            price=item.price,
            description=item.description,
            category_name=item.category_name or "Unknown",  # Default to "Unknown" if None
            price_to_make=item.price_to_make,
            photo=item.photo,
        )
        for item in food_items
    ]
    return {"success": True, "data": food_items_response}



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

class AddToCartRequest(BaseModel):
    food_id: int
    quantity: int
    user_id: int

@app.post("/cart/add", status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    cart_item: AddToCartRequest,
    db: Session = Depends(get_db),
):
    user_id = cart_item.user_id  # Extract user_id from request body

    # Fetch the user's active order (status: "pending")
    order = db.query(models.Orders).filter(
        models.Orders.user_id == user_id,
        models.Orders.status == "pending",
    ).first()

    # If no active order exists, create one
    if not order:
        order = models.Orders(
            user_id=user_id,
            status="pending",
            order_date=date.today(),
            total_food_price=0,
            delivery_fee=5000,  # Example delivery fee
        )
        db.add(order)
        db.commit()
        db.refresh(order)

    # Check if the food item is already in the order
    order_detail = db.query(models.OrderDetails).filter(
        models.OrderDetails.order_id == order.order_id,
        models.OrderDetails.food_id == cart_item.food_id,
    ).first()

    if order_detail:
        # Update the quantity if the item is already in the cart
        order_detail.quantity += cart_item.quantity
    else:
        # Add the food item to the order
        new_order_detail = models.OrderDetails(
            order_id=order.order_id,
            food_id=cart_item.food_id,
            quantity=cart_item.quantity,
        )
        db.add(new_order_detail)

    # Update the total food price
    food_item = db.query(models.FoodItem).filter(models.FoodItem.food_id == cart_item.food_id).first()
    if not food_item:
        raise HTTPException(status_code=404, detail="Food item not found")

    order.total_food_price += food_item.price * cart_item.quantity

    db.commit()
    return {"message": "Item added to cart successfully"}

# Define the request model for removing a cart item
class RemoveFromCartRequest(BaseModel):
    food_id: int
    user_id: int

@app.delete("/cart/remove", status_code=status.HTTP_200_OK)
async def remove_from_cart(
    cart_item: RemoveFromCartRequest,
    db: Session = Depends(get_db),
):
    # Fetch the user's active order (status: "pending")
    order = db.query(models.Orders).filter(
        models.Orders.user_id == cart_item.user_id,
        models.Orders.status == "pending",
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active order found."
        )

    # Check if the food item exists in the order
    order_detail = db.query(models.OrderDetails).filter(
        models.OrderDetails.order_id == order.order_id,
        models.OrderDetails.food_id == cart_item.food_id,
    ).first()

    if not order_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food item not found in the cart."
        )

    # Update the total food price
    food_item = db.query(models.FoodItem).filter(models.FoodItem.food_id == cart_item.food_id).first()
    if not food_item:
        raise HTTPException(status_code=404, detail="Food item not found")

    # Decrease the quantity by 1
    order_detail.quantity -= 1
    order.total_food_price -= food_item.price

    # If the quantity reaches zero, remove the item from the order details
    if order_detail.quantity <= 0:
        db.delete(order_detail)

    # If the order is now empty, delete the order
    remaining_items = db.query(models.OrderDetails).filter(
        models.OrderDetails.order_id == order.order_id
    ).count()

    if remaining_items == 0:
        db.delete(order)

    db.commit()
    return {"message": "Item quantity reduced in cart successfully"}

@app.get("/cart", status_code=status.HTTP_200_OK)
async def view_cart(
    user_id: int,  # Ideally passed in via an authenticated session
    db: Session = Depends(get_db),
):
    # Fetch the user's active order
    order = db.query(models.Orders).filter(
        models.Orders.user_id == user_id,
        models.Orders.status == "pending",
    ).first()

    if not order:
        return {"message": "Your cart is empty", "items": []}

    # Fetch all items in the order
    order_details = db.query(models.OrderDetails).filter(
        models.OrderDetails.order_id == order.order_id
    ).all()

    cart_items = []
    for detail in order_details:
        food_item = db.query(models.FoodItem).filter(models.FoodItem.food_id == detail.food_id).first()
        cart_items.append({
            "food_id": detail.food_id,
            "name": food_item.name,
            "quantity": detail.quantity,
            "price_per_item": food_item.price,
            "total_price": food_item.price * detail.quantity,
        })

    return {
        "order_id": order.order_id,
        "items": cart_items,
        "total_food_price": order.total_food_price,
        "delivery_fee": order.delivery_fee,
        "grand_total": order.total_food_price + order.delivery_fee,
    }

class OrderHistoryResponse(BaseModel):
    order_id: int
    order_date: date
    total_food_price: int
    delivery_fee: int
    status: str
    grand_total: int

    class Config:
        orm_mode = True

@app.get("/orders/history", response_model=List[OrderHistoryResponse])
async def get_order_history(user_id: int, db: Session = Depends(get_db)):
    # Fetch the user's orders, sorted by order_date in descending order
    orders = db.query(models.Orders).filter(
        models.Orders.user_id == user_id
    ).order_by(models.Orders.order_date.desc()).all()

    if not orders:
        return {"message": "No order history found", "orders": []}

    # Prepare response with calculated grand_total for each order
    order_history = []
    for order in orders:
        order_history.append({
            "order_id": order.order_id,
            "order_date": order.order_date,
            "total_food_price": order.total_food_price,
            "delivery_fee": order.delivery_fee,
            "status": order.status,
            "grand_total": order.total_food_price + order.delivery_fee,
        })

    return order_history

@app.post("/orders/complete", status_code=status.HTTP_200_OK)
async def complete_order(
    user_id: int,
    db: Session = Depends(get_db),
):
    # Debug: Print user_id and database state
    print(f"Completing order for user_id: {user_id}")
    
    # Check for active order
    order = db.query(models.Orders).filter(
        models.Orders.user_id == user_id,
        models.Orders.status == "pending"
    ).first()

    if not order:
        print("No active order found for user_id:", user_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active order found."
        )

    # Update order status
    order.status = "completed"
    db.commit()

    # Debug: Confirmation message for order completion
    print(f"Order {order.order_id} marked as completed.")
    return {"message": f"Order {order.order_id} has been successfully completed."}