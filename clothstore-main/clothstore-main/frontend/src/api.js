// this file is to handle the connection between the frontend and backend
// using axios to connect it which is an api connection library
import axios from "axios";

const api = axios.create({
  // the port of our fast api application
  baseURL: "http://localhost:8001",
});
export default api;
