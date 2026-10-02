'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="mx-auto max-w-xl rounded-3xl border border-red-200 bg-red-50 p-8 text-slate-900 shadow-sm">
      <h2 className="text-2xl font-bold text-red-700">Something went wrong</h2>
      <p className="mt-3 text-sm text-red-700/80">
        {error.message || 'An unexpected error occurred while loading this page.'}
      </p>
      <button
        type="button"
        onClick={() => reset()}
        className="mt-5 rounded-xl bg-red-600 px-4 py-2 font-semibold text-white transition hover:bg-red-700"
      >
        Try again
      </button>
    </div>
  );
}
