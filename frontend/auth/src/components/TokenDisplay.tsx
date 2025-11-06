import React, { useState, useEffect } from 'react';

interface TokenDisplayProps {
  token: string;
  onLogout: () => void;
}

const TokenDisplay: React.FC<TokenDisplayProps> = ({ token, onLogout }) => {
  const [copied, setCopied] = useState(false);
  const [userInfo, setUserInfo] = useState<{username: string, email: string} | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserInfo = async () => {
      try {
        const response = await fetch(`/api/auth/me?token=${token}`);
        if (response.ok) {
          const data = await response.json();
          setUserInfo(data);
        }
      } catch (error) {
        console.error('Failed to fetch user info:', error);
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchUserInfo();
    }
  }, [token]);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(token);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white dark:bg-gray-800 py-8 px-4 shadow sm:rounded-lg sm:px-10">
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">Authentication Successful</h3>
        {loading ? (
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">Loading user information...</p>
        ) : userInfo ? (
          <div className="mt-2">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Welcome, <span className="font-medium">{userInfo.username}</span>!
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Email: <span className="font-medium">{userInfo.email}</span>
            </p>
          </div>
        ) : (
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Welcome! Your JWT token is displayed below.
          </p>
        )}
        <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
          Copy this token to use with OpenBB Workspace.
        </p>
      </div>

      <div className="mt-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          JWT Token
        </label>
        <div className="flex rounded-md shadow-sm">
          <input
            type="text"
            readOnly
            value={token}
            className="flex-1 min-w-0 block w-full px-3 py-2 rounded-none rounded-l-md border border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
          />
          <button
            onClick={copyToClipboard}
            className="inline-flex items-center px-3 rounded-r-md border border-l-0 border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-500 dark:text-gray-300 text-sm"
          >
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>
      </div>

      <div className="mt-6">
        <button
          onClick={onLogout}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default TokenDisplay;