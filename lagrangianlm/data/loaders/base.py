"""
    A loader may read from:
    a) a text file
    b) JSONL
    c) Hugging Face datasets
    etc..
    but all loaders should return the same thing ie. an iterable of document objects
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator

from lagrangianlm.data.schemas import Document

class loader(ABC):  #an abstract class means it will not be used directly
    """An abstract interface for all dataset loaders"""
    def __init__(self, source_name: str, split: str = "train") -> None:
        if not isinstance(source_name, str):
            raise TypeError("source_name must be a string")
        if not source_name.strip():
            raise ValueError("source_name can't be empty")
        if not isinstance(split, str):
            raise TypeError("split must be a string")
        if not split.strip():
            raise ValueError("split can't be empty")
        self.source_name = source_name
        self.split = split
        
    @abstractmethod #abstractmethod will force every subclass to implement load()
    def load(self) -> Iterator[Document]:
        """Yield documents from the configured source"""
        raise NotImplementedError
    
    
    
