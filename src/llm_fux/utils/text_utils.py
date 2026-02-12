"""Text processing utilities for LLM responses."""

import logging
import re
import xml.etree.ElementTree as ET
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


def clean_response(text: str, datatype: str) -> str:
    """Clean an LLM response before saving.

    1. Strip markdown code fences (```xml ... ```).
    2. For XML-based formats (musicxml, mei), strip any text that precedes the
       first XML declaration or root element — LLMs sometimes prepend
       explanatory commentary.

    Args:
        text: Raw LLM response.
        datatype: Expected encoding format (musicxml, mei, abc, humdrum).

    Returns:
        Cleaned response text.
    """
    if not text:
        return text

    # Step 1: strip code fences
    text = clean_code_blocks(text, format_hint=datatype)

    # Step 2: for XML formats, strip preamble text before first XML content
    if datatype in ("musicxml", "mei"):
        # Look for <?xml or the root element tag
        xml_markers = [
            "<?xml",
            "<score-partwise",
            "<mei",
            "<!DOCTYPE",
        ]
        earliest = len(text)
        for marker in xml_markers:
            idx = text.find(marker)
            if idx != -1 and idx < earliest:
                earliest = idx
        if earliest < len(text) and earliest > 0:
            stripped = text[:earliest].strip()
            if stripped:
                logging.getLogger(__name__).info(
                    "Stripped %d chars of preamble text from %s response",
                    earliest, datatype,
                )
            text = text[earliest:]

    return text.strip()


# ---------------------------------------------------------------------------
# MusicXML duration repair
# ---------------------------------------------------------------------------

# Quarter-note multiples for each MusicXML <type> value.
_TYPE_TO_QUARTERS: dict[str, float] = {
    "whole": 4.0,
    "half": 2.0,
    "quarter": 1.0,
    "eighth": 0.5,
    "16th": 0.25,
    "32nd": 0.125,
}

logger = logging.getLogger(__name__)


def fix_musicxml_durations(xml_text: str) -> str:
    """Fix MusicXML duration values that don't match their note <type>.

    LLMs frequently set ``<divisions>2</divisions>`` (2 ticks per quarter)
    but write ``<duration>`` values as though divisions were 1.  This causes
    MuseScore to render invisible padding rests.

    The fix recalculates every ``<duration>`` from the note's ``<type>``
    (which is always correct) and the current ``<divisions>`` value, and
    also recalculates ``<backup>``/``<forward>`` durations so they equal
    the corrected measure length.

    If the XML cannot be parsed or no corrections are needed, the original
    text is returned unchanged.
    """
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return xml_text  # Not valid XML — nothing to fix.

    if root.tag != "score-partwise":
        return xml_text  # Not a partwise MusicXML document.

    fixes_applied = 0

    for part in root.findall("part"):
        divisions = 1  # MusicXML default

        for measure in part.findall("measure"):
            # Update divisions if declared in this measure's <attributes>.
            attr_div = measure.find("attributes/divisions")
            if attr_div is not None and attr_div.text:
                try:
                    divisions = int(attr_div.text)
                except ValueError:
                    pass

            # --- Pass 1: fix <note> durations from <type> ---------------
            for note in measure.findall("note"):
                note_type_el = note.find("type")
                dur_el = note.find("duration")
                if note_type_el is None or dur_el is None:
                    continue
                note_type = note_type_el.text
                if note_type not in _TYPE_TO_QUARTERS:
                    continue

                quarters = _TYPE_TO_QUARTERS[note_type]
                # Account for dotted notes (each dot adds half the previous).
                dots = note.findall("dot")
                dot_factor = sum(0.5 ** i for i in range(len(dots) + 1))
                quarters *= dot_factor

                expected = int(quarters * divisions)
                try:
                    actual = int(dur_el.text)
                except (ValueError, TypeError):
                    continue

                if actual != expected:
                    dur_el.text = str(expected)
                    fixes_applied += 1

            # --- Pass 2: fix <backup> and <forward> durations -----------
            # Expected measure length = beats * divisions (from <time>).
            time_el = measure.find("attributes/time")
            if time_el is not None:
                beats_el = time_el.find("beats")
                beat_type_el = time_el.find("beat-type")
                if beats_el is not None and beat_type_el is not None:
                    try:
                        beats = int(beats_el.text)
                        beat_type = int(beat_type_el.text)
                        measure_len = int(beats * (4.0 / beat_type) * divisions)
                    except (ValueError, TypeError):
                        measure_len = None
                else:
                    measure_len = None
            else:
                # Carry forward from previous measure (variable stays in scope).
                pass  # measure_len retains its value

            for tag in ("backup", "forward"):
                for elem in measure.findall(tag):
                    dur_el = elem.find("duration")
                    if dur_el is None:
                        continue
                    # Backup/forward should span the full measure if it
                    # separates two voices on the same staff.
                    if measure_len is not None:
                        try:
                            actual = int(dur_el.text)
                        except (ValueError, TypeError):
                            continue
                        if actual != measure_len:
                            dur_el.text = str(measure_len)
                            fixes_applied += 1

    if fixes_applied == 0:
        return xml_text  # Nothing changed — return original to preserve formatting.

    logger.info("Fixed %d MusicXML duration value(s)", fixes_applied)

    # Re-serialize. Preserve the XML declaration style the LLM used.
    raw = ET.tostring(root, encoding="unicode", xml_declaration=False)

    # Restore original XML declaration and DOCTYPE if present.
    header_lines: list[str] = []
    for line in xml_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("<?xml") or stripped.startswith("<!DOCTYPE"):
            header_lines.append(line)
        else:
            break

    if header_lines:
        return "\n".join(header_lines) + "\n" + raw + "\n"
    return raw + "\n"
