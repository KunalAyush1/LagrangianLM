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
            raise TypeError("mode must be of type FileMode")
    
    def _validate_path(self) -> None:
        """Validate the configured text file can be read"""
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Text file doesn't exist: {self.file_path}"
            )
        if self.mode is FileMode.LINE and not self.file_path.is_file():
            raise ValueError(
                "LINE mode requires file_path to point to a single file"
            )
        if self.mode is FileMode.FILE:
            if not self.file_path.is_file() and not self.file_path.is_dir():
                raise ValueError(
                    f"Expected a file or directory but received: "
                    f"{self.file_path}"
                )
    
    def _create_file_document_id(self,
                            file_path: Path
                            ) -> str:
        """Creates a docid for file mode doc"""
        source_part = self.source_name.strip().lower().replace(" ", "_")
        split_part = self.split.strip().lower().replace(" ", "_")
        
        if self.file_path.is_dir():
            relative_path = file_path.relative_to(self.file_path)
        else:
            relative_path = Path(file_path.name)
        
        path_part = str(relative_path).lower().replace(" ", "_")
        path_part = path_part.replace("/","-").replace("\\","-")
        
        return f"{source_part}-{split_part}-{path_part}"
    
    def _create_line_document_id(
        self,
        file_path: Path,
        line_number: int,
    ) -> str:
        """Creates a doc_id for line-mode docs"""
        
        source_part = self.source_name.strip().lower().replace(" ", "_")
        split_part = self.split.strip().lower().replace(" ", "_")
        file_part = file_path.stem.strip().lower().replace(" ", "_")
        
        return (
            f"{source_part}-{split_part}-"
            f"{file_part}-{line_number:08d}"
        )
        
    def _discover_files(self) -> list[Path]:
        """Discovers relevant text files to create documents"""
        
        
        if self.file_path.is_file():
            return [self.file_path]
        if self.recursive:
            files = self.file_path.rglob(self.file_pattern)
        else:
            files = self.file_path.glob(self.file_pattern)
        
        discovered_files = sorted(
            path for path in files if path.is_file()
        )
        
        if not discovered_files:
            raise FileNotFoundError(
                f"No files matching '{self.file_pattern}' were found in "
                f"{self.file_path}"
            )
        
        return discovered_files
        
        
    def load(self) -> Iterator[Document]:
        """Reads the file and yields docs"""
        self._validate_path()
        
        if self.mode is FileMode.FILE:
            yield from self._load_file_mode()
        elif self.mode is FileMode.LINE:
            yield from self._load_line_mode()
        
        else:
            raise ValueError(f"Unsupported file mode: {self.mode}")
    
    def _load_file_mode(self) -> Iterator[Document]:
        """Yield a document for each text file"""
        for file_path in self._discover_files():
            raw_text = file_path.read_text(encoding=self.encoding)
            
            if self.file_path.is_dir():
                relative_path = file_path.relative_to(self.file_path)
            else:
                relative_path = Path(file_path.name)
            
            document = Document(
                doc_id = self._create_file_document_id(file_path),
                source = self.source_name,
                source_id = str(relative_path),
                raw_text = raw_text,
                metadata = {
                    "split": self.split,
                    "file_name": file_path.name,
                    "relative_path": str(relative_path),
                    "file_size": file_path.stat().st_size,
                },
                
            )
            
            yield document
            
    def _load_line_mode(self) -> Iterator[Document]:
        """Yield a doc for each non-empty line in a text file"""
        
        with self.file_path.open("r", encoding=self.encoding) as file:
            for line_number, line in enumerate(file, start=1):
                raw_text = line.rstrip("\r\n")
                
                if not raw_text.strip():
                    continue
                
                document = Document(
                    doc_id = self._create_line_document_id(
                        file_path = self.file_path,
                        line_number = line_number
                    ),
                    source = self.source_name,
                    source_id = None,
                    raw_text = raw_text,
                    metadata = {
                        "split": self.split,
                        "file_name": self.file_path.name,
                        "line_number": line_number,
                    },
                    
                )
                
                yield document
        