"""Tests for dataset cleaning and normalisation."""

import pandas as pd
import pytest

from voice2form.data.preprocess import clean_dataset, normalize_dataset


@pytest.fixture()
def sample_df():
    return pd.DataFrame(
        {
            "audio_filepath": [
                "audio/001.wav",
                "audio/002.wav",
                "audio/003.wav",
                None,
            ],
            "transcription": [
                "ஆதார் கார்டு",
                "आधार कार्ड",
                "ఆధార్ కార్డు",
                "missing audio",
            ],
            "language": ["Tamil", "Hindi", "Telugu", "Tamil"],
        }
    )


class TestCleanDataset:
    def test_drops_null_audio_filepath(self, sample_df):
        cleaned = clean_dataset(sample_df)
        assert cleaned["audio_filepath"].notna().all()

    def test_shape_after_cleaning(self, sample_df):
        cleaned = clean_dataset(sample_df)
        assert len(cleaned) == 3

    def test_drops_duplicates(self):
        df = pd.DataFrame(
            {
                "audio_filepath": ["a.wav", "b.wav"],
                "transcription": ["hello", "hello"],
                "language": ["Tamil", "Tamil"],
            }
        )
        cleaned = clean_dataset(df)
        assert len(cleaned) == 1

    def test_resets_index(self, sample_df):
        cleaned = clean_dataset(sample_df)
        assert list(cleaned.index) == list(range(len(cleaned)))


class TestNormalizeDataset:
    def test_normalizes_transcription_column(self):
        df = pd.DataFrame(
            {
                "audio_filepath": ["a.wav"],
                "transcription": ["  hello   world  "],
                "language": ["Tamil"],
            }
        )
        result = normalize_dataset(df)
        assert result["transcription"].iloc[0] == "hello world"

    def test_does_not_modify_original(self, sample_df):
        original_transcription = sample_df["transcription"].iloc[0]
        normalize_dataset(sample_df)
        assert sample_df["transcription"].iloc[0] == original_transcription
