// frontend/app/documents/page.tsx

export const dynamic = "force-dynamic";

import Link from "next/link";
import { fetchDocuments } from "@/services/documents";
import { DocumentListItem } from "@/types/document";

export default async function DocumentsPage() {
  let documents: DocumentListItem[] = [];
  let error: string | null = null;

  try {
    documents = await fetchDocuments();
  } catch {
    error = "Unable to load documents";
  }

  return (
    <main style={{ padding: "2rem" }}>
      <h1>Documents</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {!error && documents.length === 0 && (
        <p>No documents available.</p>
      )}

      {!error && documents.length > 0 && (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            marginTop: "1rem",
          }}
        >
          <thead>
            <tr>
              <th align="left">Filename</th>
              <th align="left">Type</th>
              <th align="left">Ingestion Status</th>
              <th align="left">Processing Status</th>
              <th align="left">Created</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.id}>
                <td>
                  <Link href={`/documents/${doc.id}`}>
                    {doc.filename}
                  </Link>
                </td>
                <td>{doc.document_type ?? "-"}</td>
                <td>{doc.ingestion_status}</td>
                <td>{doc.processing_status ?? "-"}</td>
                <td>
                  {doc.created_at
                    ? new Date(doc.created_at).toLocaleString()
                    : "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}
