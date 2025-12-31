// frontend/types/document.ts

export type DocumentRow = {
  document_id: string;
  status: string;
  decision?: string | null;
  score?: number | null;
  last_updated?: string | null;

  processed_path?: string | null;
  feature_path?: string | null;

  source_system?: string | null;
};
