from lagrangianlm.data.loaders.base import BaseLoader
from lagrangianlm.data.schemas import Document
from collections.abc import Iterator
from pathlib import Path
import json


class JSONLLoader(BaseLoader):
    """Loads documents from JSONL files"""
    def __init__(self,file_path: str | Path,
                 source_name: str,
                 split: str = "train",
                 text_field: str = "text",
                 id_field: str | None = None,
                 metadata_fields: list[str] |  None = None,
                 encoding: str = "utf-8",) -> None:
        super().__init__(source_name=source_name, split=split)
        self.file_path = Path(file_path)
        self.text_field = text_field
        self.id_field = id_field
        self.metadata_fields = metadata_fields
        self.encoding = encoding
        
        self._validate_configuration()
    
    def _validate_configuration(self) -> None:
        """Validates the loader config before reading the file"""
        if not isinstance(self.text_field, str):
            raise TypeError("text_field must be a string")
        if not self.text_field.strip():
            raise ValueError("text_field can't be empty")
        if self.id_field is not None:
            if not isinstance(self.id_field, str):
                raise TypeError("id_field must be a string or None")
            if not self.id_field.strip():
                raise ValueError("id_field can't be empty")
        if self.metadata_fields is None:
            self.metadata_fields = []
        elif not isinstance(self.metadata_fields, list):
            raise TypeError("metadata fields must be a list")
        else:
            self.metadata_fields = list(self.metadata_fields)
        for field_name in self.metadata_fields:
            if not isinstance(field_name, str):
                raise TypeError("Every item in metadata field must be a string")
            if not field_name.strip():
                raise ValueError("metadata field names can't be empty")
        
        if not isinstance(self.encoding, str):
            raise TypeError("encoding must be a string")
        if not self.encoding.strip():
            raise ValueError("encoding can't be empty")
    
    def _validate_file(self) -> None:
        """Validate that the configured JSONL file can be read"""
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"JSONL file doesn't exist: {self.file_path}"
            )
        if not self.file_path.is_file():
            raise ValueError(
                f"Expected a file but receieved: {self.file_path}"
            )
    
    def _create_document_id(
        self,
        line_number: int,
        source_id: str | None,
    ) -> str:
        """Creates a docid"""
        source_part = self.source_name.strip().lower().replace(" ", "_")
        split_part = self.split.strip().lower().replace(" ", "_")
        
        if source_id is not None:
            return f"{source_part}-{split_part}-{source_id}"
        
        return f"{source_part}-{split_part}-{line_number:08d}"
    
    def _extract_metadata(self, record: dict) -> dict:
        """Extract explicitly configured metadata fields"""
        return {
            field_name: record[field_name]
            for field_name in self.metadata_fields
            if field_name in record
            
        }
        
        
    def load(self) -> Iterator[Document]:
        """Read the JSONL file and yield doc"""
        self._validate_file()
        
        with self.file_path.open("r", encoding=self.encoding) as file:
            for line_number, line in enumerate(file, start=1):
                stripped_line = line.strip()
                
                if not stripped_line:
                    continue
                try:
                    record = json.loads(stripped_line)
                except json.JSONDecodeError as error:
                    raise ValueError(
                        f"Invalid JSON at {self.file_path},"
                        f"line { line_number}: {error.msg}"
                    ) from error
                if not isinstance(record, dict):
                    raise TypeError(
                        f"Expected a JSON Object at {self.file_path},"
                        f"line { line_number}"
                    )
                if self.text_field not in record:
                    raise KeyError(
                        f"Missing text field '{self.text_field}' at"
                        f"{self.file_path}, line { line_number}"
                    )
                raw_text = record[self.text_field]
                
                if not isinstance(raw_text, str):
                    raise TypeError(
                        f"Field '{self.text_field}' must contain a string at"
                        f"{self.file_path}, line { line_number}"
                    )
                source_id = None
                
                if self.id_field is not None and self.id_field in record:
                    source_id = str(record[self.id_field])
                    
                document = Document(
                    doc_id = self._create_document_id(
                        line_number = line_number,
                        source_id = source_id
                    ),
                    source = self.source_name,
                    source_id = source_id,
                    raw_text = raw_text,
                    metadata = {
                        **self._extract_metadata(record),
                        "split":self.split,
                        "line_number": line_number,
                    },
                )
                
                yield document
        