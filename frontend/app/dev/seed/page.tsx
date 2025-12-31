"use client";

import { useState } from "react";

export default function SeedDemoPage() {
  const [status, setStatus] = useState<string | null>(null);

  const runSeed = async () => {
    setStatus("running");

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/admin/seed/v1`,
        { method: "POST" }
      );

      if (!res.ok) {
        const err = await res.json();
        setStatus(`error: ${err.detail}`);
        return;
      }

      const data = await res.json();
      setStatus(`ok: ${JSON.stringify(data.summary)}`);
    } catch (e) {
      setStatus("error: network failure");
    }
  };

  return (
    <main style={{ padding: "2rem" }}>
      <h1>Development Utilities</h1>

      <button onClick={runSeed}>
        Load demo data (Seed V1)
      </button>

      {status && <pre>{status}</pre>}
    </main>
  );
}
