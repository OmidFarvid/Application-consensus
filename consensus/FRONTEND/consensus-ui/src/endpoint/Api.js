import axios from "axios";

export default axios.create({
  baseURL: "/api/v1",
  timeout: 5000,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "xsrfHeaderName",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json"
  }
});
