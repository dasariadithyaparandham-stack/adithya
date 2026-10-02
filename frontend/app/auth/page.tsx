'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiFetch } from '../../lib/api';

type AuthResult = {
  access_token: string;
  user: { id: number; name: string; email: string; experience_level: string };
};

export default function AuthPage() {
  const router = useRouter();
  const [mode, setMode] = useState<'register' | 'login'>('register');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('fresher');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = mode === 'register' ? '/api/auth/register' : '/api/auth/login';
      const payload = mode === 'register'
        ? { name, email, password, experience_level: experienceLevel }
        : { email, password };
      const result = await apiFetch<AuthResult>(endpoint, { method: 'POST', body: JSON.stringify(payload) });
      localStorage.setItem('accessToken', result.access_token);
      localStorage.setItem('currentUser', JSON.stringify(result.user));
      window.dispatchEvent(new Event('auth-changed'));
      router.push('/upload');
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Unable to sign in.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-lg rounded-2xl border border-slate-200 bg-white p-7 shadow-sm sm:p-9">
      <div className="mb-7 flex border-b border-slate-200">
        <button type="button" onClick={() => setMode('register')} className={`border-b-2 px-4 py-3 text-sm font-semibold ${mode === 'register' ? 'border-sky-600 text-sky-700' : 'border-transparent text-slate-500'}`}>Create account</button>
        <button type="button" onClick={() => setMode('login')} className={`border-b-2 px-4 py-3 text-sm font-semibold ${mode === 'login' ? 'border-sky-600 text-sky-700' : 'border-transparent text-slate-500'}`}>Sign in</button>
      </div>

      <h1 className="text-2xl font-bold text-slate-900">{mode === 'register' ? 'Create your account' : 'Welcome back'}</h1>
      <p className="mt-2 text-sm text-slate-600">Your resume analyses and learning plan are saved to your account.</p>

      <form onSubmit={submit} className="mt-6 space-y-4">
        {mode === 'register' && (
          <>
            <label className="block text-sm font-semibold text-slate-700">Name
              <input required value={name} onChange={(event) => setName(event.target.value)} autoComplete="name" className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2.5 font-normal" />
            </label>
            <fieldset>
              <legend className="text-sm font-semibold text-slate-700">Experience level</legend>
              <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-3">
                {[
                  { value: 'fresher', label: 'Fresher', detail: 'Starting out' },
                  { value: 'intermediate', label: 'Intermediate', detail: 'Building experience' },
                  { value: 'experienced', label: 'Experienced', detail: 'Advanced practice' },
                ].map((level) => (
                  <label key={level.value} className={`cursor-pointer rounded-lg border p-3 ${experienceLevel === level.value ? 'border-sky-600 bg-sky-50' : 'border-slate-200'}`}>
                    <input className="sr-only" type="radio" name="experience" value={level.value} checked={experienceLevel === level.value} onChange={() => setExperienceLevel(level.value)} />
                    <span className="block text-sm font-semibold">{level.label}</span>
                    <span className="mt-1 block text-xs text-slate-500">{level.detail}</span>
                  </label>
                ))}
              </div>
            </fieldset>
          </>
        )}
        <label className="block text-sm font-semibold text-slate-700">Email
          <input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} autoComplete="email" className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2.5 font-normal" />
        </label>
        <label className="block text-sm font-semibold text-slate-700">Password
          <input required minLength={mode === 'register' ? 8 : 1} type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete={mode === 'register' ? 'new-password' : 'current-password'} className="mt-1.5 block w-full rounded-lg border border-slate-300 px-3 py-2.5 font-normal" />
          {mode === 'register' && <span className="mt-1 block text-xs font-normal text-slate-500">Use at least 8 characters.</span>}
        </label>
        {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
        <button disabled={loading} className="w-full rounded-lg bg-sky-700 px-4 py-3 font-semibold text-white hover:bg-sky-800 disabled:opacity-60">
          {loading ? 'Please wait...' : mode === 'register' ? 'Create account' : 'Sign in'}
        </button>
      </form>
    </main>
  );
}