'use client';

import { useEffect, useState } from 'react';
import { apiFetch } from '../../../lib/api';

type Analysis = {
  score: number;
  experience_level: string;
  matched_skills: string[];
  missing_skills: string[];
  recommendations: {
    skill: string;
    priority: string;
    reason: string;
    time_to_learn: string;
    experience_guidance: string;
    learning_path?: { level: string; path: string[] };
    study_schedule?: { day: string; focus: string; goal: string }[];
    learning_resources: { title: string; url: string; platform?: string }[];
    job_role_recommendations?: { title: string; url: string; platform?: string }[];
  }[];
  roadmap: string[];
};

export default function AnalysisDetailPage({ params }: { params: { id: string } }) {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    apiFetch<Analysis>(`/api/analysis/${params.id}`)
      .then(setAnalysis)
      .catch((reason: Error) => setError(reason.message));
  }, [params.id]);

  if (error) return <p className="text-red-600">Unable to load this analysis.</p>;
  if (!analysis) return <p className="text-slate-600">Loading analysis...</p>;

  return (
    <div className="space-y-6">
      <div className="rounded-3xl bg-slate-900 p-8 text-white shadow-xl">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-300">Match Score</p>
        <h1 className="mt-2 text-5xl font-bold">{analysis.score}%</h1>
        <p className="mt-2 text-sm text-slate-300">Learning plan for {analysis.experience_level} level</p>
      </div>
      <div className="grid gap-6 md:grid-cols-2">
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-bold">Matched Skills</h2>
          <div className="flex flex-wrap gap-2">
            {analysis.matched_skills.map((skill) => <span key={skill} className="rounded-full bg-emerald-100 px-3 py-1 text-sm text-emerald-700">{skill}</span>)}
          </div>
        </section>
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-bold">Skill Gaps</h2>
          <div className="flex flex-wrap gap-2">
            {analysis.missing_skills.map((skill) => <span key={skill} className="rounded-full bg-amber-100 px-3 py-1 text-sm text-amber-700">{skill}</span>)}
          </div>
        </section>
      </div>
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-bold">Learning Roadmap</h2>
        <ol className="list-decimal space-y-2 pl-6">{analysis.roadmap.map((step, index) => <li key={`${step}-${index}`}>{step}</li>)}</ol>
      </section>
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-bold">Recommendations</h2>
        <div className="space-y-4">{analysis.recommendations.map((item) => <div key={item.skill} className="border-l-4 border-sky-500 pl-4"><p className="font-semibold">{item.skill} · {item.priority}</p><p className="text-slate-600">{item.reason}</p><p className="mt-1 text-sm"><strong>Estimated time:</strong> {item.time_to_learn || '4-6 hours'}</p><p className="mt-1 text-sm"><strong>At your level:</strong> {item.experience_guidance}</p><p className="mt-1 text-sm"><strong>Learning path:</strong> {item.learning_path?.level || 'beginner'} ({item.learning_path?.path?.join(' → ')})</p><div className="mt-2"><p className="mb-2 text-sm font-semibold text-slate-700">Study schedule</p><div className="space-y-2">{item.study_schedule?.map((step: { day: string; focus: string; goal: string }) => <div key={step.day} className="rounded-xl bg-slate-50 p-3 text-sm"><p className="font-semibold text-slate-800">{step.day}</p><p>{step.focus}</p><p className="text-slate-600">Goal: {step.goal}</p></div>)}</div></div><div className="mt-2 flex flex-wrap gap-2 text-sm">{item.learning_resources.map((resource) => <a key={resource.url} href={resource.url} target="_blank" rel="noreferrer" className="rounded-full bg-sky-50 px-3 py-1 font-semibold text-sky-700 underline">{resource.platform || 'Learn'}: {resource.title}</a>)}</div>{Boolean(item.job_role_recommendations?.length) && <div className="mt-2"><p className="mb-2 text-sm font-semibold text-slate-700">Role-specific course picks</p><div className="flex flex-wrap gap-2 text-sm">{item.job_role_recommendations?.map((resource: { title: string; url: string; platform?: string }) => <a key={resource.url} href={resource.url} target="_blank" rel="noreferrer" className="rounded-full bg-emerald-50 px-3 py-1 font-semibold text-emerald-700 underline">{resource.platform || 'Course'}: {resource.title}</a>)}</div></div>}</div>)}</div>
      </section>
    </div>
  );
}
