import React, { useState, useEffect } from 'react';
import { CopyIcon, CheckIcon, AlertCircleIcon } from '../components/Icons';
import { authApi, UserInfo, ApiError } from '../api';

const TokenPage: React.FC = () => {
  const [token, setToken] = useState('');
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState('');
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // 从localStorage获取令牌并获取用户信息
  useEffect(() => {
    console.log('TokenPage loading, checking authentication...');
    const storedToken = authApi.getToken();
    
    console.log('TokenPage storedToken:', storedToken ? 'exists' : 'not found');
    console.log('TokenPage isAuthenticated:', authApi.isAuthenticated());
    
    if (!storedToken) {
      setError('No authentication token found. Please login again.');
      setIsLoading(false);
      return;
    }
    
    setToken(storedToken);
    console.log('Token set to state');
    
    // 获取用户信息
    const fetchUserInfo = async () => {
      try {
        const data = await authApi.getCurrentUser(storedToken);
        setUserInfo(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch user information');
        // 清除认证状态
        authApi.clearAuthInfo();
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchUserInfo();
  }, []);

  // 复制令牌到剪贴板
  const copyToClipboard = () => {
    navigator.clipboard.writeText(token)
      .then(() => {
        setCopied(true);
        // 3秒后重置复制状态
        setTimeout(() => {
          setCopied(false);
        }, 3000);
      })
      .catch(() => {
        // 如果剪贴板API失败，使用传统方法
        const textArea = document.createElement('textarea');
        textArea.value = token;
        document.body.appendChild(textArea);
        textArea.select();
        try {
          document.execCommand('copy');
          setCopied(true);
          setTimeout(() => {
            setCopied(false);
          }, 3000);
        } catch (err) {
          setError('Failed to copy token to clipboard');
        }
        document.body.removeChild(textArea);
      });
  };

  // 刷新令牌（模拟）
  const refreshToken = async () => {
    try {
      // 在实际应用中，这里应该调用刷新令牌的API
      // 由于我们当前没有实现刷新令牌的功能，这里仅作为示例
      throw new Error('Token refresh is not implemented in this demo');
      
      /* 示例代码
      const response = await fetch('/auth/refresh-token', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      
      if (!response.ok) {
        throw new Error('Failed to refresh token');
      }
      
      const data = await response.json();
      const newToken = data.access_token;
      
      // 更新本地存储和状态
      localStorage.setItem('token', newToken);
      setToken(newToken);
      */
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh token');
    }
  };

  // 登出
  const handleLogout = () => {
    // 清除认证信息
    authApi.clearAuthInfo();
    
    // 重定向到登录页
    window.location.href = '/login';
  };

  if (isLoading) {
    return (
      <div className="max-w-2xl mx-auto mt-10 flex items-center justify-center h-64">
        <div className="text-xl font-medium">Loading...</div>
      </div>
    );
  }

  if (error || !userInfo) {
    return (
      <div className="max-w-2xl mx-auto mt-10 fade-in">
        <div className="card">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <AlertCircleIcon className="w-10 h-10 text-danger mx-auto mb-4" />
              <p className="text-lg text-danger mb-6">{error || 'Authentication error'}</p>
              <button
                onClick={() => window.location.href = '/login'}
                className="btn-primary py-2 px-6 rounded-lg"
              >
                Go to Login
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 fade-in">
      <div className="card">
        <h2 className="text-2xl font-bold mb-6 text-center">Your API Token</h2>
        
        {/* 用户信息 */}
        <div className="mb-6 p-4 bg-dark-100 dark:bg-dark-700 rounded-lg">
          <h3 className="text-lg font-medium mb-2">User Information</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-dark-500 dark:text-dark-400">Username</p>
              <p className="font-medium">{userInfo.username}</p>
            </div>
            {userInfo.email && (
              <div>
                <p className="text-sm text-dark-500 dark:text-dark-400">Email</p>
                <p className="font-medium">{userInfo.email}</p>
              </div>
            )}
          </div>
        </div>
        
        {/* 令牌信息 */}
        <div className="mb-6">
          <h3 className="text-lg font-medium mb-3">Access Token</h3>
          <p className="text-sm text-dark-500 dark:text-dark-400 mb-2">
            Copy this token to use with OpenBB Workspace
          </p>
          
          <div className="relative mt-2 mb-4">
            <textarea
              value={token}
              readOnly
              className="w-full p-4 bg-dark-100 dark:bg-dark-700 border border-dark-300 dark:border-dark-600 rounded-lg font-mono text-sm h-32 resize-none overflow-x-auto"
            />
            <button
              onClick={copyToClipboard}
              className="absolute top-2 right-2 p-2 bg-dark-200 dark:bg-dark-600 rounded-lg hover:bg-dark-300 dark:hover:bg-dark-500 transition-colors"
              aria-label="Copy token to clipboard"
            >
              {copied ? (
                <div className="flex items-center space-x-1">
                  <CheckIcon className="w-4 h-4 text-success" />
                  <span className="text-xs text-success">Copied!</span>
                </div>
              ) : (
                <CopyIcon className="w-4 h-4" />
              )}
            </button>
          </div>
          
          <div className="flex flex-wrap gap-2 justify-between">
            <button
              onClick={refreshToken}
              className="btn-secondary py-2 px-4 rounded-lg text-sm"
            >
              Refresh Token
            </button>
            
            <button
              onClick={handleLogout}
              className="btn-danger py-2 px-4 rounded-lg text-sm"
            >
              Logout
            </button>
          </div>
        </div>
        
        {/* 使用说明 */}
        <div className="p-4 bg-primary/5 dark:bg-primary/10 border border-primary/20 rounded-lg">
          <h3 className="text-lg font-medium mb-2 text-primary">How to use this token</h3>
          <ol className="list-decimal list-inside space-y-2 text-sm">
            <li>Copy the access token above</li>
            <li>Open OpenBB Workspace</li>
            <li>Go to Settings → API Keys</li>
            <li>Paste the token in the appropriate field</li>
            <li>Save your settings</li>
            <li>You can now access protected resources</li>
          </ol>
          <p className="mt-3 text-xs text-dark-500 dark:text-dark-400">
            This token will expire after 30 minutes. You will need to log in again to generate a new token.
          </p>
        </div>
      </div>
    </div>
  );
};

export default TokenPage;