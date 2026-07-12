from lagrangianlm.data.loaders.base import BaseLoader
from lagrangianlm.data.schemas import Document
from collections.abc import Iterator
from pathlib import Path
from enum import Enum
from typing import Any

class FileMode(str, Enum):
    FILE = "file"
    LINE = "line"


class TextLoader(BaseLoader):
    """Loads document from text files"""
    def __init__(self,
                 file_path: str | Path,
                 source_name: str,
                 split: str = "train",
                 mode: FileMode = FileMode.FILE,
                 encoding: str = "utf-8",
                 file_pattern: str = "*.txt",
                 recursive: bool=False,  
    ) -> None:
        super().__init__(source_name=source_name, split=split)
        self.file_path = Path(file_path)
        self.mode = mode
        self.encoding = encoding
        self.file_pattern = file_pattern
        self.recursive = recursive
        
        self._validate_configuration()
    
    
    def _validate_configuration(self) -> None:
        """Validates loader config before reading the file"""
        if not isinstance(self.encoding, str):
            raise TypeError("encoding must be a string")
        if not self.encoding.strip():
            raise ValueError("Encoding can't be empty")
        if not isinstance(self.file_pattern, str):
            raise TypeError("file_pattern must be a string")
        if not self.file_pattern.strip():
            raise ValueError("file_pattern can't be empty")
        if not isinstance(self.recursive, bool):
            raise TypeError("recursive must be a boolean")
        if not isinstance(self.mode, FileMode):
            raise TypeError("mode must be of type FILEMODE")
    
    def _validate_file(self) -> None:
        """Validate the configured text file can be read"""
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Text file doesn't exist: {self.file_path}"
            )
        if not self.file_path.is_file():
            raise ValueError(
                f"Expected a file but receieved: {self.file_path}"
            )
    
    def _create_document_id(self,
                            line_number: int,
                            file_path: str | Path,
                            mode: FileMode = FileMode.FILE
                            ) -> str:
        """Creates a docid"""
        source_part = self.source_name.strip().lower().replace(" ", "_")
        split_part = self.split.strip().lower().replace(" ", "_")
        relative_path = self.file_path.strip().lower().replace(" ", "_")
        
        if mode is FileMode.FILE:
            return f"{source_part}-{split_part}-{relative_path}"
        else:
            return f"{source_part}-{split_part}-{line_number}
        
    def _discover_files() -> None:
        pass
    def load() -> Iterator[Document]:
        pass