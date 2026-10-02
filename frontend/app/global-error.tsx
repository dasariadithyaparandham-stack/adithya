'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-white">
        <div className="flex min-h-screen items-center justify-center p-6">
          <div className="max-w-xl rounded-3xl border border-red-500/40 bg-slate-900 p-8 shadow-xl">
            <h2 className="text-3xl font-bold text-red-400">Application Error</h2>
            <p className="mt-4 text-red-200">{error.message || 'An unexpected error occurred.'}</p>
            <button
              type="button"
              onClick={() => reset()}
              className="mt-6 rounded-xl bg-red-500 px-4 py-2 font-semibold text-white hover:bg-red-600"
            >
              Reload page
            </button>
          </div>
        </div>
      </body>
    </html>
  );
}
