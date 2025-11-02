import { useEffect, useState } from 'react';
import { ApiClient } from '@/utils/api-client';

declare global {
  interface Window {
    WeixinJSBridge?: any;
  }
}

export function WeChatLoginButton() {
  const [loading, setLoading] = useState(false);
  const appId = process.env.NEXT_PUBLIC_WECHAT_APP_ID;

  useEffect(() => {
    // Initialize WeChat SDK
    if (typeof window !== 'undefined' && appId) {
      const script = document.createElement('script');
      script.src = 'https://res.wx.qq.com/connect/zh_CN/htmledition/js/wxLogin.js';
      document.body.appendChild(script);
    }
  }, [appId]);

  const handleWeChatLogin = async () => {
    if (!appId) {
      console.error('WeChat App ID not configured');
      return;
    }

    setLoading(true);
    try {
      // Initialize WeChat login
      const redirectUri = encodeURIComponent(window.location.origin + '/auth/wechat-callback');
      const state = Math.random().toString(36).substring(7);
      
      // Store state for validation
      sessionStorage.setItem('wechat_state', state);

      // Redirect to WeChat OAuth page
      const url = `https://open.weixin.qq.com/connect/qrconnect?appid=${appId}&redirect_uri=${redirectUri}&response_type=code&scope=snsapi_login&state=${state}#wechat_redirect`;
      window.location.href = url;
    } catch (error) {
      console.error('WeChat login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleWeChatLogin}
      disabled={loading || !appId}
      className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
    >
      {loading ? (
        'Connecting to WeChat...'
      ) : (
        <>
          <svg
            className="w-5 h-5 mr-2"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d="M8.85 16.48a.56.56 0 0 1-.27-.07l-2.18 1.11c-.12.06-.27 0-.33-.12-.03-.07-.03-.14 0-.2l.58-1.8a.58.58 0 0 0-.11-.54c-1.06-1.07-1.7-2.4-1.7-3.83 0-3.37 3.2-6.12 7.13-6.12s7.12 2.75 7.12 6.12c0 3.38-3.19 6.13-7.12 6.13-.96 0-1.9-.15-2.77-.46a.56.56 0 0 1-.35-.22zm3.35-11.8c-4.4 0-8 3.15-8 7.02 0 1.68.7 3.22 1.92 4.44l-.82 2.57c-.12.38.24.76.62.65l3.12-1.59c.96.35 2 .54 3.06.54 4.41 0 8-3.14 8-7.02s-3.59-7.01-8-7.01z"/>
          </svg>
          Continue with WeChat
        </>
      )}
    </button>
  );
}