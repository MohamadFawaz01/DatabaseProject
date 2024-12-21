import React, { useState, useContext, useEffect } from "react";
import "./MyOrders.css";
import { StoreContext } from "../../context/StoreContext";
import axios from "axios";
import { assets } from "../../assets/assets";

const MyOrders = () => {
  // State to store orders data fetched from the server
  const [data, setData] = useState([]);

  // Access the `url` and `token` from context
  const { url, token } = useContext(StoreContext);

  // Function to fetch user orders from the server
  const fetchOrders = async () => {
    try {
      // Send a POST request to fetch orders, passing the user's token in headers
      const response = await axios.post(
        `${url}/api/order/userorders`,
        {},
        { headers: { token } }
      );
      // Update the state with the fetched data
      setData(response.data.data);
      console.log(response.data.data); // Log data for debugging purposes
    } catch (error) {
      console.error("Error fetching orders:", error); // Log any errors that occur during the request
    }
  };

  // useEffect hook to fetch orders when the component mounts or when the token changes
  useEffect(() => {
    if (token) {
      fetchOrders(); // Call the fetchOrders function if a valid token is available
    }
  }, [token]); // Dependency array ensures the effect runs when `token` changes

  return (
    <div className="my-orders">
      {/* Page title */}
      <h2>My Orders</h2>
      <div className="container">
        {/* Reverse the order of fetched data to display the latest orders first */}
        {data
          .slice()
          .reverse()
          .map((order, index) => (
            <div key={index} className="my-orders-order">
              {/* Parcel icon for visual representation */}
              <img src={assets.parcel_icon} alt="Parcel Icon" />

              {/* Display list of items in the order */}
              <p>
                {order.items.map((item, itemIndex) => (
                  <span key={itemIndex}>
                    {item.name} x {item.quantity}
                    {itemIndex !== order.items.length - 1 && ", "}{" "}
                    {/* Add a comma between items */}
                  </span>
                ))}
              </p>

              {/* Display the total order amount */}
              <p>${order.amount}.00</p>

              {/* Display the number of items in the order */}
              <p>Items: {order.items.length}</p>

              {/* Display the current status of the order */}
              <p>
                <span>&#x25cf;</span> <b>{order.status}</b>
              </p>

              {/* Track Order button (re-fetches orders on click) */}
              <button onClick={fetchOrders}>Track Order</button>
            </div>
          ))}
      </div>
    </div>
  );
};

export default MyOrders;
