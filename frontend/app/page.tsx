// frontend/app/page.tsx

export const dynamic = "force-dynamic";

import { fetchDashboardSummary } from "@/services/dashboard";
import Link from "next/link";

/* -------------------------
 * Local UI helpers
 * ------------------------- */
function formatTimestamp(ts: string | null): string {
  if (!ts) return "-";

  const date = new Date(ts);
  if (isNaN(date.getTime())) return ts;

  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, "0");
  const dd = String(date.getDate()).padStart(2, "0");
  const hh = String(date.getHours()).padStart(2, "0");
  const min = String(date.getMinutes()).padStart(2, "0");

  return `${yyyy}-${mm}-${dd} ${hh}:${min}`;
}

/* -------------------------
 * Page
 * ------------------------- */
export default async function HomePage() {
  let summary;
  let error: string | null = null;

  try {
    summary = await fetchDashboardSummary();
  } catch {
    error = "Unable to load dashboard";
  }

  return (
    <main style={{ padding: "2rem", maxWidth: "900px", margin: "0 auto" }}>
      <h1>Dashboard</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {!error && summary && (
        <>
          <section
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(4, 1fr)",
              gap: "1rem",
              marginTop: "1rem",
            }}
          >
            <MetricCard
              title="Total Documents"
              value={summary.total_visible_documents}
            />
            <MetricCard
              title="Processed"
              value={summary.processed_documents}
            />
            <MetricCard
              title="Needs Review"
              value={summary.documents_needing_review}
            />
            <MetricCard
              title="Latest Activity"
              value={formatTimestamp(summary.latest_activity_at)}
            />
          </section>

          <section style={{ marginTop: "2rem" }}>
            <Link href="/documents">View documents →</Link>
          </section>
        </>
      )}
    </main>
  );
}

/* -------------------------
 * Components
 * ------------------------- */
function MetricCard({
  title,
  value,
}: {
  title: string;
  value: string | number;
}) {
  return (
    <div
      style={{
        border: "1px solid #eee",
        borderRadius: "6px",
        padding: "1rem",
      }}
    >
      <div style={{ fontSize: "0.9rem", color: "#666" }}>{title}</div>
      <div style={{ fontSize: "1.4rem", fontWeight: 600 }}>{value}</div>
    </div>
  );
}
