import React, { useContext, useState } from "react";
import "./Cart.css";
import { StoreContext } from "../../context/StoreContext";
import { useNavigate } from "react-router-dom";

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

  const [promoCode, setPromoCode] = useState("");
  const [discount, setDiscount] = useState(0);
  const [promoMessage, setPromoMessage] = useState("");
  const totalCartAmount = getTotalCartAmount();

  const hasItemsInCart = Object.values(cartItems).some(
    (quantity) => quantity > 0
  );

  const navigate = useNavigate(); // Initialize navigate function

  const handlePromoCodeChange = (event) => {
    setPromoCode(event.target.value);
  };

  const handleApplyPromoCode = async () => {
    try {
      const response = await fetch(`${url}/promocode/validate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ code: promoCode }),
      });

      const data = await response.json();

      if (response.ok && data.success) {
        setDiscount(data.discount);
        setPromoMessage(`Promo code applied! ${data.discount}% off.`);
      } else {
        setDiscount(0);
        setPromoMessage(data.message || "Invalid promo code.");
      }
    } catch (error) {
      setPromoMessage("Error applying promo code. Please try again.");
    }
  };

  const calculateDiscountedTotal = () => {
    const discountedAmount = (totalCartAmount * discount) / 100;
    return (
      totalCartAmount -
      discountedAmount +
      (totalCartAmount > 0 ? 2 : 0)
    ).toFixed(2);
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
            <div className="promo-code-section">
              <h3>Promo Code</h3>
              <input
                type="text"
                placeholder="Enter promo code"
                className="promo-code-input"
                value={promoCode}
                onChange={handlePromoCodeChange}
              />
              <button onClick={handleApplyPromoCode}>Apply</button>
              {promoMessage && <p className="promo-message">{promoMessage}</p>}
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
              <b>${calculateDiscountedTotal()}</b>
            </div>
          </div>

          {totalCartAmount === 0 ? (
            <button>Empty basket</button>
          ) : (
            <button onClick={() => navigate("/myorders")}>
              Proceed to checkout
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Cart;
