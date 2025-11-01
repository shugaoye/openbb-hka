import { useState } from 'react'
import Taro from '@tarojs/taro'
import { api, setToken } from '@/utils/api'
import '../../styles.css'

export default function Register(){
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)

  const onSubmit = async () => {
    try{
      setLoading(true)
      const res = await api.register({ username, password, email })
      setToken(res.access_token)
      Taro.showToast({ title: 'Registered', icon: 'success' })
      Taro.redirectTo({ url: '/pages/token/index' })
    }catch(e:any){
      Taro.showToast({ title: e.message || 'Register failed', icon: 'none' })
    }finally{ setLoading(false) }
  }

  return (
    <div className='container'>
      <div className='card stack'>
        <h2>Register</h2>
        <input className='input' placeholder='Username' value={username} onChange={(e:any)=>setUsername(e.target.value)} />
        <input className='input' placeholder='Email (optional)' value={email} onChange={(e:any)=>setEmail(e.target.value)} />
        <input className='input' type='password' placeholder='Password' value={password} onChange={(e:any)=>setPassword(e.target.value)} />
        <button className='btn' disabled={loading} onClick={onSubmit}>Create account</button>
      </div>
    </div>
  )
}
