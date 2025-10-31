import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Initialize auth from localStorage or API
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Verify token is still valid
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      // For now, just set the user as authenticated if token exists
      // In a real app, you might want to verify the token with an API call
      setCurrentUser({ username: localStorage.getItem('username') || 'user' });
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    setError('');
    try {
      const response = await axios.post('/auth/token', {
        username,
        password
      });
      
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      localStorage.setItem('username', username);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      setCurrentUser({ username });
      return { success: true };
    } catch (error) {
      setError(error.response?.data?.detail || 'Login failed');
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const register = async (username, email, password) => {
    setError('');
    try {
      const response = await axios.post('/auth/register', {
        username,
        email,
        password
      });
      
      // Auto-login after registration
      return await login(username, password);
    } catch (error) {
      setError(error.response?.data?.detail || 'Registration failed');
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    }
  };

  const wechatLogin = async (code) => {
    setError('');
    try {
      const response = await axios.post('/auth/wechat/login', {
        code
      });
      
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      localStorage.setItem('username', 'wechat_user');
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      setCurrentUser({ username: 'wechat_user' });
      return { success: true };
    } catch (error) {
      setError(error.response?.data?.detail || 'WeChat login failed');
      return { success: false, error: error.response?.data?.detail || 'WeChat login failed' };
    }
  };

  const logout = async () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    delete axios.defaults.headers.common['Authorization'];
    setCurrentUser(null);
  };

  const value = {
    currentUser,
    login,
    register,
    wechatLogin,
    logout,
    error
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};