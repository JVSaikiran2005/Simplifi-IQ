import { useState, type ChangeEvent, type FormEvent } from "react";

const DEFAULT_API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

interface FormState {
  full_name: string;
  email: string;
  company_name: string;
  company_website: string;
}

export default function Home() {
  const [values, setValues] = useState<FormState>({
    full_name: "",
    email: "",
    company_name: "",
    company_website: "",
  });
  const [status, setStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (field: keyof FormState) => (event: ChangeEvent<HTMLInputElement>) => {
    setValues((current) => ({ ...current, [field]: event.target.value }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setStatus(null);
    setError(null);

    try {
      const response = await fetch(`${DEFAULT_API_URL}/api/leads`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });

      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.detail || "Submission failed.");
      }

      setStatus("Lead submitted successfully. Processing has started and the audit will arrive by email shortly.");
      setValues({ full_name: "", email: "", company_name: "", company_website: "" });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-4xl rounded-3xl bg-white p-8 shadow-xl shadow-slate-200/50">
        <div className="mb-8 grid gap-6 md:grid-cols-2 md:items-center">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-brand-700">Lead Automation</p>
            <h1 className="mt-4 text-4xl font-semibold text-slate-900">Automated AI Audit Report Workflow</h1>
            <p className="mt-4 text-slate-600">Capture leads, enrich their website, generate a professional audit report, and email it automatically.</p>
          </div>
          <div className="rounded-3xl bg-brand-900 p-6 text-white shadow-lg shadow-brand-500/10">
            <p className="text-sm uppercase tracking-[0.28em] text-brand-300">How it works</p>
            <ul className="mt-4 space-y-3 text-sm leading-7">
              <li>1. Validate lead details</li>
              <li>2. Scrape website and extract metadata</li>
              <li>3. Use AI to create a consulting-grade report</li>
              <li>4. Generate PDF and email the prospect</li>
            </ul>
          </div>
        </div>

        <form className="space-y-6" onSubmit={handleSubmit}>
          <div className="grid gap-6 sm:grid-cols-2">
            <label className="block">
              <span className="text-sm font-medium text-slate-900">Full name</span>
              <input
                type="text"
                value={values.full_name}
                onChange={handleChange("full_name")}
                disabled={loading}
                required
                className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
              />
            </label>
            <label className="block">
              <span className="text-sm font-medium text-slate-900">Email address</span>
              <input
                type="email"
                value={values.email}
                onChange={handleChange("email")}
                disabled={loading}
                required
                className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
              />
            </label>
          </div>

          <div className="grid gap-6 sm:grid-cols-2">
            <label className="block sm:col-span-2">
              <span className="text-sm font-medium text-slate-900">Company name</span>
              <input
                type="text"
                value={values.company_name}
                onChange={handleChange("company_name")}
                disabled={loading}
                required
                className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
              />
            </label>
            <label className="block sm:col-span-2">
              <span className="text-sm font-medium text-slate-900">Company website</span>
              <input
                type="url"
                value={values.company_website}
                onChange={handleChange("company_website")}
                disabled={loading}
                required
                placeholder="https://example.com"
                className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
              />
            </label>
          </div>

          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="text-sm text-slate-600">Professional automation for sales-ready lead intake.</div>
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center justify-center rounded-2xl bg-brand-900 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-500/20 transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Processing lead…" : "Submit lead"}
            </button>
          </div>

          {status && <div className="rounded-3xl border border-emerald-300 bg-emerald-50 p-4 text-sm text-emerald-900">{status}</div>}
          {error && <div className="rounded-3xl border border-rose-300 bg-rose-50 p-4 text-sm text-rose-900">{error}</div>}
        </form>
      </div>
    </main>
  );
}
