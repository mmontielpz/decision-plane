// frontend/app/documents/page.tsx

export const dynamic = "force-dynamic";

import { fetchDocuments } from "@/services/documents";
import { DocumentRow } from "@/types/document";

export default async function DocumentsPage() {
  let documents: DocumentRow[] = [];
  let error: string | null = null;

  try {
    documents = await fetchDocuments();
  } catch (e) {
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
              <th align="left">Document ID</th>
              <th align="left">Status</th>
              <th align="left">Decision</th>
              <th align="left">Score</th>
              <th align="left">Last Updated</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.document_id}>
                <td>{doc.document_id}</td>
                <td>{doc.status}</td>
                <td>{doc.decision ?? "-"}</td>
                <td>
                  {doc.score !== null ? doc.score.toFixed(2) : "-"}
                </td>
                <td>{doc.last_updated ?? "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </main>
  );
}

