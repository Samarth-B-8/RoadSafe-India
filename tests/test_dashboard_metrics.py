import pandas as pd
import pytest

# Load master dataset

DATA_PATH = (
    "data/processed/"
    "master_state_analysis_2024.csv"
)


@pytest.fixture
def master_df():
    return pd.read_csv(DATA_PATH)

# TEST 1 — State/UT coverage

def test_state_count(master_df):

    assert master_df["state"].nunique() == 36


def test_no_duplicate_states(master_df):

    assert master_df["state"].duplicated().sum() == 0

# TEST 2 — 2024 accident total

def test_2024_accident_total(master_df):

    total_accidents = (
        master_df["2024_accidents"]
        .sum()
    )

    assert total_accidents == 487707

# TEST 3 — 2024 fatality total

def test_2024_fatality_total(master_df):

    total_fatalities = (
        master_df["2024_killed"]
        .sum()
    )

    assert total_fatalities == 177175

# TEST 4 — Highest accident-count State

def test_highest_accident_state(master_df):

    top_state = master_df.loc[
        master_df["2024_accidents"].idxmax(),
        "state"
    ]

    assert top_state == "Tamil Nadu"

def test_highest_accident_value(master_df):

    top_accidents = (
        master_df["2024_accidents"]
        .max()
    )

    assert top_accidents == 67526

# TEST 5 — Highest fatality-count State

def test_highest_fatality_state(master_df):

    top_state = master_df.loc[
        master_df["2024_killed"].idxmax(),
        "state"
    ]

    assert top_state == "Uttar Pradesh"

def test_highest_fatality_value(master_df):

    top_fatalities = (
        master_df["2024_killed"]
        .max()
    )

    assert top_fatalities == 24118

# TEST 6 — Rate calculations

def test_accident_rate_formula(master_df):

    sample = master_df.iloc[0]

    expected = (
        sample["2024_accidents"]
        / sample["population_2024"]
        * 100000
    )

    actual = sample[
        "accidents_per_100k_population"
    ]

    assert actual == pytest.approx(
        expected,
        rel=1e-6
    )

def test_fatality_rate_formula(master_df):

    sample = master_df.iloc[0]

    expected = (
        sample["2024_killed"]
        / sample["population_2024"]
        * 100000
    )

    actual = sample[
        "fatalities_per_100k_population"
    ]

    assert actual == pytest.approx(
        expected,
        rel=1e-6
    )

# TEST 7 — Fatality per accident formula

def test_fatality_accident_ratio(master_df):

    sample = master_df.iloc[0]

    expected = (
        sample["2024_killed"]
        / sample["2024_accidents"]
        * 100
    )

    actual = sample[
        "fatalities_per_100_accidents"
    ]

    assert actual == pytest.approx(
        expected,
        rel=1e-6
    )