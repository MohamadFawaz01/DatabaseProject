// this file is to handle the connection between the frontend and backend
// using axios to connect it
import axios from "axios";

const api = axios.create({
  // the port of our fast api application
  baseURL: "http://localhost:8001",
});
