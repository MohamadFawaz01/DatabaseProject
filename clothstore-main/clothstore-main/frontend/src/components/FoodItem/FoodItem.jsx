import React, { useContext } from 'react';
import './FoodItem.css';
import { StoreContext } from '../../context/StoreContext';
import { assets } from '../../assets/assets';

const FoodItem = ({ id, name, price, description, image }) => {
    const { cartItems, addToCart, removeFromCart } = useContext(StoreContext);
    const itemQuantity = cartItems[id];

    return (
        <div className='food-item'>
            <div className="food-item-img-container">
                <img className='food-item-image' src={image} alt={name} />
                {!itemQuantity
                    ? <img className='add' onClick={() => addToCart(id)} src={assets.add_icon_white} alt="Add to cart" />
                    : <div className='food-item-count'>
                        <img onClick={() => removeFromCart(id)} src={assets.remove_icon_red} alt="Remove from cart" />
                        <p>{itemQuantity}</p>
                        <img onClick={() => addToCart(id)} src={assets.add_icon_green} alt="Add more to cart" />
                    </div>
                }
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
