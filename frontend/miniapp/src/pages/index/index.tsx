import { View, Input, Button, Text, Navigator } from '@tarojs/components';
import { useState } from 'react';
import Taro from '@tarojs/taro';
import './index.scss';
import { LoginCredentials } from '../../types/auth';
import { ApiClient } from '../../utils/api-client';

export default function Index() {
  const [credentials, setCredentials] = useState<LoginCredentials>({
    username: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    setError('');
    setLoading(true);

    try {
      await ApiClient.login(credentials);
      // Navigate to token page
      Taro.navigateTo({ url: '/pages/token/index' });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleWeChatLogin = async () => {
    try {
      const { code } = await Taro.login();
      await ApiClient.wechatLogin(code);
      Taro.navigateTo({ url: '/pages/token/index' });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'WeChat login failed');
    }
  };

  return (
    <View className="login-container">
      <Text className="title">Login to OpenBB</Text>

      <View className="form-item">
        <Text className="label">Username</Text>
        <Input
          type="text"
          value={credentials.username}
          onInput={e => setCredentials({ ...credentials, username: e.detail.value })}
          placeholder="Enter your username"
        />
      </View>

      <View className="form-item">
        <Text className="label">Password</Text>
        <Input
          password
          value={credentials.password}
          onInput={e => setCredentials({ ...credentials, password: e.detail.value })}
          placeholder="Enter your password"
        />
      </View>

      {error && <Text className="error-message">{error}</Text>}

      <Button
        className={`login-button ${loading ? 'loading' : ''}`}
        onClick={handleLogin}
        disabled={loading}
      >
        {loading ? 'Logging in...' : 'Login'}
      </Button>

      <View className="divider">
        <Text className="text">Or</Text>
      </View>

      <Button className="wechat-button" onClick={handleWeChatLogin}>
        Login with WeChat
      </Button>

      <Navigator url="/pages/register/index" className="register-link">
        Create new account
      </Navigator>
    </View>
  );
}
