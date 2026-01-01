"""Tests for text_utils module."""

import pytest
from llm_fux.utils.text_utils import clean_code_blocks


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

    def test_removes_mei_code_block(self):
        """Test removing ```mei ... ``` delimiters."""
        text = "```mei\n<mei/>\n```"
        assert clean_code_blocks(text) == "<mei/>"

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

    def test_removes_abc_code_block(self):
        """Test removing ```abc ... ``` delimiters."""
        text = "```abc\nX:1\nT:Test\n```"
        assert clean_code_blocks(text) == "X:1\nT:Test"

    def test_removes_humdrum_code_block(self):
        """Test removing ```humdrum ... ``` delimiters."""
        text = "```humdrum\n**kern\n4c\n```"
        assert clean_code_blocks(text) == "**kern\n4c"
