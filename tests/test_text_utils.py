"""Tests for text utility helpers."""

import pytest

from voice2form.utils.text_utils import normalize_text


class TestNormalizeText:
    def test_collapses_whitespace(self):
        assert normalize_text("hello   world") == "hello world"

    def test_strips_leading_trailing_whitespace(self):
        assert normalize_text("  hello  ") == "hello"

    def test_nfc_normalization(self):
        # U+00E9 (é, precomposed) vs U+0065 + U+0301 (e + combining acute)
        nfd_char = "e\u0301"
        nfc_char = "\u00e9"
        assert normalize_text(nfd_char) == nfc_char

    def test_non_string_input_is_coerced(self):
        assert normalize_text(42) == "42"

    def test_empty_string(self):
        assert normalize_text("") == ""

    def test_newline_collapsed(self):
        assert normalize_text("line1\nline2") == "line1 line2"

    def test_tamil_text_unchanged(self):
        tamil = "வணக்கம்"
        assert normalize_text(tamil) == tamil
