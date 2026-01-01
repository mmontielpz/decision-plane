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
    <main style={{ padding: "2rem", maxWidth: "900px" }}>
      <h1>{doc.filename}</h1>

      {/* -------------------------
          Core metadata
      ------------------------- */}
      <section style={{ marginTop: "1rem" }}>
        <p><strong>Document ID:</strong> {doc.id}</p>
        <p><strong>Type:</strong> {doc.document_type ?? "-"}</p>
        <p><strong>Ingestion Status:</strong> {doc.ingestion_status}</p>
        <p>
          <strong>Created At:</strong>{" "}
          {new Date(doc.created_at).toLocaleString()}
        </p>
      </section>

      <hr />

      {/* -------------------------
          Processing
      ------------------------- */}
      <section>
        <h2>Processing</h2>

        {doc.processing ? (
          <>
            <p><strong>Status:</strong> {doc.processing.status}</p>
            <p><strong>Processed Path:</strong> {doc.processing.processed_path ?? "-"}</p>
            <p><strong>Feature Path:</strong> {doc.processing.feature_path ?? "-"}</p>
            <p>
              <strong>Updated At:</strong>{" "}
              {doc.processing.updated_at
                ? new Date(doc.processing.updated_at).toLocaleString()
                : "-"}
            </p>
          </>
        ) : (
          <p>No processing information available.</p>
        )}
      </section>

      <hr />

      {/* -------------------------
          Artifacts
      ------------------------- */}
      <section>
        <h2>Artifacts</h2>

        {doc.artifacts.length === 0 && <p>No artifacts.</p>}

        {doc.artifacts.length > 0 && (
          <ul>
            {doc.artifacts.map((a, idx) => (
              <li key={idx}>
                <strong>{a.artifact_type}:</strong> {a.content_ref}
              </li>
            ))}
          </ul>
        )}
      </section>

      <hr />

      {/* -------------------------
          Signals
      ------------------------- */}
      <section>
        <h2>Signals</h2>

        {doc.signals.length === 0 && <p>No signals.</p>}

        {doc.signals.length > 0 && (
          <ul>
            {doc.signals.map((s, idx) => (
              <li key={idx}>
                <strong>{s.signal_type}</strong>: {s.signal_value}
                {s.confidence !== null && ` (confidence: ${s.confidence})`}
              </li>
            ))}
          </ul>
        )}
      </section>

      <hr />

      {/* -------------------------
          Latest prediction
      ------------------------- */}
      <section>
        <h2>Latest Prediction</h2>

        {doc.latest_prediction ? (
          <>
            <p><strong>Decision:</strong> {doc.latest_prediction.decision}</p>
            <p><strong>Score:</strong> {doc.latest_prediction.score}</p>
            <p><strong>Threshold:</strong> {doc.latest_prediction.threshold}</p>
            <p>
              <strong>Model:</strong>{" "}
              {doc.latest_prediction.model_name} v{doc.latest_prediction.model_version}
            </p>
            <p>
              <strong>Created At:</strong>{" "}
              {new Date(doc.latest_prediction.created_at).toLocaleString()}
            </p>
          </>
        ) : (
          <p>No prediction available.</p>
        )}
      </section>
    </main>
  );
}
