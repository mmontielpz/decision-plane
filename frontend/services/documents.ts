// frontend/services/documents.ts

import { DocumentRow } from "@/types/document";

function getApiBaseUrl() {
  const serverBase = process.env.API_BASE_URL;
  const publicBase = process.env.NEXT_PUBLIC_API_BASE_URL;

  const base = serverBase ?? publicBase ?? "";
  return base.replace(/\/+$/, "");
}

async function readBodySafe(res: Response) {
  try {
    return await res.text();
  } catch {
    return "<unreadable body>";
  }
}

export async function fetchDocuments(): Promise<DocumentRow[]> {
  const base = getApiBaseUrl();
  const url = `${base}/api/documents`;

  console.log("[fetchDocuments] API_BASE_URL:", process.env.API_BASE_URL);
  console.log("[fetchDocuments] NEXT_PUBLIC_API_BASE_URL:", process.env.NEXT_PUBLIC_API_BASE_URL);
  console.log("[fetchDocuments] final URL:", url);

  if (!base) {
    throw new Error("API base URL is empty");
  }

  let res: Response;
  try {
    res = await fetch(url, {
      method: "GET",
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
  } catch (e: any) {
    console.log("[fetchDocuments] fetch threw:", e);
    throw new Error(`fetch threw before response: ${e?.message ?? String(e)}`);
  }

  console.log("[fetchDocuments] status:", res.status, res.statusText);

  if (!res.ok) {
    const body = await readBodySafe(res);
    console.log("[fetchDocuments] non-OK body:", body);
    throw new Error(`HTTP ${res.status} ${res.statusText}\n${body}`);
  }

  const data = await res.json();
  console.log("[fetchDocuments] rows:", Array.isArray(data) ? data.length : "not-array");
  return data as DocumentRow[];
}

export async function fetchDocument(documentId: string): Promise<DocumentRow> {
  const base = getApiBaseUrl();
  const url = `${base}/api/documents/${documentId}`;

  console.log("[fetchDocument] final URL:", url);

  const res = await fetch(url, { cache: "no-store" });

  if (!res.ok) {
    const body = await readBodySafe(res);
    throw new Error(`HTTP ${res.status}\n${body}`);
  }

  return res.json();
}
