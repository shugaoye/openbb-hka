import { AuthResponse, LoginCredentials, RegisterData } from '../../../types/auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export class ApiClient {
  private static token: string | null = null;

  static setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', token);
    }
  }

  static getToken(): string | null {
    if (!this.token && typeof window !== 'undefined') {
      this.token = localStorage.getItem('auth_token');
    }
    return this.token;
  }

  static clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('auth_token');
    }
  }

  private static async fetchWithAuth(endpoint: string, options: RequestInit = {}) {
    const token = this.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'An error occurred' }));
      throw new Error(error.message || 'Network response was not ok');
    }

    return response.json();
  }

  static async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await this.fetchWithAuth('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    this.setToken(response.token);
    return response;
  }

  static async register(data: RegisterData): Promise<AuthResponse> {
    const response = await this.fetchWithAuth('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    this.setToken(response.token);
    return response;
  }

  static async wechatLogin(code: string): Promise<AuthResponse> {
    const response = await this.fetchWithAuth('/auth/wechat', {
      method: 'POST',
      body: JSON.stringify({ code }),
    });
    this.setToken(response.token);
    return response;
  }
}