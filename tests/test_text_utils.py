"""Tests for text_utils module."""

import pytest
from llm_fux.utils.text_utils import clean_code_blocks, fix_musicxml_durations, clean_response


class TestCleanCodeBlocks:
    """Tests for the clean_code_blocks function."""

    def test_removes_xml_code_block(self):
        """Test removing ```xml ... ``` delimiters."""
        text = "```xml\n<note/>\n```"
        assert clean_code_blocks(text) == "<note/>"

    def test_removes_musicxml_code_block(self):
        """Test removing ```musicxml ... ``` delimiters."""
        text = "```musicxml\n<score-partwise/>\n```"
        assert clean_code_blocks(text) == "<score-partwise/>"

    def test_removes_plain_code_block(self):
        """Test removing ``` ... ``` delimiters without format specifier."""
        text = "```\n<content/>\n```"
        assert clean_code_blocks(text) == "<content/>"

    def test_no_change_without_delimiters(self):
        """Test that text without delimiters is unchanged."""
        text = "<score-partwise>\n  <part/>\n</score-partwise>"
        assert clean_code_blocks(text) == text

    def test_handles_empty_string(self):
        """Test that empty string returns empty string."""
        assert clean_code_blocks("") == ""

    def test_handles_none(self):
        """Test that None returns None."""
        assert clean_code_blocks(None) is None

    def test_preserves_internal_backticks(self):
        """Test that backticks within content are preserved."""
        text = "```xml\n<code>`example`</code>\n```"
        assert clean_code_blocks(text) == "<code>`example`</code>"

    def test_case_insensitive(self):
        """Test that format specifier matching is case insensitive."""
        text = "```XML\n<note/>\n```"
        assert clean_code_blocks(text) == "<note/>"


# ---------------------------------------------------------------------------
# MusicXML duration fix tests
# ---------------------------------------------------------------------------

def _make_musicxml(divisions: int, notes: str, time_sig: str = "4/4") -> str:
    """Build a minimal MusicXML score with one measure."""
    beats, beat_type = time_sig.split("/")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<score-partwise version="4.0">\n'
        '  <part-list><score-part id="P1"><part-name>P</part-name></score-part></part-list>\n'
        '  <part id="P1">\n'
        '    <measure number="1">\n'
        '      <attributes>\n'
        f'        <divisions>{divisions}</divisions>\n'
        '        <time>\n'
        f'          <beats>{beats}</beats>\n'
        f'          <beat-type>{beat_type}</beat-type>\n'
        '        </time>\n'
        '      </attributes>\n'
        f'      {notes}\n'
        '    </measure>\n'
        '  </part>\n'
        '</score-partwise>'
    )


class TestFixMusicxmlDurations:
    """Tests for fix_musicxml_durations."""

    def test_no_change_when_correct(self):
        """Already-correct durations should be returned unchanged."""
        xml = _make_musicxml(1, '<note><pitch><step>C</step><octave>4</octave></pitch>'
                                '<duration>4</duration><type>whole</type></note>')
        assert fix_musicxml_durations(xml) == xml

    def test_fixes_half_note_with_divisions_2(self):
        """Half note at divisions=2 should have duration=4, not 2."""
        xml = _make_musicxml(2, '<note><pitch><step>C</step><octave>4</octave></pitch>'
                                '<duration>2</duration><type>half</type></note>'
                                '<note><pitch><step>D</step><octave>4</octave></pitch>'
                                '<duration>2</duration><type>half</type></note>'
                                '<note><pitch><step>E</step><octave>4</octave></pitch>'
                                '<duration>2</duration><type>half</type></note>'
                                '<note><pitch><step>F</step><octave>4</octave></pitch>'
                                '<duration>2</duration><type>half</type></note>')
        fixed = fix_musicxml_durations(xml)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(fixed)
        durations = [int(d.text) for d in root.iter("duration")]
        assert all(d == 4 for d in durations), f"Expected all 4, got {durations}"

    def test_fixes_whole_note_with_divisions_2(self):
        """Whole note at divisions=2 should have duration=8, not 4."""
        xml = _make_musicxml(2, '<note><pitch><step>C</step><octave>4</octave></pitch>'
                                '<duration>4</duration><type>whole</type></note>')
        fixed = fix_musicxml_durations(xml)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(fixed)
        dur = root.find(".//note/duration")
        assert dur.text == "8"

    def test_fixes_backup_duration(self):
        """Backup element should span the full measure."""
        notes = (
            '<note><pitch><step>C</step><octave>5</octave></pitch>'
            '<duration>4</duration><type>whole</type><voice>1</voice><staff>1</staff></note>'
            '<backup><duration>4</duration></backup>'
            '<note><pitch><step>C</step><octave>4</octave></pitch>'
            '<duration>4</duration><type>whole</type><voice>2</voice><staff>2</staff></note>'
        )
        xml = _make_musicxml(2, notes)
        fixed = fix_musicxml_durations(xml)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(fixed)
        backup_dur = root.find(".//backup/duration")
        assert backup_dur.text == "8"

    def test_preserves_xml_declaration(self):
        """Original XML declaration and DOCTYPE should be preserved."""
        xml = _make_musicxml(2, '<note><pitch><step>C</step><octave>4</octave></pitch>'
                                '<duration>4</duration><type>whole</type></note>')
        fixed = fix_musicxml_durations(xml)
        assert fixed.startswith('<?xml version="1.0" encoding="UTF-8"?>')

    def test_returns_unchanged_for_non_xml(self):
        """Non-XML input should be returned as-is."""
        text = "This is not XML at all"
        assert fix_musicxml_durations(text) == text

    def test_returns_unchanged_for_non_musicxml(self):
        """Valid XML that isn't score-partwise should be returned as-is."""
        xml = '<root><child>text</child></root>'
        assert fix_musicxml_durations(xml) == xml

    def test_divisions_1_unchanged(self):
        """With divisions=1, standard durations are already correct."""
        xml = _make_musicxml(1, '<note><pitch><step>C</step><octave>4</octave></pitch>'
                                '<duration>2</duration><type>half</type></note>'
                                '<note><pitch><step>D</step><octave>4</octave></pitch>'
                                '<duration>2</duration><type>half</type></note>')
        assert fix_musicxml_durations(xml) == xml

    def test_quarter_note_with_divisions_2(self):
        """Quarter note at divisions=2 should have duration=2, not 1."""
        notes = ''.join(
            f'<note><pitch><step>C</step><octave>4</octave></pitch>'
            f'<duration>1</duration><type>quarter</type></note>'
            for _ in range(4)
        )
        xml = _make_musicxml(2, notes)
        fixed = fix_musicxml_durations(xml)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(fixed)
        durations = [int(d.text) for d in root.iter("duration")]
        assert all(d == 2 for d in durations)


class TestCleanResponse:
    """Tests for the clean_response function."""

    def test_strips_code_fences_musicxml(self):
        """Code fences around MusicXML should be stripped."""
        text = "```xml\n<?xml version=\"1.0\"?>\n<score-partwise/>\n```"
        result = clean_response(text, "musicxml")
        assert result.startswith("<?xml")
        assert "```" not in result

    def test_strips_preamble_text(self):
        """Explanatory text before XML should be stripped."""
        text = "Here is the counterpoint I composed:\n\n<?xml version=\"1.0\"?>\n<score-partwise/>"
        result = clean_response(text, "musicxml")
        assert result.startswith("<?xml")

    def test_strips_preamble_before_doctype(self):
        """Explanatory text before DOCTYPE should be stripped."""
        text = "Let me analyze the cantus firmus.\n\n<!DOCTYPE score-partwise>\n<score-partwise/>"
        result = clean_response(text, "musicxml")
        assert result.startswith("<!DOCTYPE")

    def test_no_change_clean_musicxml(self):
        """Already-clean MusicXML should be unchanged."""
        text = "<?xml version=\"1.0\"?>\n<score-partwise/>"
        assert clean_response(text, "musicxml") == text

    def test_handles_empty(self):
        assert clean_response("", "musicxml") == ""

    def test_handles_none(self):
        assert clean_response(None, "musicxml") is None
