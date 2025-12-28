// frontend/app/documents/loading.tsx

export default function DocumentsLoading() {
  return (
    <main style={{ padding: "2rem" }}>
      <h1 style={{ opacity: 0.3, marginBottom: "1rem" }}>
        Documents
      </h1>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            {["Document ID", "Status", "Decision", "Score", "Last Updated"].map((h) => (
              <th key={h} align="left" style={{ opacity: 0.3 }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {[1, 2, 3].map((i) => (
            <tr key={i}>
              {[1, 2, 3, 4, 5].map((j) => (
                <td key={j} style={{ padding: "0.5rem 0" }}>
                  <div
                    style={{
                      height: "14px",
                      width: "80%",
                      backgroundColor: "#e5e7eb",
                      borderRadius: "4px",
                    }}
                  />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
