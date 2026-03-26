"""Tests for dataset splitting and manifest generation."""

import json
import textwrap
from pathlib import Path

import pandas as pd
import pytest

from voice2form.data.split import save_manifests, split_dataset


@pytest.fixture()
def sample_df():
    """Small stratified DataFrame (6 rows, 2 per language)."""
    rows = []
    for lang in ["Tamil", "Hindi", "Telugu"]:
        for i in range(4):
            rows.append(
                {
                    "audio_filepath": f"audio/{lang}_{i:03d}.wav",
                    "transcription": f"{lang} sentence {i}",
                    "language": lang,
                }
            )
    return pd.DataFrame(rows)


class TestSplitDataset:
    def test_total_rows_preserved(self, sample_df):
        train, val, test = split_dataset(sample_df, test_size=0.5, val_ratio=0.5)
        assert len(train) + len(val) + len(test) == len(sample_df)

    def test_no_overlap_between_splits(self, sample_df):
        train, val, test = split_dataset(sample_df, test_size=0.5, val_ratio=0.5)
        train_idx = set(train.index)
        val_idx = set(val.index)
        test_idx = set(test.index)
        assert train_idx.isdisjoint(val_idx)
        assert train_idx.isdisjoint(test_idx)
        assert val_idx.isdisjoint(test_idx)


class TestSaveManifests:
    def test_files_created(self, sample_df, tmp_path):
        train, val, test = split_dataset(sample_df, test_size=0.5, val_ratio=0.5)
        save_manifests(train, val, test, output_dir=str(tmp_path))
        for name in ("train", "validation", "test"):
            assert (tmp_path / f"{name}_manifest.jsonl").exists()

    def test_valid_jsonl(self, sample_df, tmp_path):
        train, val, test = split_dataset(sample_df, test_size=0.5, val_ratio=0.5)
        save_manifests(train, val, test, output_dir=str(tmp_path))
        manifest_path = tmp_path / "train_manifest.jsonl"
        lines = manifest_path.read_text(encoding="utf-8").strip().splitlines()
        for line in lines:
            record = json.loads(line)
            assert "audio_filepath" in record
            assert "transcription" in record
            assert "language" in record
