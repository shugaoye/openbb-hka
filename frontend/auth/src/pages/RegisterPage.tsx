import React, { useState, useRef, useEffect } from 'react';
import { LockIcon, UserIcon, MailIcon, EyeIcon, EyeOffIcon, AlertCircleIcon } from '../components/Icons';
import { authApi, ApiError } from '../api';

const RegisterPage: React.FC = () => {
  // 表单状态
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [passwordStrength, setPasswordStrength] = useState<0 | 1 | 2 | 3 | 4>(0);
  
  // 表单引用
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const confirmPasswordRef = useRef<HTMLInputElement>(null);

  // 处理密码强度检查
  useEffect(() => {
    // 简单的密码强度检查逻辑
    if (!password) {
      setPasswordStrength(0);
      return;
    }
    
    let strength = 0;
    
    // 长度检查
    if (password.length >= 8) strength++;
    
    // 包含小写字母
    if (/[a-z]/.test(password)) strength++;
    
    // 包含大写字母或数字
    if (/[A-Z]/.test(password) || /[0-9]/.test(password)) strength++;
    
    // 包含特殊字符
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    setPasswordStrength(strength as 0 | 1 | 2 | 3 | 4);
  }, [password]);

  // 处理用户名输入
  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
    setError(''); // 清除错误信息
  };

  // 处理邮箱输入
  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
    setError(''); // 清除错误信息
  };

  // 处理密码输入
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
    setError(''); // 清除错误信息
  };

  // 处理确认密码输入
  const handleConfirmPasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmPassword(e.target.value);
    setError(''); // 清除错误信息
  };

  // 切换密码显示状态
  const toggleShowPassword = () => {
    setShowPassword(!showPassword);
  };

  // 验证邮箱格式
  const isValidEmail = (email: string): boolean => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  // 处理表单提交
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // 表单验证
    if (!username || !password || !confirmPassword) {
      setError('Please fill in all required fields');
      return;
    }
    
    if (username.length < 3) {
      setError('Username must be at least 3 characters long');
      return;
    }
    
    if (email && !isValidEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }
    
    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }
    
    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    setIsLoading(true);
    setError('');
    setSuccess('');
    
    try {
      // 使用authApi注册用户
      await authApi.register({
        username,
        password,
        email: email || undefined
      });

      // 注册成功后，自动登录用户
      const loginData = await authApi.login({
        username,
        password
      });

      // 保存认证信息
      authApi.saveAuthInfo(loginData);
      
      // 跳转到令牌页面
      window.location.href = '/token';
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.statusCode === 400) {
          setError('Username already exists');
        } else {
          setError(err.message);
        }
      } else {
        setError(err instanceof Error ? err.message : 'Registration failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // 跳转到登录页面
  const goToLogin = () => {
    window.location.href = '/login';
  };

  // 获取密码强度文本
  const getPasswordStrengthText = () => {
    switch (passwordStrength) {
      case 0:
        return '';
      case 1:
        return 'Weak';
      case 2:
        return 'Fair';
      case 3:
        return 'Good';
      case 4:
        return 'Strong';
      default:
        return '';
    }
  };

  // 获取密码强度类名
  const getPasswordStrengthClassName = () => {
    switch (passwordStrength) {
      case 0:
        return 'w-full bg-dark-200 dark:bg-dark-700';
      case 1:
        return 'password-strength-weak';
      case 2:
        return 'password-strength-medium';
      case 3:
      case 4:
        return 'password-strength-strong';
      default:
        return 'w-full bg-dark-200 dark:bg-dark-700';
    }
  };

  return (
    <div className="max-w-md mx-auto mt-8 fade-in">
      <div className="card">
        <h2 className="text-2xl font-bold mb-6 text-center">Register for OpenBB</h2>
        
        {error && (
          <div className="mb-4 p-3 bg-danger/10 text-danger rounded-lg flex items-center">
            <AlertCircleIcon className="w-5 h-5 mr-2 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}
        
        {success && (
          <div className="mb-4 p-3 bg-success/10 text-success rounded-lg flex items-center">
            <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            <span>{success}</span>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* 用户名输入框 */}
          <div>
            <label htmlFor="username" className="block text-sm font-medium mb-1">Username <span className="text-danger">*</span></label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <UserIcon className="w-5 h-5 text-dark-400" />
              </div>
              <input
                type="text"
                id="username"
                value={username}
                onChange={handleUsernameChange}
                onKeyDown={(e) => e.key === 'Enter' && emailRef.current?.focus()}
                className="w-full pl-10 pr-4 py-2 border rounded-lg"
                placeholder="Enter your username"
                required
                minLength={3}
                maxLength={50}
              />
            </div>
            <p className="text-xs text-dark-500 dark:text-dark-400 mt-1">At least 3 characters</p>
          </div>
          
          {/* 邮箱输入框 */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium mb-1">Email (Optional)</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MailIcon className="w-5 h-5 text-dark-400" />
              </div>
              <input
                ref={emailRef}
                type="email"
                id="email"
                value={email}
                onChange={handleEmailChange}
                onKeyDown={(e) => e.key === 'Enter' && passwordRef.current?.focus()}
                className="w-full pl-10 pr-4 py-2 border rounded-lg"
                placeholder="Enter your email address"
              />
            </div>
          </div>
          
          {/* 密码输入框 */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium mb-1">Password <span className="text-danger">*</span></label>
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
                onKeyDown={(e) => e.key === 'Enter' && confirmPasswordRef.current?.focus()}
                className="w-full pl-10 pr-10 py-2 border rounded-lg"
                placeholder="Enter your password"
                required
                minLength={6}
              />
              <button
                type="button"
                onClick={toggleShowPassword}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-dark-400 hover:text-dark-600 dark:hover:text-dark-200"
              >
                {showPassword ? <EyeOffIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
              </button>
            </div>
            <p className="text-xs text-dark-500 dark:text-dark-400 mt-1">At least 6 characters</p>
            
            {/* 密码强度指示器 */}
            {password && (
              <div className="mt-2">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs">Password Strength</span>
                  <span className={`text-xs font-medium ${passwordStrength <= 1 ? 'text-danger' : passwordStrength === 2 ? 'text-warning' : 'text-success'}`}>
                    {getPasswordStrengthText()}
                  </span>
                </div>
                <div className="h-1 rounded-full bg-dark-200 dark:bg-dark-700 overflow-hidden">
                  <div className={getPasswordStrengthClassName()}></div>
                </div>
              </div>
            )}
          </div>
          
          {/* 确认密码输入框 */}
          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium mb-1">Confirm Password <span className="text-danger">*</span></label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <LockIcon className="w-5 h-5 text-dark-400" />
              </div>
              <input
                ref={confirmPasswordRef}
                type={showPassword ? 'text' : 'password'}
                id="confirmPassword"
                value={confirmPassword}
                onChange={handleConfirmPasswordChange}
                onKeyDown={(e) => e.key === 'Enter' && handleSubmit(e)}
                className="w-full pl-10 pr-4 py-2 border rounded-lg"
                placeholder="Confirm your password"
                required
              />
            </div>
          </div>
          
          {/* 注册按钮 */}
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
                Registering...
              </div>
            ) : (
              'Register'
            )}
          </button>
        </form>
        
        {/* 登录链接 */}
        <div className="mt-6 text-center">
          <p className="text-sm text-dark-600 dark:text-dark-400">
            Already have an account? 
            <button
              onClick={goToLogin}
              className="text-primary hover:underline ml-1 font-medium"
            >
              Login
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;