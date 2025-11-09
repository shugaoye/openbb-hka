import React, { useState } from 'react'

export default function Login({ onToken }: { onToken: (token: string) => void }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      const form = new URLSearchParams()
      form.append('username', username)
      form.append('password', password)
      const res = await fetch('/auth/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: form.toString(),
      })
      if (!res.ok) {
        const j = await res.json().catch(() => ({}))
        setError(j.detail || 'Login failed')
        return
      }
      const data = await res.json()
      if (data.access_token) {
        onToken(data.access_token)
      } else {
        setError('no token in response')
      }
    } catch (e: any) {
      setError(e?.message || String(e))
    }
  }

  return (
    <form onSubmit={submit} className="space-y-4">
      <div>
        <label className="block text-sm">Username</label>
        <input className="w-full mt-1 p-2 border rounded" value={username} onChange={e=>setUsername(e.target.value)} />
      </div>
      <div>
        <label className="block text-sm">Password</label>
        <input type="password" className="w-full mt-1 p-2 border rounded" value={password} onChange={e=>setPassword(e.target.value)} />
      </div>
      {error && <div className="text-sm text-red-600">{error}</div>}
      <div className="flex justify-end">
        <button className="px-4 py-2 bg-sky-600 text-white rounded" type="submit">Login</button>
      </div>
    </form>
  )
}
