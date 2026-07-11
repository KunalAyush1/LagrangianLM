from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DocumentStatus(str, Enum):
    LOADED = "loaded"
    PROCESSED = "processed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DUPLICATE = "duplicate"
    FAILED = "failed"


@dataclass
class Document:
    """represents one document moving through the ingestion pipeline"""
    #required fields
    doc_id: str
    source: str
    raw_text: str
    #optional fields
    source_id: str | None = None
    clean_text: str | None = None
    language: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    content_hash: str | None = None
    status: DocumentStatus = DocumentStatus.LOADED
    rejection_reason: str | None = None
    
    def __post_init__(self) -> None:
        if not isinstance(self.doc_id, str):
            raise TypeError("doc_id must be a string")
        if not self.doc_id.strip():
            raise ValueError("doc_id cannot be empty")
        if not isinstance(self.source, str):
            raise TypeError("source must be a string")
        if not self.source.strip():
            raise ValueError("source cannot be empty")
        if not isinstance(self.raw_text, str):
            raise TypeError("raw_text must be a string")
        
        


@dataclass
class FilterResult:
    """it represents the outcome of applying a filter to one document"""
    
    passed: bool # whether the doc passed the filter or not
    filter_name: str #name of the filter
    reason: str | None = None #reason for rejection/fail
    score: float | None = None #score for numeric filters
    details: dict[str, Any] = field(default_factory=dict) #for some extra info
    error: str | None = None
    
    def __post_init__(self) -> None:
        if not isinstance(self.passed, bool):
            raise TypeError("passed must be a boolean")
        if not isinstance(self.filter_name, str):
            raise TypeError("filter_name must be a string")
        if not self.filter_name.strip():
            raise ValueError("filter_name can't be empty")
        if self.passed and self.reason is not None:
            raise ValueError("A passed filter can't have a rejection reason")
        if not self.passed and self.reason is None and self.error is None:
            raise ValueError("A failed filter result must contain either a rejection reason or an error")
        if self.score is not None and not isinstance(self.score, (int, float)):
            raise TypeError("Score must be numeric or float")
        
    
    
    