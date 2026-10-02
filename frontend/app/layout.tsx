import './globals.css';
import Link from 'next/link';
import ThemeToggle from '../components/theme-toggle';
import AuthControls from '../components/auth-controls';

export const metadata = {
  title: 'Resume Skill Gap Analysis',
  description: 'AI-based resume and job skill gap analysis system',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-slate-200 bg-white/80 backdrop-blur-sm dark:border-slate-800 dark:bg-slate-950/80">
          <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
            <div className="flex flex-col items-start">
              <Link href="/" className="text-xl font-bold text-slate-900 dark:text-white">SkillGap AI</Link>
              <Link href="/#how-it-works" className="mt-1 rounded-md border border-sky-700 px-2 py-1 text-xs font-semibold text-sky-800 transition hover:bg-sky-50 dark:text-sky-300 dark:hover:bg-slate-800">How it works</Link>
            </div>
            <div className="flex flex-wrap items-center justify-end gap-4 text-sm font-medium text-slate-700 dark:text-slate-300">
              <Link href="/upload">Upload</Link>
              <Link href="/jobs">Jobs</Link>
              <Link href="/analysis">Analysis</Link>
              <Link href="/dashboard">Dashboard</Link>
              <Link href="/history">History</Link>
              <AuthControls />
              <ThemeToggle />
            </div>
          </nav>
        </header>
        <main className="mx-auto max-w-6xl px-6 py-10">{children}</main>
      </body>
    </html>
  );
}
