from fastapi import Depends
from .infrastructure.http.httpx_client import HttpxClient
from .infrastructure.extraction.trafilatura_markdown_extractor import TrafilaturaMarkdownExtractor
from .infrastructure.extraction.image_extractor import ImageExtractor
from .infrastructure.storage.filesystem_storage import FilesystemStorage
from .application.extract_usecase import ExtractUseCase


async def usecase_provider():
    http = HttpxClient()
    content_ext = TrafilaturaMarkdownExtractor()
    image_ext = ImageExtractor()
    storage = FilesystemStorage()
    return ExtractUseCase(http, content_ext, image_ext, storage)


UseCaseDep = Depends(usecase_provider)