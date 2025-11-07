// API调用封装

// 定义API响应接口
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

// 注册请求接口
export interface RegisterRequest {
  username: string;
  password: string;
  email?: string;
}

// 登录请求接口
export interface LoginRequest {
  username: string;
  password: string;
}

// 登录响应接口
export interface LoginResponse {
  access_token: string;
  token_type: string;
  username: string;
}

// 用户信息接口
export interface UserInfo {
  username: string;
  email?: string;
  id: number;
  created_at: string;
}

// 基础API错误类
export class ApiError extends Error {
  constructor(public message: string, public statusCode?: number) {
    super(message);
    this.name = 'ApiError';
  }
}

// 通用fetch封装
async function fetchWithError<T>(url: string, options: RequestInit = {}): Promise<T> {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      // 解析错误信息
      const errorMessage = data.detail || data.error || `HTTP error! Status: ${response.status}`;
      throw new ApiError(errorMessage, response.status);
    }

    return data as T;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    // 网络错误或解析错误
    throw new ApiError(
      error instanceof Error ? error.message : 'Network error occurred',
      0
    );
  }
}

// 认证相关API
export const authApi = {
  // 用户注册
  async register(request: RegisterRequest): Promise<UserInfo> {
    return fetchWithError<UserInfo>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  },

  // 用户登录
  async login(request: LoginRequest): Promise<LoginResponse> {
    // 使用FormData格式发送登录请求，因为FastAPI的OAuth2PasswordRequestForm期望这种格式
    const formData = new URLSearchParams();
    formData.append('username', request.username);
    formData.append('password', request.password);

    try {
      const response = await fetch('/auth/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      });

      const data = await response.json();

      if (!response.ok) {
        const errorMessage = data.detail || `Login failed! Status: ${response.status}`;
        throw new ApiError(errorMessage, response.status);
      }

      return data;
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      throw new ApiError(
        error instanceof Error ? error.message : 'Network error occurred',
        0
      );
    }
  },

  // 获取当前用户信息
  async getCurrentUser(token: string): Promise<UserInfo> {
    return fetchWithError<UserInfo>('/auth/me', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
  },

  // 微信登录（模拟）
  async wechatLogin(code: string): Promise<LoginResponse> {
    return fetchWithError<LoginResponse>('/auth/wechat-login', {
      method: 'POST',
      body: JSON.stringify({ code }),
    });
  },

  // 保存认证信息到本地存储
  saveAuthInfo(loginResponse: LoginResponse): void {
    console.log('Saving auth info:', loginResponse);
    
    // 同时保存到localStorage和sessionStorage作为双重保险
    // 不使用try-catch避免掩盖其他错误
    try {
      localStorage.setItem('token', loginResponse.access_token);
      localStorage.setItem('isAuthenticated', 'true');
      console.log('Auth info saved to localStorage successfully');
    } catch (localError) {
      console.error('Error saving to localStorage:', localError);
    }
    
    try {
      sessionStorage.setItem('token', loginResponse.access_token);
      sessionStorage.setItem('isAuthenticated', 'true');
      console.log('Auth info saved to sessionStorage successfully');
    } catch (sessionError) {
      console.error('Error saving to sessionStorage:', sessionError);
    }
    
    // 验证保存结果
    const localStorageToken = localStorage.getItem('token');
    const sessionStorageToken = sessionStorage.getItem('token');
    console.log('Save verification:', {
      localStorageToken: localStorageToken ? 'exists' : 'not found',
      sessionStorageToken: sessionStorageToken ? 'exists' : 'not found',
      match: localStorageToken === loginResponse.access_token,
      bothExist: localStorageToken && sessionStorageToken
    });
  },

  // 清除认证信息
  clearAuthInfo(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('isAuthenticated');
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('isAuthenticated');
  },

  // 检查是否已认证
  isAuthenticated(): boolean {
    try {
      // 检查认证标志和token是否都存在
      const authFlagExists = localStorage.getItem('isAuthenticated') === 'true' || 
                             sessionStorage.getItem('isAuthenticated') === 'true';
      const hasToken = this.hasValidToken();
      
      const result = authFlagExists && hasToken;
      console.log('isAuthenticated result:', result, { authFlagExists, hasToken });
      return result;
    } catch (error) {
      console.error('Error checking authentication:', error);
      return false;
    }
  },

  // 获取存储的令牌
  getToken(): string | null {
    try {
      // 直接检查两个存储
      const localStorageToken = localStorage.getItem('token');
      const sessionStorageToken = sessionStorage.getItem('token');
      
      const token = localStorageToken || sessionStorageToken;
      console.log('getToken result:', { token, localStorageToken, sessionStorageToken });
      return token;
    } catch (error) {
      console.error('Error getting token:', error);
      return null;
    }
  },
  
  // 直接检查token是否有效
  hasValidToken(): boolean {
    const token = this.getToken();
    return token !== null && token.trim() !== '';
  },
};

// 其他API功能可以在这里扩展