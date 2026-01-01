type DashboardSummary = {
  total_visible_documents: number;
  processed_documents: number;
  documents_needing_review: number;
  latest_activity_at: string | null;
};

function getApiBaseUrl() {
  const serverBase = process.env.API_BASE_URL;
  const publicBase = process.env.NEXT_PUBLIC_API_BASE_URL;
  const base = serverBase ?? publicBase ?? "";
  return base.replace(/\/+$/, "");
}

export async function fetchDashboardSummary(): Promise<DashboardSummary> {
  const base = getApiBaseUrl();
  if (!base) {
    throw new Error("API base URL is empty");
  }

  const res = await fetch(`${base}/api/dashboard/summary`, {
    cache: "no-store",
    headers: { Accept: "application/json" },
  });

  if (!res.ok) {
    const body = await res.text().catch(() => "<unreadable body>");
    throw new Error(`HTTP ${res.status}\n${body}`);
  }

  return res.json();
}
