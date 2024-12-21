import React, { useContext } from "react";
import "./FoodDisplay.css";
import { StoreContext } from "../../context/StoreContext";
import FoodItem from "../FoodItem/FoodItem";

const FoodDisplay = ({ category }) => {
  const { food_list } = useContext(StoreContext);

  // Group food items by category
  const groupedFoodList = food_list.reduce((acc, item) => {
    (acc[item.category_name] = acc[item.category_name] || []).push(item);
    return acc;
  }, {});

  const renderCategory = (category) => (
    <div key={category}>
      <h2>{category}:</h2>
      <div className="food-display-list">
        {groupedFoodList[category].map((item) => (
          <FoodItem
            key={item.food_id}
            id={item.food_id}
            name={item.name}
            description={item.description}
            price={item.price}
            image={item.photo} // Ensure 'photo' is the correct field from the API
          />
        ))}
      </div>
      <hr />
    </div>
  );

  return (
    <div className="food-display" id="food-display">
      {category === "All"
        ? Object.keys(groupedFoodList).map(renderCategory)
        : renderCategory(category)}
    </div>
  );
};

export default FoodDisplay;
