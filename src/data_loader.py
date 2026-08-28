from pathlib import Path

import pandas as pd


def load_master_data() -> pd.DataFrame:
    """
    Load the validated RoadSafe master State/UT dataset.

    Returns
    -------
    pd.DataFrame
        Master State/UT analytical dataset.
    """

    # Locate the RoadSafe project root.
    # data_loader.py is inside:
    # RoadSafe-India/src/
    project_root = Path(__file__).resolve().parent.parent

    # Build the path to the master dataset.
    data_path = (
        project_root
        / "data"
        / "processed"
        / "master_state_analysis_2024.csv"
    )

    # Give a clear error if the dataset does not exist.
    if not data_path.exists():
        raise FileNotFoundError(
            f"Master dataset not found at: {data_path}"
        )

    # Load and return the dataset.
    df = pd.read_csv(data_path)

    return df