import Taro from '@tarojs/taro';
import { AuthResponse, LoginCredentials, RegisterData } from '../types/auth';

const API_URL = process.env.API_URL || 'http://localhost:8000';

export class ApiClient {
  private static token: string | null = null;

  static setToken(token: string) {
    this.token = token;
    Taro.setStorageSync('auth_token', token);
  }

  static getToken(): string | null {
    if (!this.token) {
      this.token = Taro.getStorageSync('auth_token');
    }
    return this.token;
  }

  static clearToken() {
    this.token = null;
    Taro.removeStorageSync('auth_token');
  }

  private static async request<T>(endpoint: string, options: Omit<Taro.request.Option, 'url'> = {}): Promise<T> {
    const token = this.getToken();
    const header = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.header,
    };

    try {
      const response = await Taro.request({
        url: `${API_URL}${endpoint}`,
        ...options,
        header,
      });

      if (response.statusCode >= 400) {
        throw new Error(response.data.message || 'Request failed');
      }

      return response.data;
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Network error');
    }
  }

  static async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/auth/login', {
      method: 'POST',
      data: credentials,
    });
    this.setToken(response.token);
    return response;
  }

  static async register(data: RegisterData): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/auth/register', {
      method: 'POST',
      data,
    });
    this.setToken(response.token);
    return response;
  }

  static async wechatLogin(code: string): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/auth/wechat', {
      method: 'POST',
      data: { code },
    });
    this.setToken(response.token);
    return response;
  }
}