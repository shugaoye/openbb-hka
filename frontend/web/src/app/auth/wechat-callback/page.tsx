import { ApiClient } from '@/utils/api-client';
import { useSearchParams } from 'next/navigation';
import { useEffect } from 'react';

export default function WeChatCallback() {
  const searchParams = useSearchParams();
  
  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const state = searchParams.get('state');
      const savedState = sessionStorage.getItem('wechat_state');

      // Verify state to prevent CSRF attacks
      if (!state || state !== savedState) {
        console.error('Invalid state parameter');
        window.location.href = '/login';
        return;
      }

      if (code) {
        try {
          // Exchange code for token
          await ApiClient.wechatLogin(code);
          window.location.href = '/token';
        } catch (error) {
          console.error('WeChat login failed:', error);
          window.location.href = '/login';
        }
      } else {
        window.location.href = '/login';
      }
    };

    handleCallback();
  }, [searchParams]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h2 className="text-xl font-semibold text-gray-900">Processing WeChat login...</h2>
        <p className="mt-2 text-gray-600">Please wait while we complete your login.</p>
      </div>
    </div>
  );
}