from ...domain.ports import ContentExtractorPort
import trafilatura


class TrafilaturaMarkdownExtractor(ContentExtractorPort):
    def extract_markdown(self, html: str, base_url: str) -> str:
        # Trafilatura prioritizes main content; request markdown output
        md = trafilatura.extract(html, url=base_url, output_format="markdown", include_links=True)
        return md or ""