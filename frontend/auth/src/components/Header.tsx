import React from 'react';
import { MoonIcon, SunIcon, LogOutIcon } from './Icons';
import { authApi } from '../api';

interface HeaderProps {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
  isAuthenticated: boolean;
  setIsAuthenticated: () => void;
}

const Header: React.FC<HeaderProps> = ({ theme, toggleTheme, isAuthenticated, setIsAuthenticated }) => {
  // 处理登出
  const handleLogout = () => {
    console.log('Performing logout');
    // 使用authApi清除认证信息
    authApi.clearAuthInfo();
    
    // 更新认证状态
    setIsAuthenticated();
    
    // 重定向到登录页
    window.location.href = '/login';
  };

  return (
    <header className="bg-white dark:bg-dark-800 shadow-md sticky top-0 z-10">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-primary">OpenBB Auth</h1>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* 主题切换按钮 */}
            <button 
              onClick={toggleTheme} 
              className="p-2 rounded-full hover:bg-dark-200 dark:hover:bg-dark-700 transition-colors"
              aria-label={theme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'}
            >
              {theme === 'light' ? <MoonIcon className="w-5 h-5" /> : <SunIcon className="w-5 h-5" />}
            </button>
            
            {/* 登出按钮（仅在已登录时显示） */}
            {isAuthenticated && (
              <button 
                onClick={handleLogout}
                className="flex items-center space-x-2 px-4 py-2 bg-dark-200 dark:bg-dark-700 rounded-lg hover:bg-dark-300 dark:hover:bg-dark-600 transition-colors"
              >
                <LogOutIcon className="w-4 h-4" />
                <span>Logout</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;