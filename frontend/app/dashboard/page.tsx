'use client';

import { useEffect, useState } from 'react';
import { apiFetch } from '../../lib/api';

export default function DashboardPage() {
  const [analysis, setAnalysis] = useState<any>(null);

  useEffect(() => {
    async function loadAnalysis() {
      const saved = localStorage.getItem('latestAnalysis');
      const analysisId = saved ? JSON.parse(saved).analysis_id : null;
      if (!analysisId) return;
      try {
        const data = await apiFetch(`/api/analysis/${analysisId}`);
        setAnalysis(data);
        localStorage.setItem('latestAnalysis', JSON.stringify(data));
      } catch {
        if (saved) setAnalysis(JSON.parse(saved));
      }
    }
    loadAnalysis();
  }, []);

  if (!analysis) {
    return <p>No analysis available yet. Run an analysis first.</p>;
  }

  return (
    <div className="space-y-8">
      <div className="rounded-3xl bg-slate-900 p-8 text-white shadow-xl">
        <p className="text-sm uppercase tracking-[0.2em] text-sky-300">Match Score</p>
        <h1 className="mt-2 text-5xl font-bold">{analysis.score}%</h1>
        <p className="mt-2 text-sm text-slate-300">Learning plan for {analysis.experience_level || 'fresher'} level</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-bold">Matched Skills</h2>
          <div className="flex flex-wrap gap-2">
            {analysis.matched_skills.map((skill: string) => (
              <span key={skill} className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-medium text-emerald-700">{skill}</span>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="mb-4 text-xl font-bold">Missing Skills</h2>
          <div className="flex flex-wrap gap-2">
            {analysis.missing_skills.map((skill: string) => (
              <span key={skill} className="rounded-full bg-amber-100 px-3 py-1 text-sm font-medium text-amber-700">{skill}</span>
            ))}
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-bold">Skill Priorities</h2>
        <div className="space-y-3">
          {Object.entries(analysis.priority_summary || {}).map(([priority, items]) => (
            <div key={priority}>
              <p className="mb-2 font-semibold text-slate-700">{priority}</p>
              <div className="flex flex-wrap gap-2">
                {(items as string[]).map((item: string) => (
                  <span key={item} className="rounded-full bg-slate-100 px-2.5 py-1 text-xs text-slate-700">{item}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-bold">Recommendations</h2>
        <div className="space-y-4">
          {analysis.recommendations?.map((item: any) => (
            <div key={item.skill} className="border-l-4 border-sky-500 pl-4">
              <p className="font-semibold">{item.skill} - {item.priority}</p>
              <p className="text-slate-600">{item.reason}</p>
              <p className="mt-2 text-sm"><strong>Estimated time:</strong> {item.time_to_learn || '4-6 hours'}</p>
              <p className="mt-2 text-sm"><strong>At your level:</strong> {item.experience_guidance}</p>
              <p className="mt-2 text-sm"><strong>Learning path:</strong> {item.learning_path?.level || 'beginner'} ({item.learning_path?.path?.join(' → ')})</p>
              <p className="mt-2 text-sm"><strong>Topics:</strong> {item.topics.join(', ')}</p>
              <p className="text-sm"><strong>Practice:</strong> {item.practice}</p>
              <div className="mt-3">
                <p className="mb-2 text-sm font-semibold text-slate-700">Study schedule</p>
                <div className="space-y-2">
                  {item.study_schedule?.map((step: { day: string; focus: string; goal: string }) => (
                    <div key={step.day} className="rounded-xl bg-slate-50 p-3 text-sm">
                      <p className="font-semibold text-slate-800">{step.day}</p>
                      <p>{step.focus}</p>
                      <p className="text-slate-600">Goal: {step.goal}</p>
                    </div>
                  ))}
                </div>
              </div>
              <div className="mt-3 flex flex-wrap gap-2 text-sm">
                {item.learning_resources?.map((resource: { title: string; url: string; platform?: string }) => (
                  <a key={resource.url} href={resource.url} target="_blank" rel="noreferrer" className="rounded-full bg-sky-50 px-3 py-1 font-semibold text-sky-700 underline">
                    {resource.platform || 'Learn'}: {resource.title}
                  </a>
                ))}
              </div>
              {item.job_role_recommendations?.length > 0 && (
                <div className="mt-3">
                  <p className="mb-2 text-sm font-semibold text-slate-700">Role-specific course picks</p>
                  <div className="flex flex-wrap gap-2 text-sm">
                    {item.job_role_recommendations.map((resource: { title: string; url: string; platform?: string }) => (
                      <a key={resource.url} href={resource.url} target="_blank" rel="noreferrer" className="rounded-full bg-emerald-50 px-3 py-1 font-semibold text-emerald-700 underline">{resource.platform || 'Course'}: {resource.title}</a>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-xl font-bold">Learning Roadmap</h2>
        <ol className="list-decimal space-y-2 pl-6 text-slate-700">
          {analysis.roadmap?.map((item: string, index: number) => <li key={item + index}>{item}</li>)}
        </ol>
      </div>
    </div>
  );
}
