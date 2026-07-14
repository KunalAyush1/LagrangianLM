from lagrangianlm.data.loaders.base import BaseLoader
from lagrangianlm.data.schemas import Document
from collections.abc import Iterator, Mapping
from datasets import load_dataset
from pathlib import Path
from typing import Any



class HFLoader(BaseLoader):
    """Loads document from HuggingFace Datasets"""
    def __init__(self,
                 dataset_name: str,
                 source_name: str,
                 dataset_config_name: str | None = None,
                 split: str = "train",
                 text_field: str = "text",
                 id_field: str | None = None,
                 metadata_fields: list[str] | None = None,
                 streaming: bool = False,
                 limit: int | None = None,
                 cache_dir: str | Path | None = None,
                 revision: str | None = None,
                 ) -> None:
        super().__init__(
            source_name = source_name,
            split = split,
        )
        self.dataset_name = dataset_name
        self.dataset_config_name = dataset_config_name
        self.text_field = text_field
        self.id_field = id_field
        self.metadata_fields = metadata_fields
        self.streaming = streaming
        self.limit = limit
        self.cache_dir = Path(cache_dir) if cache_dir is not None else None
        self.revision = revision
        
        self._validate_configuration()
        
        
        
        

    def _validate_configuration(self) -> None:
        """Validates the configs of hugging face datasets"""
        if not isinstance(self.dataset_name, str):
            raise TypeError("Dataset name must be a string")
        if not self.dataset_name.strip():
            raise ValueError("Dataset name can't be empty")
        if (
            self.dataset_config_name is not None
            and not isinstance(self.dataset_config_name, str)
        ):
            raise TypeError(
                "dataset_config_name must be a string or None"
            )
        if (
            self.dataset_config_name is not None
            and not self.dataset_config_name.strip()
        ):
            raise ValueError(
                "dataset_config_name can't be empty"
            )
        if not isinstance(self.text_field, str):
            raise TypeError("text_field must be a string")
        if not self.text_field.strip():
            raise ValueError("text_field can't be empty")
        
        if self.id_field is not None:
            if not isinstance(self.id_field, str):
                raise TypeError(
                    "id_field must be string or None"
                )
            if not self.id_field.strip():
                raise ValueError("id_field can't be empty")
        
        if self.metadata_fields is None:
            self.metadata_fields = []
        elif not isinstance(self.metadata_fields, list):
            raise TypeError(
                "metadata_fields must be a list of string"
            )
        else:
            self.metadata_fields = list(self.metadata_fields)
        
        for field_name in self.metadata_fields:
            if not isinstance(field_name, str):
                raise TypeError("Every metadata field_name must be a string")
            if not field_name.strip():
                raise ValueError(
                    "Metadata field names can't be empty"
                )
        if not isinstance(self.streaming, bool):
            raise TypeError("streaming must be a boolean")
        if self.limit is not None:
            if isinstance(self.limit, bool) or not isinstance(
                self.limit,
                int
            ):
                raise TypeError(
                    "limit must be a +ve integer or None"
                )
            if self.limit <= 0:
                raise ValueError(
                    "limit must be greater than zero"
                )
        if self.revision is not None:
            if not isinstance(self.revision, str):
                raise TypeError(
                    "revision must be a string or None"
                )
            if not self.revision.strip():
                raise ValueError("revision can't be empty")
        
        
    def _load_dataset(self) -> Any:
        """Load the configured dataset from Hugging Face"""
        
        try:
            return load_dataset(
                path = self.dataset_name,
                name = self.dataset_config_name,
                split = self.split,
                streaming = self.streaming,
                cache_dir = (
                    str(self.cache_dir)
                    if self.cache_dir is not None
                    else None
                ),
                revision = self.revision
            )
        except Exception as error:
            raise RuntimeError(
                f"Failed to load Hugging Face dataset"
                f"'{self.dataset_name}', split '{self.split}'"
            ) from error

    
    def _extract_source_id(self,
                           record: Mapping[str, Any]) -> str | None:
        """Extracts recordID when configured"""
        if self.id_field is None:
            return None
        if self.id_field not in record:
            return None
        value = record[self.id_field]
        
        if value is None:
            return None
        
        if not isinstance(value, (str, int)):
            raise TypeError(
                f"Field '{self.id_field}' must contain a"
                f"string, integer or a null"
            )
        
        source_id = str(value).strip()
        
        if not source_id:
            return None
        
        return source_id
    
    def _sanitize_identifier(self, value: str) -> str:
        """Convert a value into docID component"""
        
        sanitized = value.strip().lower()
        sanitized = sanitized.replace(" ", "_")
        sanitized = sanitized.replace("/", "-")
        sanitized = sanitized.replace("\\", "-")
        
        return sanitized
        
    def _create_document_id(self,
                            record_index: int,
                            source_id: str | None) -> str:
        """Creates a docid"""
        source_part = self._sanitize_identifier(self.source_name)
        split_part = self._sanitize_identifier(self.split)
        
        if source_id is not None:
            source_id_part = self._sanitize_identifier(
                source_id
            )
            
            if source_id_part:
                return (
                    f"{source_part}-"
                    f"{split_part}-"
                    f"{source_id_part}"
                )
        return (
            f"{source_part}-"
            f"{split_part}-"
            f"{record_index:08d}"
        )
        
        
    def _extract_metadata(self,
                          record: Mapping[str, Any],
                          record_index: int,
                          ) -> dict[str, Any]:
        """Extract metadata from a record"""
        
        metadata = {
            field_name: record[field_name]
            for field_name in self.metadata_fields
            if field_name in record
        }
        
        metadata.update(
            {
                "dataset_name": self.dataset_name,
                "dataset_config_name": (
                    self.dataset_config_name
                ),
                "split": self.split,
                "record_index": record_index,
            }
        )
        
        return metadata
        
    def load(self) -> Iterator[Document]:
        """Yields doc from hugging face dataset"""
        
        dataset = self._load_dataset()
        
        for record_index, record in enumerate(
            dataset,
            start = 1,
        ):
            if (
                self.limit is not None
                and record_index > self.limit
            ):
                break
            
            if not isinstance(record, Mapping):
                raise TypeError(
                    f"Expected a mapping at record "
                    f"{record_index}, received "
                    f"{type(record).__name__}"
                )
            if self.text_field not in record:
                raise KeyError(
                    f"Missing text field "
                    f"'{self.text_field}' at record "
                    f"{record_index}"
                )
            
            raw_text = record[self.text_field]
            
            if not isinstance(raw_text, str):
                raise TypeError(
                    f"Field '{self.text_field}' must "
                    f"contain a string at record "
                    f"{record_index}"
                )
            
            try:
                source_id = self._extract_source_id(record)
            except TypeError as error:
                raise TypeError(
                    f"{error} at record {record_index}"
                ) from error
                
            document = Document(
                doc_id = self._create_document_id(
                    record_index = record_index,
                    source_id = source_id,
                ),
                source = self.source_name,
                source_id = source_id,
                raw_text = raw_text,
                metadata = self._extract_metadata(
                    record = record,
                    record_index = record_index,
                ),
            )
            
            yield document
    
    