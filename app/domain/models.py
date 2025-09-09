from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ExtractionResult:
    markdown: str
    image_filenames: List[str]


@dataclass(frozen=True)
class PageAssets:
    html: str
    url: str