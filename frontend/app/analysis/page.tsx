'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiFetch } from '../../lib/api';

export default function AnalysisPage() {
  const router = useRouter();
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [jobId, setJobId] = useState<number | null>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const storedResumeId = localStorage.getItem('currentResumeId');
    const storedJobId = localStorage.getItem('selectedJobId');
    if (storedResumeId) setResumeId(Number(storedResumeId));
    if (storedJobId) setJobId(Number(storedJobId));
  }, []);

  async function runAnalysis() {
    if (!resumeId || !jobId) {
      setError('Please upload a resume and choose a job first.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const data = await apiFetch('/api/analysis', {
        method: 'POST',
        body: JSON.stringify({ resume_id: resumeId, job_id: jobId }),
      });
      setAnalysis(data);
      localStorage.setItem('latestAnalysis', JSON.stringify(data));
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Unable to analyze resume.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <h1 className="mb-6 text-3xl font-bold">Run Skill Gap Analysis</h1>
      <div className="space-y-3 text-slate-700">
        <p>Resume ID: {resumeId ?? 'Not selected'}</p>
        <p>Job ID: {jobId ?? 'Not selected'}</p>
      </div>

      {error && <p className="mt-4 text-sm text-red-600">{error}</p>}

      <button
        onClick={runAnalysis}
        disabled={loading}
        className="mt-6 w-full rounded-xl bg-sky-600 px-4 py-3 font-semibold text-white disabled:bg-slate-400"
      >
        {loading ? 'Analyzing...' : 'Analyze Resume'}
      </button>
    </div>
  );
}
