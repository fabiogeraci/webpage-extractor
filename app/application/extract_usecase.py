from __future__ import annotations
from typing import List
from ..domain.ports import HttpClientPort, ContentExtractorPort, ImageExtractorPort, StoragePort
from ..domain.models import ExtractionResult
import os


class ExtractUseCase:
    def __init__(self, http: HttpClientPort, content_ext: ContentExtractorPort, image_ext: ImageExtractorPort, storage: StoragePort):
        self.http = http
        self.content_ext = content_ext
        self.image_ext = image_ext
        self.storage = storage


    async def execute(self, url: str, destination_name: str) -> ExtractionResult:
        dest = self.storage.ensure_destination(destination_name)


        html = await self.http.get_text(url)
        markdown = self.content_ext.extract_markdown(html, url)
        if not markdown:
            markdown = f"# Extracted Content\n\n_Source:_ {url}\n\n(No main content detected.)\n"


        # Discover & download images
        image_urls = list(self.image_ext.discover_image_urls(html, url))
        saved_images: List[str] = []
        for idx, img_url in enumerate(image_urls, start=1):
            try:
                content = await self.http.get_bytes(img_url)
                resized, ext = self.image_ext.resize_image_square_max(content, 800)
                fname = f"images/img_{idx:03d}.{ext}"
                self.storage.save_binary(dest, fname, resized)
                saved_images.append(fname)
            except Exception:
                # Best-effort; skip broken images
                continue


        # Enhance markdown with local image references (append section)
        if saved_images:
            md_images = "\n".join([f"![image]({p})" for p in saved_images])
            markdown = markdown.rstrip() + "\n\n## Extracted Images\n\n" + md_images + "\n"


        base_name = self._safe_filename(url)
        self.storage.save_markdown(dest, f"{base_name}.md", markdown)

        return ExtractionResult(markdown=markdown, image_filenames=saved_images)


    def _safe_filename(self, url: str) -> str:
        keep = [c if c.isalnum() else "-" for c in url]
        out = "".join(keep).strip("-")
        return out[:80] or "page"