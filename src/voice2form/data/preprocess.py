"""Dataset cleaning and text normalisation steps."""

import pandas as pd

from voice2form.utils.text_utils import normalize_text


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with missing or duplicate entries.

    Parameters
    ----------
    df:
        Raw input DataFrame.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame with duplicates and nulls removed.
    """
    df = df.dropna(subset=["transcription", "audio_filepath"])
    df = df.drop_duplicates(subset=["language", "transcription"])
    print("✅ After cleaning:", df.shape)
    return df.reset_index(drop=True)


def normalize_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Apply Unicode NFC normalisation and whitespace cleanup to all transcriptions.

    Parameters
    ----------
    df:
        DataFrame that has already been cleaned.

    Returns
    -------
    pd.DataFrame
        DataFrame with normalised ``transcription`` column.
    """
    df = df.copy()
    df["transcription"] = df["transcription"].map(normalize_text)
    print("✅ After normalisation sample:")
    print(df[["language", "transcription"]].head(5))
    return df
