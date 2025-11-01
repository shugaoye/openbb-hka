import { useState } from 'react'
import Taro from '@tarojs/taro'
import { api, setToken } from '@/utils/api'
import '../../styles.css'

export default function Login(){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const onSubmit = async () => {
    try{
      setLoading(true)
      const res = await api.login({ username, password })
      setToken(res.access_token)
      Taro.showToast({ title: 'Login success', icon: 'success' })
      Taro.redirectTo({ url: '/pages/token/index' })
    }catch(e:any){
      Taro.showToast({ title: e.message || 'Login failed', icon: 'none' })
    }finally{ setLoading(false) }
  }

  const onWxLogin = async () => {
    try{
      setLoading(true)
      const res = await api.wechatLogin()
      setToken(res.access_token)
      Taro.redirectTo({ url: '/pages/token/index' })
    }catch(e:any){
      Taro.showToast({ title: e.message || 'WeChat login failed', icon: 'none' })
    }finally{ setLoading(false) }
  }

  return (
    <div className='container'>
      <div className='card stack'>
        <h2>Login</h2>
        <input className='input' placeholder='Username' value={username} onChange={(e:any)=>setUsername(e.target.value)} />
        <input className='input' type='password' placeholder='Password' value={password} onChange={(e:any)=>setPassword(e.target.value)} />
        <button className='btn' disabled={loading} onClick={onSubmit}>Login</button>
        <button className='btn secondary' disabled={loading} onClick={onWxLogin}>WeChat Login</button>
        <div>
          No account? <a href='/pages/register/index'>Register</a>
        </div>
      </div>
    </div>
  )
}
