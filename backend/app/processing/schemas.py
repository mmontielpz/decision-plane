from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class ProcessedRecord(BaseModel):
    """
    Canonical processed representation derived from raw input.

    This record is reproducible from raw data and serves as the
    single source of truth for downstream feature extraction.
    """

    document_id: str = Field(..., description="Stable unique document identifier")
    ingestion_timestamp: datetime = Field(
        ..., description="Timestamp from the original ingestion event"
    )
    source_system: str = Field(..., description="Originating system identifier")

    processing_timestamp: datetime = Field(
        ..., description="Time when this processing step was executed"
    )
    processor_version: str = Field(
        ..., description="Version of the processor that generated this record"
    )

    extraction_method: str = Field(
        ..., description="Method used to extract content (e.g. plain_text)"
    )

    normalized_text: Optional[str] = Field(
        None,
        description=(
            "Normalized textual representation of the document. "
            "If None, the document must not proceed to feature extraction."
        ),
    )

    parsing_warnings: Optional[List[str]] = Field(
        default=None,
        description="Non-fatal issues encountered during processing",
    )

    raw_path: str = Field(
        ..., description="Filesystem path to the immutable raw input"
    )


class FeatureRecord(BaseModel):
    """
    Stable, versioned feature representation derived from a ProcessedRecord.

    Features must be deterministic and reproducible across runs.
    """

    document_id: str = Field(..., description="Stable unique document identifier")

    feature_timestamp: datetime = Field(
        ..., description="Time when feature extraction was executed"
    )

    feature_version: str = Field(
        ..., description="Version identifier for the feature definitions"
    )

    features: Dict[str, float] = Field(
        ...,
        description="Key-value feature map used by downstream models",
    )

    processed_path: str = Field(
        ..., description="Filesystem path to the processed record used as input"
    )
