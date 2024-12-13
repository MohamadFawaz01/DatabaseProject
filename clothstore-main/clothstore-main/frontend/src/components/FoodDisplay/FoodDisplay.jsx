import React, { useContext } from 'react';
import './FoodDisplay.css';
import { StoreContext } from '../../context/StoreContext';
import FoodItem from '../FoodItem/FoodItem';

const FoodDisplay = ({ category }) => {
  const { food_list } = useContext(StoreContext);

  // Group food items by category
  const groupedFoodList = food_list.reduce((acc, item) => {
    (acc[item.category] = acc[item.category] || []).push(item);
    return acc;
  }, {});

  const renderCategory = (category) => (
    <div key={category}>
      <h2>{category}:</h2>
      <div className='food-display-list'>
        {groupedFoodList[category].map((item) => (
          <FoodItem
            key={item._id}
            id={item._id}
            name={item.name}
            description={item.description}
            price={item.price}
            image={item.image}
          />
        ))}
      </div>
      <hr />
    </div>
  );

  return (
    <div className='food-display' id='food-display'>
      {category === 'All'
        ? Object.keys(groupedFoodList).map(renderCategory)
        : renderCategory(category)}
    </div>
  );
};

export default FoodDisplay;
