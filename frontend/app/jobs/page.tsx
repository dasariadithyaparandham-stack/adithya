'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiFetch } from '../../lib/api';

type Job = {
  id: number;
  title: string;
  description: string;
  required_skills: Array<{ name: string; importance: number }>;
};

type Company = {
  name: string;
  industry: string;
  roles: string[];
  match_score: number;
  matched_skills: string[];
};

export default function JobsPage() {
  const router = useRouter();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [targetJobId, setTargetJobId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadJobs() {
      try {
        const data = await apiFetch<Job[]>('/api/jobs');
        setJobs(data);
        const savedJobId = localStorage.getItem('selectedJobId');
        const initialJobId = savedJobId ? Number(savedJobId) : data[0]?.id;
        if (initialJobId) setTargetJobId(initialJobId);
      } finally {
        setLoading(false);
      }
    }
    loadJobs();
  }, []);

  useEffect(() => {
    async function loadCompanies() {
      const resumeId = localStorage.getItem('currentResumeId');
      if (!resumeId || !targetJobId) return;
      const companyData = await apiFetch<{ companies: Company[] }>(`/api/resume/${resumeId}/companies?job_id=${targetJobId}`);
      setCompanies(companyData.companies);
    }
    loadCompanies().catch(() => setCompanies([]));
  }, [targetJobId]);

  function selectJob(jobId: number) {
    localStorage.setItem('selectedJobId', String(jobId));
    setTargetJobId(jobId);
    router.push('/analysis');
  }

  if (loading) return <p>Loading jobs...</p>;

  return (
    <div className="space-y-6">
      {companies.length > 0 && (
        <section className="rounded-3xl bg-slate-900 p-6 text-white shadow-xl">
          <div className="flex flex-wrap items-end justify-between gap-3">
            <div>
              <p className="text-sm uppercase tracking-[0.18em] text-sky-300">Resume-based matches</p>
              <h1 className="mt-1 text-2xl font-bold">Companies aligned with your skills</h1>
            </div>
            <p className="max-w-sm text-sm text-slate-300">Profile matches from detected resume skills, not live vacancy listings.</p>
          </div>
          <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {companies.map((company) => (
              <article key={company.name} className="rounded-2xl border border-slate-700 bg-slate-800 p-5">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h2 className="text-lg font-bold">{company.name}</h2>
                    <p className="mt-1 text-sm text-slate-300">{company.industry}</p>
                  </div>
                  <span className="rounded-full bg-emerald-400/15 px-2.5 py-1 text-sm font-semibold text-emerald-300">{company.match_score}%</span>
                </div>
                <p className="mt-4 text-xs uppercase tracking-[0.12em] text-slate-400">Relevant roles</p>
                <p className="mt-1 text-sm text-slate-200">{company.roles.slice(0, 3).join(' · ')}</p>
                <div className="mt-4 flex flex-wrap gap-2">
                  {company.matched_skills.map((skill) => <span key={`${company.name}-${skill}`} className="rounded-full bg-slate-700 px-2.5 py-1 text-xs text-sky-100">{skill}</span>)}
                </div>
              </article>
            ))}
          </div>
        </section>
      )}
      <h1 className="text-3xl font-bold">Choose Target Job Role</h1>
      <label className="block max-w-md text-sm font-semibold text-slate-700">
        Target role for company matches
        <select value={targetJobId ?? ''} onChange={(event) => setTargetJobId(Number(event.target.value))} className="mt-2 block w-full rounded-xl border border-slate-300 bg-white px-3 py-3 font-normal">
          {jobs.map((job) => <option key={job.id} value={job.id}>{job.title}</option>)}
        </select>
      </label>
      <div className="grid gap-5 md:grid-cols-2">
        {jobs.map((job) => (
          <div key={job.id} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-3 flex items-center justify-between gap-4">
              <h2 className="text-2xl font-bold text-slate-900">{job.title}</h2>
              <button
                onClick={() => selectJob(job.id)}
                className="rounded-xl bg-sky-600 px-4 py-2 text-sm font-semibold text-white"
              >
                Select
              </button>
            </div>
            <p className="mb-4 text-slate-600">{job.description}</p>
            <div className="flex flex-wrap gap-2">
              {job.required_skills.slice(0, 6).map((skill) => (
                <span key={`${job.id}-${skill.name}`} className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700">
                  {skill.name}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
