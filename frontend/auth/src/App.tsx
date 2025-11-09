import React, { useState } from 'react'
import Login from './pages/Login'
import Register from './pages/Register'
import TokenView from './components/TokenView'

export default function App() {
  const [token, setToken] = useState<string | null>(null)
  const [view, setView] = useState<'login' | 'register' | 'token'>('login')

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-white dark:bg-slate-800 rounded-lg shadow p-6">
        <div className="flex gap-4 mb-4">
          <button className={`px-3 py-1 rounded ${view==='login'? 'bg-sky-600 text-white' : 'bg-slate-100'}`} onClick={()=>setView('login')}>Login</button>
          <button className={`px-3 py-1 rounded ${view==='register'? 'bg-sky-600 text-white' : 'bg-slate-100'}`} onClick={()=>setView('register')}>Register</button>
        </div>

        {view === 'login' && (
          <Login onToken={(t) => { setToken(t); setView('token') }} />
        )}
        {view === 'register' && (
          <Register onRegistered={() => setView('login')} />
        )}
        {view === 'token' && token && (
          <TokenView token={token} onLogout={() => { setToken(null); setView('login') }} />
        )}
      </div>
    </div>
  )
}
