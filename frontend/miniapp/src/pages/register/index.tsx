import { View, Input, Button, Text } from '@tarojs/components';
import { useState } from 'react';
import Taro from '@tarojs/taro';
import { RegisterData } from '../../types/auth';
import { ApiClient } from '../../utils/api-client';
import './index.scss';

export default function Register() {
  const [data, setData] = useState<RegisterData>({
    username: '',
    password: '',
    email: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    setError('');
    setLoading(true);

    try {
      await ApiClient.register(data);
      Taro.navigateTo({ url: '/pages/token/index' });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View className="register-container">
      <Text className="title">Create Account</Text>

      <View className="form-item">
        <Text className="label">Username</Text>
        <Input
          type="text"
          value={data.username}
          onInput={e => setData({ ...data, username: e.detail.value })}
          placeholder="Enter your username"
        />
      </View>

      <View className="form-item">
        <Text className="label">Email (optional)</Text>
        <Input
          type="text"
          value={data.email}
          onInput={e => setData({ ...data, email: e.detail.value })}
          placeholder="Enter your email"
        />
      </View>

      <View className="form-item">
        <Text className="label">Password</Text>
        <Input
          password
          value={data.password}
          onInput={e => setData({ ...data, password: e.detail.value })}
          placeholder="Enter your password"
        />
      </View>

      {error && <Text className="error-message">{error}</Text>}

      <Button
        className={`register-button ${loading ? 'loading' : ''}`}
        onClick={handleRegister}
        disabled={loading}
      >
        {loading ? 'Creating account...' : 'Create Account'}
      </Button>

      <View className="login-link" onClick={() => Taro.navigateBack()}>
        Back to Login
      </View>
    </View>
  );
}