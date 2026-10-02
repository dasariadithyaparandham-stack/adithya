const resolveApiBaseUrl = () => {
  const configuredUrl = process.env.NEXT_PUBLIC_API_URL;
  if (configuredUrl && configuredUrl.trim()) return configuredUrl.trim().replace(/\/$/, '');

  if (typeof window !== 'undefined') {
    const host = window.location.hostname;
    if (host === 'localhost' || host === '127.0.0.1' || host === '0.0.0.0') {
      return 'http://localhost:8000';
    }
  }

  return 'http://localhost:8000';
};

export const API_BASE_URL = resolveApiBaseUrl();

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const isFormData = typeof FormData !== 'undefined' && options.body instanceof FormData;
  const token = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(isFormData ? {} : { 'Content-Type': 'application/json' }),
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    let errorMessage = errorText || 'Request failed';
    try {
      const errorBody = JSON.parse(errorText);
      errorMessage = errorBody.detail || errorMessage;
    } catch {}
    throw new Error(errorMessage);
  }

  return response.json() as Promise<T>;
}
