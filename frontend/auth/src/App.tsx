import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import TokenPage from './pages/TokenPage';
import Header from './components/Header';
import { useLocalStorage } from './hooks/useLocalStorage';
import { authApi } from './api';

function App() {
  // 主题管理
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');
  const [isLoading, setIsLoading] = useState(true);

  // 初始化主题
  useEffect(() => {
    // 检查系统偏好
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme) {
      setTheme(savedTheme as 'light' | 'dark');
    } else if (prefersDark) {
      setTheme('dark');
    }
    
    setIsLoading(false);
  }, []);

  // 应用主题到HTML元素
  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [theme]);

  // 切换主题
  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  // 检查用户是否已登录
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  // 初始化认证状态
  useEffect(() => {
    const checkAuthStatus = () => {
      const tokenExists = authApi.getToken() !== null;
      const authStatus = authApi.isAuthenticated();
      setIsAuthenticated(authStatus);
      console.log('Auth status check:', { tokenExists, authStatus });
      console.log('Storage contents:', {
        localStorage: {
          token: localStorage.getItem('token') ? 'exists' : 'not found',
          isAuthenticated: localStorage.getItem('isAuthenticated')
        },
        sessionStorage: {
          token: sessionStorage.getItem('token') ? 'exists' : 'not found',
          isAuthenticated: sessionStorage.getItem('isAuthenticated')
        }
      });
    };
    
    // 初始检查
    checkAuthStatus();
    
    // 定期检查以确保状态同步
    const intervalId = setInterval(checkAuthStatus, 1000);
    
    // 监听存储变化
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === 'token' || event.key === 'isAuthenticated' || event.key === null) {
        console.log('Storage change detected:', event);
        checkAuthStatus();
      }
    };
    
    window.addEventListener('storage', handleStorageChange);
    return () => {
      window.removeEventListener('storage', handleStorageChange);
      clearInterval(intervalId);
    };
  }, []);
  
  // 优化setIsAuthenticated函数
  const updateAuthStatus = () => {
    const authStatus = authApi.isAuthenticated();
    console.log('Updating auth status to:', authStatus);
    setIsAuthenticated(authStatus);
  };

  if (isLoading) {
    return <div className="flex items-center justify-center h-screen"><div className="text-xl font-medium">Loading...</div></div>;
  }

  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Header 
            theme={theme} 
            toggleTheme={toggleTheme} 
            isAuthenticated={isAuthenticated}
            setIsAuthenticated={updateAuthStatus} />
        <main className="flex-grow container mx-auto px-4 py-8">
          <Routes>
              {/* 主路由：根据认证状态重定向到不同页面 */}
              <Route 
                path="/" 
                element={
                  isAuthenticated ? 
                    <Navigate to="/token" replace /> : 
                    <Navigate to="/login" replace /> 
                } 
              />
              
              {/* 登录页 */}
              <Route 
                path="/login" 
                element={
                  isAuthenticated ? 
                    <Navigate to="/token" replace /> : 
                    <LoginPage setIsAuthenticated={updateAuthStatus} /> 
                } 
              />
              
              {/* 注册页 */}
              <Route 
                path="/register" 
                element={
                  isAuthenticated ? 
                    <Navigate to="/token" replace /> : 
                    <RegisterPage /> 
                } 
              />
              
              {/* Token页 */}
              <Route 
                path="/token" 
                element={
                  // 同时检查认证状态和token是否存在
                  isAuthenticated && authApi.hasValidToken() ? 
                    <TokenPage /> : 
                    <Navigate to="/login" replace /> 
                } 
              />
              
              {/* 捕获所有未匹配的路由 */}
              <Route 
                path="*" 
                element={
                  isAuthenticated ? 
                    <Navigate to="/token" replace /> : 
                    <Navigate to="/login" replace /> 
                } 
              />
            </Routes>
        </main>
        <footer className="bg-dark-800 text-dark-200 py-6 mt-8">
          <div className="container mx-auto px-4 text-center">
            <p className="text-sm">© {new Date().getFullYear()} OpenBB Auth Portal</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;