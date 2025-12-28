// frontend/app/loading.tsx

export default function HomeLoading() {
  return (
    <main style={{ padding: "2.5rem", maxWidth: "900px", margin: "0 auto" }}>
      <h1 style={{ opacity: 0.3, marginBottom: "2rem" }}>
        Risk-Aware ML System
      </h1>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: "1rem",
          marginBottom: "2rem",
        }}
      >
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            style={{
              height: "90px",
              backgroundColor: "#e5e7eb",
              borderRadius: "8px",
            }}
          />
        ))}
      </section>

      <div
        style={{
          width: "160px",
          height: "40px",
          backgroundColor: "#e5e7eb",
          borderRadius: "6px",
        }}
      />
    </main>
  );
}
