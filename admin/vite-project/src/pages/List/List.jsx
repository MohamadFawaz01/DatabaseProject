import React, { useState, useEffect } from "react";
import "./List.css";
import axios from "axios";
import { toast } from "react-toastify";

const List = ({ url }) => {
  const [list, setList] = useState([]);

  // Fetch the list of food items from the backend
  const fetchList = async () => {
    try {
      const response = await axios.get(`${url}/api/food/list`);
      if (response.data.success) {
        setList(response.data.data);
      } else {
        toast.error("Error fetching list");
      }
    } catch (error) {
      toast.error("Error fetching list");
      console.error(error);
    }
  };

  // Delete a food item using its ID
  const removeFood = async (foodId) => {
    try {
      const response = await axios.delete(`${url}/fooditems/${foodId}`); // DELETE request
      if (response.status === 204) {
        // Check for HTTP 204 No Content
        toast.success(
          `Food item with ID ${foodId} has been deleted successfully`
        );
        await fetchList(); // Refresh the list after deletion
      } else {
        toast.error("Error removing item");
      }
    } catch (error) {
      if (error.response && error.response.status === 404) {
        toast.error(`Food item with ID ${foodId} not found`);
      } else {
        toast.error("Error removing item");
      }
      console.error(error);
    }
  };

  // Fetch the list on component mount
  useEffect(() => {
    fetchList();
  }, []);

  return (
    <div className="list-add-flex-col">
      <div className="title">
        <p>All Foods List</p>
      </div>
      <div className="list-table">
        <div className="list-table-format title">
          <b>Image</b>
          <b>Name</b>
          <b>Category</b>
          <b>Price</b>
          <b>Action</b>
        </div>
        {list.map((item, index) => (
          <div key={index} className="list-table-format">
            <img src={`${url}/static${item.photo}`} alt={item.name} />
            <p>{item.name}</p>
            <p>{item.category_name}</p>
            <p>${item.price}</p>
            <p
              onClick={() => removeFood(item.food_id)} // Trigger delete on click
              className="cursor"
            >
              x
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default List;
