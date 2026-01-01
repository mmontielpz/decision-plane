// frontend/services/documents.ts

import {
  DocumentListItem,
  DocumentDetail,
} from "@/types/document";

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

/* =========================
 * Documents – List
 * ========================= */

export async function fetchDocuments(): Promise<DocumentListItem[]> {
  const base = getApiBaseUrl();
  if (!base) {
    throw new Error("API base URL is empty");
  }

  const res = await fetch(`${base}/api/documents`, {
    method: "GET",
    cache: "no-store",
    headers: { Accept: "application/json" },
  });

  if (!res.ok) {
    const body = await readBodySafe(res);
    throw new Error(`HTTP ${res.status}\n${body}`);
  }

  return res.json();
}

/* =========================
 * Document – Detail
 * ========================= */

export async function fetchDocumentDetail(
  documentId: string
): Promise<DocumentDetail | null> {
  const base = getApiBaseUrl();
  if (!base) {
    throw new Error("API base URL is empty");
  }

  const res = await fetch(`${base}/api/documents/${documentId}`, {
    cache: "no-store",
  });

  if (res.status === 404) {
    return null;
  }

  if (!res.ok) {
    const body = await readBodySafe(res);
    throw new Error(`HTTP ${res.status}\n${body}`);
  }

  return res.json();
}
