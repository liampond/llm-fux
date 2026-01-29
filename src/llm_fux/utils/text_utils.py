"""Text processing utilities for LLM responses."""

import re
from typing import Optional


def clean_code_blocks(text: str, format_hint: Optional[str] = None) -> str:
    """Remove markdown code block delimiters from LLM responses.
    
    LLMs often wrap code/XML output in markdown code blocks like:
        ```xml
        <content>...</content>
        ```
    
    This function strips those delimiters while preserving the actual content.
    
    Args:
        text: The raw LLM response text
        format_hint: Optional hint about expected format (e.g., 'musicxml', 'mei')
                    Used to detect format-specific code block markers
    
    Returns:
        The cleaned text with code block delimiters removed
    
    Examples:
        >>> clean_code_blocks("```xml\\n<note/>\\n```")
        '<note/>'
        >>> clean_code_blocks("```musicxml\\n<score/>\\n```")
        '<score/>'
        >>> clean_code_blocks("<score/>")  # No change if no delimiters
        '<score/>'
    """
    if not text:
        return text
    
    # Build pattern for opening delimiter
    # Matches: ```xml, ```musicxml, ```mei, ```abc, ```humdrum, ```krn, or just ```
    format_patterns = r"(?:xml|musicxml|mei|abc|humdrum|krn)?"
    
    # Remove opening code block: ```format (with optional whitespace/newline)
    text = re.sub(rf'^```{format_patterns}\s*\n?', '', text, flags=re.IGNORECASE)
    
    # Remove closing code block: ``` (with optional preceding whitespace/newline)
    text = re.sub(r'\n?```\s*$', '', text)
    
    return text.strip()
