import React, { useState } from "react";
import "./Add.css";
import { assets } from "../../assets/assets";
import axios from "axios";
import { toast } from "react-toastify";

const Add = ({ url }) => {
  const [data, setData] = useState({
    name: "",
    price: "",
    description: "",
    category_name: "Salad", // Default category value
    price_to_make: "",
  });
  const [image, setImage] = useState(null);

  // Handle form input changes
  const onChangeHandler = (e) => {
    const { name, value } = e.target;
    setData({ ...data, [name]: value });
  };

  // Handle form submission
  const onSubmitHandler = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append("name", data.name);
      formData.append("price", data.price);
      formData.append("description", data.description);
      formData.append("category_name", data.category_name);
      formData.append("price_to_make", data.price_to_make);
      formData.append("photo", image);

      const response = await axios.post(`${url}/fooditems/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      toast.success("Food item added successfully!");
      console.log(response.data);
    } catch (error) {
      console.error("Error:", error.response || error.message);
      if (error.response) {
        toast.error(
          `Error: ${error.response.data.detail || "Failed to add food item."}`
        );
      } else {
        toast.error("Failed to add food item. Please try again.");
      }
    }
  };

  return (
    <div className="add">
      <form className="flex-col" onSubmit={onSubmitHandler}>
        <div className="add-img-upload flex-col">
          <div className="titles">
            <p>Upload Image</p>
          </div>

          <label htmlFor="image">
            <img
              src={image ? URL.createObjectURL(image) : assets.upload_area}
              alt="Uploaded Preview"
            />
          </label>
          <input
            onChange={(e) => setImage(e.target.files[0])}
            type="file"
            id="image"
            hidden
            required
          />
        </div>
        <div className="add-product-name flex-col">
          <p>Product Name</p>
          <input
            onChange={onChangeHandler}
            value={data.name}
            type="text"
            name="name"
            placeholder="Enter product name"
            required
          />
        </div>
        <div className="add-product-description flex-col">
          <p>Product Description</p>
          <textarea
            onChange={onChangeHandler}
            value={data.description}
            name="description"
            rows="6"
            placeholder="Enter product description"
            required
          ></textarea>
        </div>
        <div className="add-category-price">
          <div className="add-category flex-col">
            <p>Product Category</p>
            <select
              onChange={onChangeHandler}
              name="category_name"
              value={data.category_name}
            >
              <option value="Salad">Salad</option>
              <option value="Appetizers">Appetizers</option>
              <option value="Pizza">Pizza</option>
              <option value="Pasta">Pasta</option>
              <option value="Burger">Burger</option>
              <option value="Sandwiches">Sandwiches</option>
              <option value="Platters">Platters</option>
              <option value="Kids corner">Kids Corner</option>
              <option value="Add ons">Add Ons</option>
              <option value="Drinks">Drinks</option>
              <option value="Shisha">Shisha</option>
            </select>
          </div>
          <div className="add-price flex-col">
            <p>Product Price</p>
            <input
              onChange={onChangeHandler}
              value={data.price}
              type="number"
              name="price"
              placeholder="Enter price"
              required
            />
          </div>
          <div className="add-price-to-make flex-col">
            <p>Price to Make</p>
            <input
              onChange={onChangeHandler}
              value={data.price_to_make}
              type="number"
              name="price_to_make"
              placeholder="Enter cost to make"
              required
            />
          </div>
        </div>
        <button type="submit" className="add-btn">
          ADD
        </button>
      </form>
    </div>
  );
};

export default Add;
