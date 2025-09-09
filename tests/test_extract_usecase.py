import pytest
from app.application.extract_usecase import ExtractUseCase
from app.domain.ports import HttpClientPort, ContentExtractorPort, ImageExtractorPort, StoragePort
from app.domain.models import ExtractionResult


class FakeHttp(HttpClientPort):
    async def get_text(self, url: str, timeout: float = 20.0) -> str:
        return f"""
        <html><body>
        <main><h1>Title</h1><p>Hello <strong>world</strong>.</p>
        <img src="/a.jpg"/></main>
        </body></html>
        """
    async def get_bytes(self, url: str, timeout: float = 20.0) -> bytes:
        # 1×1 white JPEG
        return bytes.fromhex(
        "FFD8FFE000104A46494600010100000100010000FFDB00430001010101010101"
        "0101010101010101010101010101010101010101010101010101010101010101"
        "0101010101010101010101FFC00011080001000103012200021101031101FFDA"
        "000C03010002110311003F00D2CFD9FFDA0008010100010502FF00D2FFDA0008"
        "010300010502FF00D2FFD9"
        )


class FakeContent(ContentExtractorPort):
    def extract_markdown(self, html: str, base_url: str) -> str:
        return "# Title\n\nHello **world**."


    class CaptureStorage(StoragePort):
        def __init__(self):
            self.saved = {}
        def list_destinations(self):
            return []
        def ensure_destination(self, name: str) -> str:
            return "/tmp/dest"
        def save_markdown(self, dest: str, filename: str, content: str) -> str:
            self.saved[filename] = content
            return "/tmp/dest/" + filename
        def save_binary(self, dest: str, filename: str, content: bytes) -> str:
            self.saved[filename] = content
            return "/tmp/dest/" + filename


class NoopImage(ImageExtractorPort):
    def discover_image_urls(self, html: str, base_url: str):
        return ["https://example.com/a.jpg"]
    def resize_image_square_max(self, content: bytes, max_px: int = 800):
        return content, "jpg"


@pytest.mark.asyncio
async def test_execute_happy_path():
    usecase = ExtractUseCase(FakeHttp(), FakeContent(), NoopImage(), CaptureStorage())
    res: ExtractionResult = await usecase.execute("https://example.com/article", "exports/test")
    assert "# Title" in res.markdown
    assert len(res.image_filenames) == 1