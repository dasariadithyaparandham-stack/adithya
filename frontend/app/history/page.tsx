'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiFetch } from '../../lib/api';

type AnalysisHistory = {
  analysis_id: number;
  job_title: string;
  score: number;
  created_at: string;
};

export default function HistoryPage() {
  const [history, setHistory] = useState<AnalysisHistory[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  async function loadHistory() {
    try {
      const data = await apiFetch<AnalysisHistory[]>('/api/history');
      setHistory(data);
      setError('');
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Unable to load your saved analyses.');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  async function handleDelete(analysisId: number) {
    const confirmed = window.confirm('Delete this analysis from your history?');
    if (!confirmed) return;

    try {
      await apiFetch(`/api/history/${analysisId}`, {
        method: 'DELETE',
      });
      setHistory((current) => current.filter((item) => item.analysis_id !== analysisId));
    } catch (error) {
      console.error('Failed to delete analysis', error);
      alert('Unable to delete the selected analysis.');
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Previous Analyses</h1>
      {error && <p role="alert" className="rounded-lg border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">{error} <Link href="/auth" className="font-semibold underline">Sign in</Link></p>}
      <div className="space-y-4">
        {loading ? (
          <p className="text-slate-600">Loading saved analyses...</p>
        ) : history.length === 0 && !error ? (
          <p className="text-slate-600">No analyses yet.</p>
        ) : !error && (
          history.map((item) => (
            <div key={item.analysis_id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-sky-400">
              <div className="flex items-center justify-between gap-4">
                <Link href={`/analysis/${item.analysis_id}`} className="flex-1">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold">{item.job_title}</h2>
                    <span className="rounded-full bg-sky-100 px-3 py-1 text-sm font-semibold text-sky-700">{item.score}%</span>
                  </div>
                  <p className="mt-2 text-sm text-slate-600">Created: {new Date(item.created_at).toLocaleString()}</p>
                </Link>

                <button
                  type="button"
                  onClick={() => handleDelete(item.analysis_id)}
                  className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm font-medium text-red-600 transition hover:bg-red-100"
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
