import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="space-y-8">
      <section className="rounded-3xl bg-slate-900 p-10 text-white shadow-xl">
        <p className="mb-3 text-sm uppercase tracking-[0.2em] text-sky-300">AI Career Assistant</p>
        <h1 className="text-4xl font-bold">AI-Based Resume and Job Skill Gap Analysis System</h1>
        <p className="mt-4 max-w-2xl text-slate-200">
          Upload a resume, compare it with a target job, identify missing skills, and receive a practical learning roadmap.
        </p>
        <div className="mt-8 flex gap-4">
          <Link href="/upload" className="rounded-xl bg-sky-500 px-5 py-3 font-semibold text-white">Start Analysis</Link>
          <Link href="/jobs" className="rounded-xl border border-slate-600 px-5 py-3 font-semibold text-white">Browse Jobs</Link>
        </div>
      </section>

      <section id="how-it-works" aria-labelledby="how-it-works-title" className="scroll-mt-8 space-y-5">
        <h2 id="how-it-works-title" className="text-2xl font-bold text-slate-900">How it works</h2>
        <div className="grid gap-6 md:grid-cols-3">
        {[
          ['Upload resume', 'Support PDF and DOCX uploads with validation and extraction.'],
          ['Compare with job role', 'Match extracted skills against job requirements and weighted importance.'],
          ['Get roadmap', 'Receive missing-skill priorities and guided learning recommendations.'],
        ].map(([title, text]) => (
          <div key={title} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-3 text-xl font-semibold text-slate-900">{title}</div>
            <p className="text-slate-600">{text}</p>
          </div>
        ))}
        </div>
      </section>
    </div>
  );
}
