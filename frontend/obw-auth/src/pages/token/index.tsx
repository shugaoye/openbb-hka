import { useEffect, useState } from 'react'
import Taro from '@tarojs/taro'
import { getToken } from '@/utils/api'
import '../../styles.css'

export default function Token(){
  const [token, setToken] = useState('')

  useEffect(()=>{
    const t = getToken()
    if (t) setToken(t)
  },[])

  const copy = async () => {
    try{
      await Taro.setClipboardData({ data: token })
      Taro.showToast({ title: 'Copied', icon: 'success' })
    }catch{}
  }

  return (
    <div className='container'>
      <div className='card stack'>
        <h2>JWT Token</h2>
        <textarea rows={6} value={token} readOnly />
        <button className='btn' onClick={copy}>Copy</button>
        <p>Use this token as APP_API_KEY in OpenBB Workspace or call /auth/token to view in browser.</p>
      </div>
    </div>
  )
}
