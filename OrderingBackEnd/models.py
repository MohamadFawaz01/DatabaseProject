from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class FoodItem(Base):
    __tablename__ = 'food_items'

    food_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)  # Specify length
    price = Column(Integer)
    description = Column(String(200))
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    price_to_make = Column(Integer)
    photo = Column(String(255))

    category = relationship("Category", back_populates="food_items")
    feedbacks = relationship("Feedback", back_populates="food_item")
    order_details = relationship("OrderDetails", back_populates="food_item")


class Feedback(Base):
    __tablename__ = 'feedbacks'

    feedback_id = Column(Integer, primary_key=True)
    stars = Column(Integer)
    user_id = Column(BigInteger, ForeignKey('users.user_id'))
    food_id = Column(Integer, ForeignKey('food_items.food_id'))
    comment = Column(String(500))

    user = relationship("User", back_populates="feedbacks")
    food_item = relationship("FoodItem", back_populates="feedbacks")


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(100), unique=True)
    phone_number = Column(String(8))
    password = Column(String(255), nullable=False)
    address = Column(String(255))

    feedbacks = relationship("Feedback", back_populates="user")
    orders = relationship("Orders", back_populates="user")


class Orders(Base):
    __tablename__ = 'orders'

    order_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id'))
    promo_code = Column(String(50), ForeignKey('promo_codes.code'))
    total_food_price = Column(Integer)
    delivery_fee = Column(Integer)
    status = Column(String(50))
    order_date = Column(Date)
    payment_id = Column(BigInteger, ForeignKey('payments.payment_id'))

    user = relationship("User", back_populates="orders")
    payment = relationship("Payment", back_populates="orders")
    order_details = relationship("OrderDetails", back_populates="order")


class OrderDetails(Base):
    __tablename__ = 'order_details'

    order_id = Column(BigInteger, ForeignKey('orders.order_id'), primary_key=True)
    food_id = Column(Integer, ForeignKey('food_items.food_id'), primary_key=True)
    quantity = Column(Integer)

    order = relationship("Orders", back_populates="order_details")
    food_item = relationship("FoodItem", back_populates="order_details")


class Stats(Base):
    __tablename__ = 'stats'

    stats_id = Column(Integer, primary_key=True)
    total_income = Column(Integer)
    plate_of_the_day = Column(Integer, ForeignKey('food_items.food_id'))
    net_income = Column(Integer)

    plate_of_the_day_item = relationship("FoodItem")


class ItemOfMonth(Base):
    __tablename__ = 'item_of_month'

    month = Column(String(20), primary_key=True)
    plate_of_month = Column(Integer, ForeignKey('food_items.food_id'))

    plate_of_month_item = relationship("FoodItem")


class Admin(Base):
    __tablename__ = 'admins'

    admin_id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(255))


class Payment(Base):
    __tablename__ = 'payments'

    payment_id = Column(BigInteger, primary_key=True)
    payment_method = Column(String(50))
    payment_status = Column(String(50))
    transaction_id = Column(String(100))

    orders = relationship("Orders", back_populates="payment")


class PromoCode(Base):
    __tablename__ = 'promo_codes'

    code = Column(String(50), primary_key=True)
    discount = Column(Integer)
    valid_from = Column(Date)
    valid_to = Column(Date)


class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(100))
    addons = Column(String(200))
    removable_items = Column(String(200))

    food_items = relationship("FoodItem", back_populates="category")




