'use client';

import { ApiClient } from '@/utils/api-client';
import { useEffect, useState } from 'react';

export default function TokenPage() {
  const [token, setToken] = useState<string>('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const storedToken = ApiClient.getToken();
    if (!storedToken) {
      window.location.href = '/login';
      return;
    }
    
    // Use requestAnimationFrame to avoid synchronous state update
    requestAnimationFrame(() => {
      setToken(storedToken);
    });
  }, []);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(token);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy token:', err);
    }
  };

  const handleLogout = () => {
    ApiClient.clearToken();
    window.location.href = '/login';
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-lg w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Your JWT Token
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Copy this token to use with OpenBB Workspace
          </p>
        </div>

        <div className="bg-white shadow sm:rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="mt-2 max-w-xl text-sm text-gray-500">
              <p>
                Your authentication token is shown below. Use this token to authenticate with the OpenBB Workspace backend.
              </p>
            </div>
            <div className="mt-5">
              <textarea
                readOnly
                value={token}
                className="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md h-24 font-mono"
              />
            </div>
            <div className="mt-5 space-y-4">
              <button
                type="button"
                onClick={copyToClipboard}
                className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                {copied ? 'Copied!' : 'Copy to Clipboard'}
              </button>
              
              <button
                type="button"
                onClick={handleLogout}
                className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}