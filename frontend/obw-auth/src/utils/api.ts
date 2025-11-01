import Taro from '@tarojs/taro'

const BASE_URL = process.env.TARO_APP_API_BASE || 'http://localhost:8000'

export function setToken(token: string){
  Taro.setStorageSync('token', token)
}
export function getToken(): string | null{
  try { return Taro.getStorageSync('token') || null } catch { return null }
}

export async function request<T>(url: string, options: Partial<Taro.request.Option> = {}): Promise<T>{
  const token = getToken()
  const headers = {
    'Content-Type': 'application/json',
    ...(options.header || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  }
  const res = await Taro.request<T>({ url: `${BASE_URL}${url}`, method: 'GET', ...options, header: headers })
  if ((res.statusCode || 0) >= 400) throw new Error(typeof res.data === 'string' ? res.data : JSON.stringify(res.data))
  return res.data as T
}

export const api = {
  register: (payload: {username: string; password: string; email?: string}) => request<{access_token: string}>(`/auth/register`, { method: 'POST', data: payload }),
  login: (payload: {username: string; password: string}) => request<{access_token: string}>(`/auth/login`, { method: 'POST', data: payload }),
  wechatLogin: async () => {
    const loginRes = await Taro.login()
    const code = loginRes.code
    return request<{access_token: string}>(`/auth/wechat/login`, { method: 'POST', data: { code } })
  },
}
