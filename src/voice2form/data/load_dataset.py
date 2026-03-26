"""Load the ASR dataset from a CSV manifest file."""

import pandas as pd


def load_dataset(csv_file: str = "public_services_asr_manifest.csv") -> pd.DataFrame:
    """Read the CSV manifest and return a DataFrame.

    Parameters
    ----------
    csv_file:
        Path to the CSV file that contains the audio-text pairs.

    Returns
    -------
    pd.DataFrame
        DataFrame with all columns from the CSV manifest.
    """
    df = pd.read_csv(csv_file)
    print("✅ Dataset loaded:", df.shape)
    print(df.head(5))
    return df


if __name__ == "__main__":
    load_dataset()
