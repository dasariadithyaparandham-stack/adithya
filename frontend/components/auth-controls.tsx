'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

type Account = { name: string };

export default function AuthControls() {
  const [account, setAccount] = useState<Account | null>(null);

  useEffect(() => {
    function syncAccount() {
      const savedAccount = localStorage.getItem('currentUser');
      setAccount(savedAccount ? JSON.parse(savedAccount) as Account : null);
    }

    syncAccount();
    window.addEventListener('auth-changed', syncAccount);
    return () => window.removeEventListener('auth-changed', syncAccount);
  }, []);

  function signOut() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('currentUser');
    setAccount(null);
    window.dispatchEvent(new Event('auth-changed'));
  }

  if (!account) return <Link href="/auth">Sign in</Link>;

  return (
    <div className="flex items-center gap-3">
      <span className="max-w-28 truncate text-slate-500" title={account.name}>{account.name}</span>
      <button type="button" onClick={signOut} className="font-semibold text-sky-700 hover:text-sky-900">Sign out</button>
    </div>
  );
}