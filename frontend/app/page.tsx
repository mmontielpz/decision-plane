// frontend/app/page.tsx

import Link from "next/link";

export default function Home() {
  return (
    <main style={{ padding: "2rem" }}>
      <h1>Risk-Aware ML System</h1>
      <p>Product UI</p>

      <nav style={{ marginTop: "1rem" }}>
        <Link href="/documents">Go to Documents</Link>
      </nav>
    </main>
  );
}
