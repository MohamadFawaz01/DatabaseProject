import React, { useContext, useState } from "react";
import "./Cart.css";
import { StoreContext } from "../../context/StoreContext";

const Cart = () => {
  const {
    cartItems,
    food_list,
    removeFromCart,
    getTotalCartAmount,
    addToCart,
    url,
    token,
  } = useContext(StoreContext);

  const [foodInfo, setFoodInfoState] = useState("");
  const totalCartAmount = getTotalCartAmount();

  const hasItemsInCart = Object.values(cartItems).some(
    (quantity) => quantity > 0
  );

  const handleFoodInfoChange = (event) => {
    setFoodInfoState(event.target.value);
  };

  return (
    <div className="cart">
      <div className="cart-items">
        <div className="cart-items-title">
          <p>Image</p>
          <p>Title</p>
          <p>Price</p>
          <p>Quantity</p>
          <p>Total</p>
          <p>Actions</p>
        </div>
        <br />
        <hr />

        {food_list.map((item, index) => {
          if (cartItems[item.food_id] > 0) {
            // Construct image URL in the same manner as FoodItem
            const imageUrl = `http://localhost:8000/static/${item.photo}`;

            return (
              <div key={index} className="cart-items-item">
                <img
                  src={imageUrl}
                  alt={item.name}
                  className="cart-item-image"
                />
                <p>{item.name}</p>
                <p>${item.price.toFixed(2)}</p>
                <p>{cartItems[item.food_id]}</p>
                <p>${(item.price * cartItems[item.food_id]).toFixed(2)}</p>
                <div className="actions">
                  <span
                    onClick={() => removeFromCart(item.food_id)}
                    className="cross"
                  >
                    x
                  </span>
                </div>
              </div>
            );
          }
          return null;
        })}

        {hasItemsInCart && (
          <>
            <div className="title">
              <h3>Food Instructions</h3>
              <input
                type="text"
                placeholder="Food instructions"
                className="food-info-input"
                value={foodInfo}
                onChange={handleFoodInfoChange}
              />
            </div>
            <hr />
          </>
        )}
      </div>

      <div className="cart-bottom">
        <div className="cart-total">
          <h2>Cart total</h2>
          <div>
            <div className="cart-total-details">
              <p>Subtotal</p>
              <p>${totalCartAmount.toFixed(2)}</p>
            </div>
            <hr />
            <div className="cart-total-details">
              <p>Delivery Fee</p>
              <p>${totalCartAmount === 0 ? 0 : 2}</p>
            </div>
            <hr />
            <div className="cart-total-details">
              <b>Total</b>
              <b>
                ${totalCartAmount === 0 ? 0 : (totalCartAmount + 2).toFixed(2)}
              </b>
            </div>
          </div>

          {totalCartAmount === 0 ? (
            <button>Empty basket</button>
          ) : (
            <button>Proceed to checkout</button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Cart;
