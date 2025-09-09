from __future__ import annotations
from typing import Iterable, Tuple
from urllib.parse import urljoin
from bs4 import BeautifulSoup # via trafilatura dependency (lxml/bs4)
from PIL import Image
import io


from ...domain.ports import ImageExtractorPort


class ImageExtractor(ImageExtractorPort):
    def discover_image_urls(self, html: str, base_url: str) -> Iterable[str]:
        soup = BeautifulSoup(html, "lxml")
        urls: list[str] = []
        for tag in soup.find_all(["img", "source"]):
            src = tag.get("src") or tag.get("data-src") or tag.get("srcset")
            if not src:
                continue
            # handle srcset: take first candidate
            if "," in src:
                src = src.split(",")[0].split()[0]
            abs_url = urljoin(base_url, src)
            urls.append(abs_url)
            # de-dup while preserving order
            seen = set()
            out = []
        for u in urls:
            if u not in seen:
                seen.add(u)
            out.append(u)
        return out


    def resize_image_square_max(self, content: bytes, max_px: int = 800) -> Tuple[bytes, str]:
        with Image.open(io.BytesIO(content)) as im:
            im = im.convert("RGB") # normalize
            im.thumbnail((max_px, max_px)) # preserves aspect ratio within box
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=88, optimize=True)
            return buf.getvalue(), "jpg"