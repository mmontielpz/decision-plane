// frontend/app/documents/[document_id]/loading.tsx

export default function DocumentDetailLoading() {
  return (
    <main style={{ padding: "2rem" }}>
      <h1 style={{ opacity: 0.3, marginBottom: "1.5rem" }}>
        Document
      </h1>

      <section style={{ marginBottom: "1.5rem" }}>
        {[1, 2, 3, 4].map((i) => (
          <div
            key={i}
            style={{
              height: "16px",
              width: i === 1 ? "40%" : "60%",
              backgroundColor: "#e5e7eb",
              borderRadius: "4px",
              marginBottom: "0.75rem",
            }}
          />
        ))}
      </section>

      <hr />

      <section style={{ marginTop: "1.5rem" }}>
        {[1, 2].map((i) => (
          <div
            key={i}
            style={{
              height: "14px",
              width: "80%",
              backgroundColor: "#e5e7eb",
              borderRadius: "4px",
              marginBottom: "0.75rem",
            }}
          />
        ))}
      </section>
    </main>
  );
}
