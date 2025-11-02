export interface User {
  id: string;
  username: string;
  email?: string;
  wechatId?: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData extends LoginCredentials {
  email?: string;
}