"""Train / validation / test splitting and JSONL manifest generation."""

import json
from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


def split_dataset(
    df: pd.DataFrame,
    test_size: float = 0.2,
    val_ratio: float = 0.5,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split *df* into train, validation, and test sets.

    The split is stratified by language so that each language is represented
    proportionally in every split.

    Parameters
    ----------
    df:
        Fully preprocessed DataFrame.
    test_size:
        Fraction of data held out from training (combined val + test).
    val_ratio:
        Fraction of the held-out data used for validation (rest becomes test).
    random_state:
        Random seed for reproducibility.

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]
        ``(train, val, test)`` DataFrames.
    """
    train, temp = train_test_split(
        df,
        test_size=test_size,
        stratify=df["language"],
        random_state=random_state,
    )
    val, test = train_test_split(
        temp,
        test_size=val_ratio,
        stratify=temp["language"],
        random_state=random_state,
    )

    print("✅ Train size:", len(train))
    print("✅ Validation size:", len(val))
    print("✅ Test size:", len(test))
    return train, val, test


def save_manifests(
    train: pd.DataFrame,
    val: pd.DataFrame,
    test: pd.DataFrame,
    output_dir: str = "manifests",
) -> None:
    """Serialise each split to a JSONL manifest file.

    Each line in the output file is a JSON object with the keys
    ``audio_filepath``, ``transcription``, and ``language``.

    Parameters
    ----------
    train, val, test:
        DataFrames returned by :func:`split_dataset`.
    output_dir:
        Directory where the manifest files will be written.
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    splits = {"train": train, "validation": val, "test": test}

    for split_name, split_df in splits.items():
        out_path = Path(output_dir) / f"{split_name}_manifest.jsonl"
        with open(out_path, "w", encoding="utf-8") as fh:
            for _, row in split_df.iterrows():
                record = {
                    "audio_filepath": row["audio_filepath"],
                    "transcription": row["transcription"],
                    "language": row["language"],
                }
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"✅ {split_name} manifest saved → {out_path}")
