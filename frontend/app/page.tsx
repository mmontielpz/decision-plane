// frontend/app/page.tsx

export const dynamic = "force-dynamic";

import Link from "next/link";
import { fetchDocuments } from "@/services/documents";
import { DocumentRow } from "@/types/document";
import styles from "./page.module.css";

export default async function HomePage() {
  let documents: DocumentRow[] = [];

  try {
    documents = await fetchDocuments();
  } catch {
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
    <main className={styles.container}>
      <h1 className={styles.title}>Risk-Aware ML System</h1>

      {/* Metrics */}
      <section className={styles.metricsGrid}>
        <div className={styles.card}>
          <div className={styles.cardLabel}>Total Documents</div>
          <div className={styles.cardValue}>{total}</div>
        </div>

        <div className={styles.card}>
          <div className={styles.cardLabel}>Processed</div>
          <div className={styles.cardValue}>{processed}</div>
        </div>

        <div className={styles.card}>
          <div className={styles.cardLabel}>Needs Review</div>
          <div className={styles.cardValue}>{needsReview}</div>
        </div>
      </section>

      {/* Primary action */}
      <section className={styles.primaryActionSection}>
        <Link href="/documents" className={styles.primaryButton}>
          View Documents
        </Link>
      </section>

      {/* Latest document */}
      <section>
        <h2 className={styles.latestTitle}>Latest Document</h2>

        {latestDocument ? (
          <Link
            href={`/documents/${latestDocument.document_id}`}
            className={styles.latestCardLink}
          >
            <strong>{latestDocument.document_id}</strong>
            <div className={styles.muted}>
              Status: {latestDocument.status}
            </div>
          </Link>
        ) : (
          <p>No documents ingested yet.</p>
        )}
      </section>
    </main>
  );
}
