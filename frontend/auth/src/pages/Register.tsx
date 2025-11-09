import React, { useState } from 'react'

export default function Register({ onRegistered }: { onRegistered?: () => void }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [ok, setOk] = useState(false)

  async function submit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      const res = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })
      if (!res.ok) {
        const j = await res.json().catch(() => ({}))
        setError(j.detail || 'Register failed')
        return
      }
      setOk(true)
      onRegistered && onRegistered()
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
      {ok && <div className="text-sm text-green-600">Registered — you can now login</div>}
      <div className="flex justify-end">
        <button className="px-4 py-2 bg-sky-600 text-white rounded" type="submit">Register</button>
      </div>
    </form>
  )
}
