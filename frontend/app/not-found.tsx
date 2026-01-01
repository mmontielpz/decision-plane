// frontend/app/not-found.tsx

import Link from "next/link";

export default function NotFound() {
  return (
    <main
      style={{
        padding: "2.5rem",
        maxWidth: "900px",
        margin: "0 auto",
      }}
    >
      <h1 style={{ fontSize: "1.75rem", marginBottom: "1rem" }}>
        Document not available
      </h1>

      <p style={{ marginBottom: "1.5rem", color: "#555" }}>
        This document does not exist or is not ready to be viewed yet.
      </p>

      <Link
        href="/documents"
        style={{
          textDecoration: "none",
          color: "#000",
          fontWeight: 500,
        }}
      >
        ← Back to documents
      </Link>
    </main>
  );
}
