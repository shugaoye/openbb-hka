import { View, Text, Button } from '@tarojs/components';
import { useEffect, useState } from 'react';
import Taro from '@tarojs/taro';
import { ApiClient } from '../../utils/api-client';
import './index.scss';

export default function Token() {
  const [token, setToken] = useState<string>('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const storedToken = ApiClient.getToken();
    if (!storedToken) {
      Taro.navigateTo({ url: '/pages/index/index' });
      return;
    }
    
    // Use requestAnimationFrame equivalent for Taro
    setTimeout(() => {
      setToken(storedToken);
    }, 0);
  }, []);

  const handleCopy = async () => {
    try {
      await Taro.setClipboardData({
        data: token,
      });
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy token:', err);
    }
  };

  const handleLogout = () => {
    ApiClient.clearToken();
    Taro.reLaunch({ url: '/pages/index/index' });
  };

  return (
    <View className="token-container">
      <Text className="title">Your JWT Token</Text>
      <Text className="subtitle">Copy this token to use with OpenBB Workspace</Text>

      <View className="token-display">
        <Text className="token-text">{token}</Text>
      </View>

      <Button className="copy-button" onClick={handleCopy}>
        {copied ? 'Copied!' : 'Copy to Clipboard'}
      </Button>

      <Button className="logout-button" onClick={handleLogout}>
        Logout
      </Button>
    </View>
  );
}