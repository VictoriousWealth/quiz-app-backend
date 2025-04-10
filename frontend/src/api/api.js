import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000', // your FastAPI base URL
});

export default API;
