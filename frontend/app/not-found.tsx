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
        Page not found
      </h1>

      <p style={{ marginBottom: "1.5rem", color: "#555" }}>
        The page you are looking for does not exist or has been moved.
      </p>

      <Link
        href="/"
        style={{
          textDecoration: "none",
          color: "#000",
          fontWeight: 500,
        }}
      >
        ← Back to Home
      </Link>
    </main>
  );
}
