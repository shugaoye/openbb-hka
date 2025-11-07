import React, { useState, useRef } from 'react';
import { LockIcon, UserIcon, EyeIcon, EyeOffIcon, AlertCircleIcon, WechatIcon } from '../components/Icons';
import { authApi, ApiError } from '../api';

interface LoginPageProps {
  setIsAuthenticated: () => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ setIsAuthenticated }) => {
  // 表单状态
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isWechatLoading, setIsWechatLoading] = useState(false);
  
  // 表单引用
  const passwordRef = useRef<HTMLInputElement>(null);

  // 处理用户名输入
  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
    setError(''); // 清除错误信息
  };

  // 处理密码输入
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
    setError(''); // 清除错误信息
  };

  // 切换密码显示状态
  const toggleShowPassword = () => {
    setShowPassword(!showPassword);
  };

  // 处理表单提交
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // 表单验证
    if (!username || !password) {
      setError('Please enter both username and password');
      return;
    }
    
    setIsLoading(true);
    setError('');
    
    try {
      // 使用 authApi 进行登录
      const data = await authApi.login({
        username,
        password
      });
      
      try {
        // 保存认证信息 - 传递完整的LoginResponse对象
          authApi.saveAuthInfo(data);
        console.log('Login successful, token saved');
        
        // 强制更新认证状态
        setIsAuthenticated();
        
        // 立即检查存储
        console.log('localStorage token exists:', localStorage.getItem('token') ? 'yes' : 'no');
        console.log('sessionStorage token exists:', sessionStorage.getItem('token') ? 'yes' : 'no');
        console.log('Auth status after save:', authApi.isAuthenticated());
        
        // 延迟稍微长一点，确保所有状态更新完成
        setTimeout(() => {
          console.log('Final check before redirect:', authApi.isAuthenticated());
          console.log('Redirecting to token page...');
          window.location.href = '/token';
        }, 800);
      } catch (error) {
        console.error('Error during login process:', error);
        setError('Failed to complete login process. Please try again.');
        setIsLoading(false);
      }
    } catch (err) {
      if (err instanceof ApiError && err.statusCode === 401) {
        setError('Invalid username or password');
      } else {
        setError(err instanceof Error ? err.message : 'Login failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // 处理微信登录
  const handleWechatLogin = async () => {
    setIsWechatLoading(true);
    setError('');
    
    try {
      // 注意：在实际应用中，这里需要调用微信登录API获取code
      // 由于没有实际的微信环境，这里仅作为示例
      // 在生产环境中，需要使用微信提供的SDK或API获取真实code
      const mockCode = 'mock_code';
      const data = await authApi.wechatLogin(mockCode);
      
      try {
        // 保存认证信息 - 传递完整的LoginResponse对象
          authApi.saveAuthInfo(data);
        console.log('WeChat login successful, token saved');
        
        // 强制更新认证状态
        setIsAuthenticated();
        
        // 立即检查存储
        console.log('localStorage token exists:', localStorage.getItem('token') ? 'yes' : 'no');
        console.log('sessionStorage token exists:', sessionStorage.getItem('token') ? 'yes' : 'no');
        console.log('Auth status after save:', authApi.isAuthenticated());
        
        // 延迟稍微长一点，确保所有状态更新完成
        setTimeout(() => {
          console.log('Final check before redirect:', authApi.isAuthenticated());
          console.log('Redirecting to token page...');
          window.location.href = '/token';
        }, 800);
      } catch (error) {
        console.error('Error during WeChat login process:', error);
        setError('Failed to complete login process. Please try again.');
        setIsWechatLoading(false);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'WeChat login failed. Please try again.');
    } finally {
      setIsWechatLoading(false);
    }
  };

  // 跳转到注册页面
  const goToRegister = () => {
    window.location.href = '/register';
  };

  return (
    <div className="max-w-md mx-auto mt-10 fade-in">
      <div className="card">
        <h2 className="text-2xl font-bold mb-6 text-center">Login to OpenBB</h2>
        
        {error && (
          <div className="mb-4 p-3 bg-danger/10 text-danger rounded-lg flex items-center">
            <AlertCircleIcon className="w-5 h-5 mr-2 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* 用户名输入框 */}
          <div>
            <label htmlFor="username" className="block text-sm font-medium mb-1">Username</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <UserIcon className="w-5 h-5 text-dark-400" />
              </div>
              <input
                type="text"
                id="username"
                value={username}
                onChange={handleUsernameChange}
                onKeyDown={(e) => e.key === 'Enter' && passwordRef.current?.focus()}
                className="w-full pl-10 pr-4 py-2 border rounded-lg"
                placeholder="Enter your username"
                required
              />
            </div>
          </div>
          
          {/* 密码输入框 */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium mb-1">Password</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <LockIcon className="w-5 h-5 text-dark-400" />
              </div>
              <input
                ref={passwordRef}
                type={showPassword ? 'text' : 'password'}
                id="password"
                value={password}
                onChange={handlePasswordChange}
                onKeyDown={(e) => e.key === 'Enter' && handleSubmit(e)}
                className="w-full pl-10 pr-10 py-2 border rounded-lg"
                placeholder="Enter your password"
                required
              />
              <button
                type="button"
                onClick={toggleShowPassword}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-dark-400 hover:text-dark-600 dark:hover:text-dark-200"
              >
                {showPassword ? <EyeOffIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
              </button>
            </div>
          </div>
          
          {/* 登录按钮 */}
          <button
            type="submit"
            className="w-full btn-primary py-2 px-4 rounded-lg font-medium transition-all duration-200"
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Loading...
              </div>
            ) : (
              'Login'
            )}
          </button>
        </form>
        
        {/* 分隔线 */}
        <div className="relative my-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-dark-200 dark:border-dark-700"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white dark:bg-dark-800 text-dark-500 dark:text-dark-400">
              or
            </span>
          </div>
        </div>
        
        {/* 微信登录按钮 */}
        <button
          onClick={handleWechatLogin}
          className="w-full flex items-center justify-center py-2 px-4 border border-dark-300 dark:border-dark-700 rounded-lg font-medium transition-all duration-200 hover:bg-dark-100 dark:hover:bg-dark-700"
          disabled={isWechatLoading}
        >
          <WechatIcon className="w-5 h-5 mr-2" />
          {isWechatLoading ? 'Loading...' : 'Login with WeChat'}
        </button>
        
        {/* 注册链接 */}
        <div className="mt-6 text-center">
          <p className="text-sm text-dark-600 dark:text-dark-400">
            Don't have an account? 
            <button
              onClick={goToRegister}
              className="text-primary hover:underline ml-1 font-medium"
            >
              Register
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;