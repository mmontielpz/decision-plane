// frontend/app/page.tsx

export const dynamic = "force-dynamic";

import Link from "next/link";
import { fetchDocuments } from "@/services/documents";
import { DocumentRow } from "@/types/document";

export default async function HomePage() {
  let documents: DocumentRow[] = [];

  try {
    documents = await fetchDocuments();
  } catch {
    // Home should not crash; show empty state instead
    documents = [];
  }

  const total = documents.length;
  const processed = documents.filter(d => d.status === "processed").length;
  const needsReview = documents.filter(d => d.decision === "REVIEW").length;

  const latestDocument = documents
    .slice()
    .sort((a, b) => {
      if (!a.last_updated || !b.last_updated) return 0;
      return new Date(b.last_updated).getTime() - new Date(a.last_updated).getTime();
    })[0];

  return (
    <main style={{ padding: "2rem" }}>
      <h1>Risk-Aware ML System</h1>

      <section style={{ marginTop: "2rem" }}>
        <h2>System Overview</h2>
        <ul>
          <li>Total documents: {total}</li>
          <li>Processed: {processed}</li>
          <li>Needs review: {needsReview}</li>
        </ul>
      </section>

      <section style={{ marginTop: "2rem" }}>
        <Link href="/documents">
          View Documents
        </Link>
      </section>

      <section style={{ marginTop: "2rem" }}>
        <h3>Latest Document</h3>
        {latestDocument ? (
          <Link href={`/documents/${latestDocument.document_id}`}>
            {latestDocument.document_id}
          </Link>
        ) : (
          <p>No documents ingested yet.</p>
        )}
      </section>
    </main>
  );
}
