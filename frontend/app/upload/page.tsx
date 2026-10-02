'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiFetch } from '../../lib/api';

export default function UploadPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [isSignedIn, setIsSignedIn] = useState(false);

  useEffect(() => {
    setIsSignedIn(Boolean(localStorage.getItem('accessToken')));
  }, []);

  async function handleUpload() {
    if (!file) {
      setMessage('Please choose a PDF or DOCX resume.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    setIsLoading(true);
    setMessage('');

    try {
      const data = await apiFetch<{ resume_id: number; filename: string }>('/api/resume/upload', { method: 'POST', body: formData });

      localStorage.setItem('currentResumeId', String(data.resume_id));
      localStorage.setItem('currentResumeName', data.filename);
      setMessage('Resume uploaded successfully.');
      router.push('/jobs');
    } catch (error: any) {
      setMessage(error.message || 'There was a problem uploading the file.');
    } finally {
      setIsLoading(false);
    }
  }

  if (!isSignedIn) {
    return (
      <section className="max-w-xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-bold">Sign in to upload your resume</h1>
        <p className="mt-2 text-slate-600">Your analyses and learning recommendations will be saved to your account.</p>
        <Link href="/auth" className="mt-5 inline-flex rounded-lg bg-sky-700 px-4 py-2.5 font-semibold text-white">Create account or sign in</Link>
      </section>
    );
  }

  return (
    <div className="max-w-xl rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <h1 className="mb-6 text-3xl font-bold">Upload a Resume</h1>
      <input
        type="file"
        accept=".pdf,.docx"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4 block w-full rounded-xl border border-slate-300 p-3"
      />

      <button
        onClick={handleUpload}
        disabled={isLoading}
        className="w-full rounded-xl bg-sky-600 px-4 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-400"
      >
        {isLoading ? 'Uploading...' : 'Upload Resume'}
      </button>

      {message && <p className="mt-4 text-sm text-slate-700">{message}</p>}
    </div>
  );
}
