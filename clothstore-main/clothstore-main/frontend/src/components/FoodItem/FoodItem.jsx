import React, { useContext } from "react";
import "./FoodItem.css";
import { StoreContext } from "../../context/StoreContext";
import { assets } from "../../assets/assets";

const FoodItem = ({ id, name, price, description, image }) => {
  const { cartItems, addToCart, removeFromCart } = useContext(StoreContext);
  const itemQuantity = cartItems[id];

  const imageUrl = `http://localhost:8000/static/${image}`;

  return (
    <div className="food-item">
      <div className="food-item-img-container">
        <img className="food-item-image" src={imageUrl} alt={name} />
        <div className="food-item-count">
          {/* Plus button for adding to cart */}
          <img
            onClick={() => addToCart(id)}
            src={assets.add_icon_white}
            alt="Add to cart"
            className="add-to-cart-button"
          />

          {/* Display the quantity and Remove button if item is in the cart */}
          {itemQuantity && (
            <div className="cart-item-quantity">
              <img
                onClick={() => removeFromCart(id)}
                src={assets.remove_icon_red}
                alt="Remove from cart"
                className="remove-from-cart-button"
              />
              <p>{itemQuantity}</p>
            </div>
          )}
        </div>
      </div>
      <div className="food-item-info">
        <p className="food-item-name">{name}</p>
        <p className="food-item-desc">{description}</p>
        <p className="food-item-price">${price.toFixed(2)}</p>
      </div>
    </div>
  );
};

export default FoodItem;
