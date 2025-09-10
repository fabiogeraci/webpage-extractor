from __future__ import annotations
from typing import List, Dict
from bs4 import BeautifulSoup
import trafilatura
from ...domain.ports import ContentExtractorPort


class AccordionContentExtractor(ContentExtractorPort):
    """
    Enhanced content extractor that captures both main content and hidden accordion content.
    Specifically designed to extract content from <details>/<summary> accordion elements.
    Now includes specific extraction for "Ingredients" and "How to use" sections.
    """
    
    def extract_markdown(self, html: str, base_url: str) -> str:
        # First, get the main content using trafilatura
        main_content = trafilatura.extract(html, url=base_url, output_format="markdown", include_links=True)
        main_content = main_content or ""
        
        # Then extract accordion content
        accordion_content = self._extract_accordion_content(html, base_url)
        
        # Combine both contents
        if accordion_content:
            if main_content:
                return main_content + "\n\n" + accordion_content
            else:
                return accordion_content
        else:
            return main_content or f"# Extracted Content\n\n_Source:_ {base_url}\n\n(No main content detected.)\n"
    
    def _extract_accordion_content(self, html: str, base_url: str) -> str:
        """Extract content from accordion elements (<details>/<summary>)."""
        soup = BeautifulSoup(html, "lxml")
        
        accordion_sections = []
        
        # Find all <details> elements
        details_elements = soup.find_all("details")
        
        for details in details_elements:
            # Get the summary text (the accordion header)
            summary = details.find("summary")
            if not summary:
                continue
                
            # Clean up summary text - look for h2, h3, or direct text
            summary_text = ""
            h_tag = summary.find(["h1", "h2", "h3", "h4", "h5", "h6"])
            if h_tag:
                summary_text = self._clean_text(h_tag.get_text())
            else:
                summary_text = self._clean_text(summary.get_text())
            
            if not summary_text:
                continue
            
            # Look for content in various possible locations
            content_text = ""
            
            # First, try to find accordion content divs
            content_divs = details.find_all("div", class_=lambda x: x and ("content" in x.lower() or "accordion" in x.lower()))
            
            for content_div in content_divs:
                div_text = self._clean_text(content_div.get_text())
                if div_text and len(div_text.strip()) > 10:
                    content_text = div_text
                    break
            
            # If no content found in specific divs, try to get all content except summary
            if not content_text:
                # Create a copy of details to avoid modifying the original
                details_copy = BeautifulSoup(str(details), "lxml").find("details")
                if details_copy:
                    # Remove summary from the copy
                    summary_copy = details_copy.find("summary")
                    if summary_copy:
                        summary_copy.decompose()
                    
                    content_text = self._clean_text(details_copy.get_text())
            
            # Only include sections with substantial content
            if content_text and len(content_text.strip()) > 10:
                accordion_sections.append({
                    "title": summary_text,
                    "content": content_text
                })
        
        # Convert to markdown with specific handling for Ingredients and How to use
        if accordion_sections:
            markdown_sections = []
            
            # Separate sections into specific categories
            ingredients_sections = []
            how_to_use_sections = []
            other_sections = []
            
            for section in accordion_sections:
                title_lower = section['title'].lower()
                if 'ingredient' in title_lower:
                    ingredients_sections.append(section)
                elif any(keyword in title_lower for keyword in ['how to use', 'usage', 'directions', 'instructions']):
                    how_to_use_sections.append(section)
                else:
                    other_sections.append(section)
            
            # Add Ingredients section if found
            if ingredients_sections:
                markdown_sections.append("## Ingredients")
                for section in ingredients_sections:
                    markdown_sections.append(section['content'])
                    markdown_sections.append("")  # Empty line for spacing
            
            # Add How to use section if found
            if how_to_use_sections:
                markdown_sections.append("## How to use")
                for section in how_to_use_sections:
                    markdown_sections.append(section['content'])
                    markdown_sections.append("")  # Empty line for spacing
            
            # Add other sections under Additional Information
            if other_sections:
                markdown_sections.append("## Additional Information")
                for section in other_sections:
                    markdown_sections.append(f"### {section['title']}")
                    markdown_sections.append(section['content'])
                    markdown_sections.append("")  # Empty line for spacing
            
            return "\n".join(markdown_sections)
        
        return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]  # Remove empty lines
        
        return '\n'.join(lines)
