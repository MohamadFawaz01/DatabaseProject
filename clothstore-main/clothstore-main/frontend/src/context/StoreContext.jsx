import React, { createContext, useState, useEffect } from "react";

export const StoreContext = createContext(null);

const StoreContextProvider = (props) => {
  const [cartItems, setCartItems] = useState({});
  const [foodList, setFoodList] = useState([]);
  const [token, setToken] = useState("");
  const url = "http://localhost:8000"; // FastAPI server URL

  useEffect(() => {
    const fetchFoodList = async () => {
      try {
        const response = await fetch(`${url}/api/food/list`);
        const result = await response.json();
        if (result.success) {
          setFoodList(result.data);
        } else {
          console.error("Failed to fetch food items");
        }
      } catch (error) {
        console.error("Error fetching food items:", error);
      }
    };

    fetchFoodList();
  }, [url]);

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  const addToCart = async (food_id, quantity = 1) => {
    try {
      const response = await fetch(`${url}/cart/add`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // Include token if required
        },
        body: JSON.stringify({ food_id, quantity, user_id: 1 }), // Add user_id to the body
      });
      const data = await response.json();
      if (response.ok) {
        setCartItems((prev) => ({
          ...prev,
          [food_id]: (prev[food_id] || 0) + quantity,
        }));
      } else {
        console.error("Error adding item to cart:", data);
        alert(data.detail || "Failed to add item to cart");
      }
    } catch (error) {
      console.error("Error in addToCart function:", error);
    }
  };

  const removeFromCart = async (food_id) => {
    try {
      const response = await fetch(`${url}/cart/remove`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`, // Include token if required
        },
        body: JSON.stringify({ food_id, user_id: 1 }), // Replace 1 with dynamic user_id if needed
      });

      const data = await response.json();

      if (response.ok) {
        setCartItems((prev) => {
          const newQuantity = (prev[food_id] || 0) - 1;
          const updatedCart = { ...prev };
          if (newQuantity > 0) {
            updatedCart[food_id] = newQuantity;
          } else {
            delete updatedCart[food_id];
          }
          return updatedCart;
        });
      } else {
        console.error("Error removing item from cart:", data);
        alert(data.detail || "Failed to remove item from cart");
      }
    } catch (error) {
      console.error("Error in removeFromCart function:", error);
    }
  };

  const getTotalCartAmount = () => {
    return Object.entries(cartItems).reduce((total, [itemId, quantity]) => {
      const item = foodList.find(
        (product) => product.food_id === parseInt(itemId)
      );
      return item ? total + item.price * quantity : total;
    }, 0);
  };

  const contextValue = {
    food_list: foodList,
    cartItems,
    addToCart,
    removeFromCart,
    getTotalCartAmount,
    token,
    setToken,
    url,
  };

  return (
    <StoreContext.Provider value={contextValue}>
      {props.children}
    </StoreContext.Provider>
  );
};

export default StoreContextProvider;
