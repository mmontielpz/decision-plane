// frontend/types/document.ts

export type DocumentRow = {
  document_id: string;
  status: string;
  decision: string | null;
  score: number | null;
  last_updated: string | null;
};
