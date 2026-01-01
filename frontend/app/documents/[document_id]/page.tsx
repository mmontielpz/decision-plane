// frontend/app/documents/[document_id]/page.tsx

import { fetchDocument } from "@/services/documents";
import { notFound } from "next/navigation";

export const dynamic = "force-dynamic";

type Props = {
  params: {
    document_id: string;
  };
};

export default async function DocumentDetailPage({ params }: Props) {
  const { document_id } = params;

  let doc;
  try {
    doc = await fetchDocument(document_id);
  } catch {
    notFound();
  }

  return (
    <main style={{ padding: "2rem" }}>
      <h1>{doc.filename}</h1>

      <section>
        <p>
          <strong>Type:</strong> {doc.document_type ?? "-"}
        </p>
        <p>
          <strong>Ingestion status:</strong> {doc.ingestion_status}
        </p>
        <p>
          <strong>Processing status:</strong> {doc.processing?.status}
        </p>
      </section>

      <hr />

      <section>
        <h2>Artifacts</h2>
        {doc.artifacts.length === 0 && <p>No artifacts available.</p>}
        <ul>
          {doc.artifacts.map((a: any, idx: number) => (
            <li key={idx}>
              {a.artifact_type}: {a.content_ref}
            </li>
          ))}
        </ul>
      </section>

      <section>
        <h2>Signals</h2>
        {doc.signals.length === 0 && <p>No signals available.</p>}
        <ul>
          {doc.signals.map((s: any, idx: number) => (
            <li key={idx}>
              {s.signal_type}: {s.signal_value} ({s.confidence ?? "-"})
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
