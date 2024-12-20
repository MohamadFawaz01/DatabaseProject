import React, { useState } from "react";
import { toast } from "react-toastify";
import "./PromoCode.css"; // Optional: Add this for specific styles

const PromoCode = ({ url }) => {
  const [formData, setFormData] = useState({
    code: "",
    discount: "",
    valid_from: "",
    valid_to: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${url}/promocodes/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`, // Ensure your backend requires a token
        },
        body: JSON.stringify({
          ...formData,
          discount: parseInt(formData.discount, 10),
        }),
      });

      if (response.ok) {
        toast.success("Promo code created successfully!");
        setFormData({
          code: "",
          discount: "",
          valid_from: "",
          valid_to: "",
        });
      } else {
        const data = await response.json();
        toast.error(data.detail || "Failed to create promo code.");
      }
    } catch (error) {
      console.error("Error creating promo code:", error);
      toast.error("An error occurred. Please try again.");
    }
  };

  return (
    <div className="promo-code-page">
      <h2>Create Promo Code</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="code">Code:</label>
          <input
            type="text"
            id="code"
            name="code"
            value={formData.code}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="discount">Discount (%):</label>
          <input
            type="number"
            id="discount"
            name="discount"
            value={formData.discount}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="valid_from">Valid From:</label>
          <input
            type="date"
            id="valid_from"
            name="valid_from"
            value={formData.valid_from}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="valid_to">Valid To:</label>
          <input
            type="date"
            id="valid_to"
            name="valid_to"
            value={formData.valid_to}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" className="submit-button">Create Promo Code</button>
      </form>
    </div>
  );
};

export default PromoCode;
