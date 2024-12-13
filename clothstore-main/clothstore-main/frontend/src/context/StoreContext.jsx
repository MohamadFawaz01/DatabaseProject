// StoreContext.jsx
import React, { createContext, useState, useEffect } from 'react';
import { food_list } from '../assets/assets';

export const StoreContext = createContext(null);

const getDefaultCart = () => {
  let cart = {};
  food_list.forEach((item) => {
    cart[item._id] = 0;
  });
  return cart;
};

const StoreContextProvider = (props) => {
  const [cartItems, setCartItems] = useState(getDefaultCart());
  const [foodInfo, setFoodInfo] = useState('');
  const [token, setToken] = useState('');

  const addToCart = (itemId) => {
    setCartItems((prev) => ({ ...prev, [itemId]: prev[itemId] + 1 }));
  };

  const removeFromCart = (itemId) => {
    setCartItems((prev) => {
      const newQuantity = prev[itemId] - 1;
      return { ...prev, [itemId]: newQuantity >= 0 ? newQuantity : 0 };
    });
  };

  const getTotalCartAmount = () => {
    let totalAmount = 0;
    for (const itemId in cartItems) {
      const item = food_list.find((product) => product._id === itemId);
      if (item) {
        totalAmount += item.price * cartItems[itemId];
      }
    }
    return totalAmount;
  };

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  const contextValue = {
    food_list,
    cartItems,
    addToCart,
    removeFromCart,
    getTotalCartAmount,
    token,
    setToken,
    foodInfo,
    setFoodInfo,
  };

  return (
    <StoreContext.Provider value={contextValue}>
      {props.children}
    </StoreContext.Provider>
  );
};

export default StoreContextProvider;
