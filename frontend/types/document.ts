// frontend/types/document.ts

/* =========================
 * Document – List View
 * ========================= */

export type DocumentListItem = {
  id: string;
  filename: string;
  document_type: string | null;
  ingestion_status: string;
  created_at: string;

  processing_status?: string | null;
  processed_at?: string | null;
};

/* =========================
 * Document – Detail View
 * ========================= */

export type DocumentDetail = {
  id: string;
  filename: string;
  document_type: string | null;
  ingestion_status: string;
  created_at: string;

  processing: DocumentProcessing | null;
  artifacts: DocumentArtifact[];
  signals: DocumentSignal[];
  latest_prediction: DocumentPrediction | null;
};

/* =========================
 * Sub-structures
 * ========================= */

export type DocumentProcessing = {
  status: string;
  processed_path: string | null;
  feature_path: string | null;
  updated_at: string;
};

export type DocumentArtifact = {
  artifact_type: string;
  content_ref: string;
  created_at: string;
};

export type DocumentSignal = {
  signal_type: string;
  signal_value: string;
  confidence: number | null;
  created_at: string;
};

export type DocumentPrediction = {
  score: number;
  threshold: number;
  decision: string;
  created_at: string;

  model_name: string;
  model_version: string;
  feature_version: string;
};
