import React from 'react'

export default function TokenView({ token, onLogout }: { token: string, onLogout?: () => void }) {
  function copy() {
    navigator.clipboard.writeText(token)
  }
  return (
    <div className="space-y-4">
      <div className="text-sm text-slate-500">Copy this token into OpenBB Workspace or use it for authenticated requests.</div>
      <pre className="p-3 bg-slate-100 rounded break-all">{token}</pre>
      <div className="flex gap-2 justify-end">
        <button onClick={copy} className="px-3 py-1 bg-slate-200 rounded">Copy</button>
        <button onClick={onLogout} className="px-3 py-1 bg-rose-500 text-white rounded">Logout</button>
      </div>
    </div>
  )
}
