import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import axios from 'axios';

// Set the base URL for API requests
// In development, this would typically be your backend server
axios.defaults.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(<App />);