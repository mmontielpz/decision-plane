// frontend/app/documents/page.tsx

type DocumentRow = {
  document_id: string;
  status: string;
  decision: string | null;
  score: number | null;
  last_updated: string | null;
};

const MOCK_DOCUMENTS: DocumentRow[] = [
  {
    document_id: "doc-001",
    status: "processed",
    decision: "REVIEW",
    score: 0.78,
    last_updated: "2025-01-10T14:22:00Z",
  },
  {
    document_id: "doc-002",
    status: "processed",
    decision: "ACCEPT",
    score: 0.12,
    last_updated: "2025-01-09T09:10:00Z",
  },
];

export default function DocumentsPage() {
  return (
    <main style={{ padding: "2rem" }}>
      <h1>Documents</h1>

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
          {MOCK_DOCUMENTS.map((doc) => (
            <tr key={doc.document_id}>
              <td>{doc.document_id}</td>
              <td>{doc.status}</td>
              <td>{doc.decision ?? "-"}</td>
              <td>{doc.score !== null ? doc.score.toFixed(2) : "-"}</td>
              <td>{doc.last_updated ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
