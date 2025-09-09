from abc import ABC, abstractmethod
from typing import Iterable, Tuple
from .models import PageAssets


class HttpClientPort(ABC):
    @abstractmethod
    async def get_text(self, url: str, timeout: float = 20.0) -> str: ...


    @abstractmethod
    async def get_bytes(self, url: str, timeout: float = 20.0) -> bytes: ...


class ContentExtractorPort(ABC):
    @abstractmethod
    def extract_markdown(self, html: str, base_url: str) -> str: ...


class ImageExtractorPort(ABC):
    @abstractmethod
    def discover_image_urls(self, html: str, base_url: str) -> Iterable[str]: ...


    @abstractmethod
    def resize_image_square_max(self, content: bytes, max_px: int = 800) -> Tuple[bytes, str]:
        """
        Return (image_bytes, ext) preserving aspect ratio within max_px square.
        """


class StoragePort(ABC):
    @abstractmethod
    def list_destinations(self) -> list[str]: ...


    @abstractmethod
    def ensure_destination(self, name: str) -> str: ...


    @abstractmethod
    def save_markdown(self, dest: str, filename: str, content: str) -> str: ...


    @abstractmethod
    def save_binary(self, dest: str, filename: str, content: bytes) -> str: ...