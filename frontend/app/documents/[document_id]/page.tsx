import { fetchDocument } from "@/services/documents";

export const dynamic = "force-dynamic";

type Props = {
  params: Promise<{
    document_id: string;
  }>;
};

export default async function DocumentDetailPage({ params }: Props) {
  const { document_id } = await params;

  try {
    const doc = await fetchDocument(document_id);

    return (
      <main style={{ padding: "2rem" }}>
        <h1>Document {doc.document_id}</h1>

        <section>
          <p><strong>Status:</strong> {doc.status}</p>
          <p><strong>Decision:</strong> {doc.decision ?? "-"}</p>
          <p><strong>Score:</strong> {doc.score ?? "-"}</p>
          <p><strong>Last Updated:</strong> {doc.last_updated ?? "-"}</p>
        </section>

        <hr />

        <section>
          <p><strong>Processed Path:</strong> {doc.processed_path ?? "-"}</p>
          <p><strong>Feature Path:</strong> {doc.feature_path ?? "-"}</p>
        </section>
      </main>
    );
  } catch (e: any) {
    return (
      <main style={{ padding: "2rem" }}>
        <h1>Document not found</h1>
        <p>{e.message}</p>
      </main>
    );
  }
}
