// frontend/app/error.tsx

"use client";

import { useEffect } from "react";
import Link from "next/link";

type Props = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function GlobalError({ error, reset }: Props) {
  useEffect(() => {
    // Aquí podrías enviar el error a un logger externo
    console.error(error);
  }, [error]);

  return (
    <main
      style={{
        padding: "2.5rem",
        maxWidth: "900px",
        margin: "0 auto",
      }}
    >
      <h1 style={{ fontSize: "1.75rem", marginBottom: "1rem" }}>
        Something went wrong
      </h1>

      <p style={{ marginBottom: "1.5rem", color: "#555" }}>
        An unexpected error occurred. You can try again or return home.
      </p>

      <div style={{ display: "flex", gap: "1rem" }}>
        <button
          onClick={() => reset()}
          style={{
            padding: "0.6rem 1rem",
            borderRadius: "6px",
            border: "1px solid #000",
            background: "#000",
            color: "#fff",
            cursor: "pointer",
          }}
        >
          Retry
        </button>

        <Link
          href="/"
          style={{
            alignSelf: "center",
            textDecoration: "none",
            color: "#000",
            fontWeight: 500,
          }}
        >
          ← Back to Home
        </Link>
      </div>
    </main>
  );
}
