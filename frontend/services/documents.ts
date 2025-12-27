// frontend/services/documents.ts

import { DocumentRow } from "@/types/document";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function fetchDocuments(): Promise<DocumentRow[]> {
  const res = await fetch(`${API_BASE_URL}/api/documents`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch documents");
  }

  return res.json();
}
