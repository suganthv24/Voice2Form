"""Text utility functions used across the pipeline."""

import re
import unicodedata


def normalize_text(text: str) -> str:
    """Apply NFC Unicode normalisation and collapse whitespace.

    Parameters
    ----------
    text:
        Raw transcription string (may contain combining characters or
        irregular whitespace from data entry).

    Returns
    -------
    str
        Cleaned, NFC-normalised string with leading/trailing whitespace
        removed and internal whitespace collapsed to single spaces.
    """
    text = str(text)
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
