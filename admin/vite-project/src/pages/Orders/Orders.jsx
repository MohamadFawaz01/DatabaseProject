import React, { useState, useEffect } from "react";
import "./Orders.css";
import axios from "axios";
import { toast } from "react-toastify";

const Orders = ({ url }) => {
  const [orders, setOrders] = useState([]);

  // Fetch all orders from the backend
  const fetchOrders = async () => {
    try {
      const response = await axios.get(`${url}/orders/`);
      setOrders(response.data); // Assuming response is already the list of orders
    } catch (error) {
      toast.error("Error fetching orders");
      console.error(error);
    }
  };

  // Delete an order by ID
  const deleteOrder = async (orderId) => {
    try {
      const response = await axios.delete(`${url}/orders/${orderId}`); // DELETE request
      if (response.status === 204) {
        toast.success(`Order with ID ${orderId} has been deleted successfully`);
        await fetchOrders(); // Refresh the list after deletion
      } else {
        toast.error("Error deleting order");
      }
    } catch (error) {
      if (error.response && error.response.status === 404) {
        toast.error(`Order with ID ${orderId} not found`);
      } else {
        toast.error("Error deleting order");
      }
      console.error(error);
    }
  };

  // Fetch orders on component mount
  useEffect(() => {
    fetchOrders();
  }, []);

  return (
    <div className="orders-container">
      <div className="orders-title">
        <p>All Orders List</p>
      </div>
      <div className="orders-table">
        <div className="orders-table-header">
          <b>Order ID</b>
          <b>User ID</b>
          <b>Promo Code</b>
          <b>Total Price</b>
          <b>Delivery Fee</b>
          <b>Status</b>
          <b>Order Date</b>
          <b>Action</b>
        </div>
        {orders.map((order) => (
          <div key={order.order_id} className="orders-table-row">
            <p>{order.order_id}</p>
            <p>{order.user_id}</p>
            <p>{order.promo_code || "N/A"}</p>
            <p>${order.total_food_price}</p>
            <p>${order.delivery_fee}</p>
            <p>{order.status}</p>
            <p>{new Date(order.order_date).toLocaleDateString()}</p>
            <p
              onClick={() => deleteOrder(order.order_id)} // Trigger delete on click
              className="delete-button"
            >
              Delete
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Orders;
