import pandas as pd

def get_top_state(
    df: pd.DataFrame,
    column: str
) -> pd.Series:
    """
    Return the State/UT with the highest value
    for a specified column.
    """

    return df.loc[
        df[column].idxmax()
    ]

def generate_overview_insights(
    df: pd.DataFrame
) -> list[str]:
    """
    Generate dashboard insight statements from
    the RoadSafe master analytical dataset.
    """

    insights = []

    # Highest accident count

    top_accidents = get_top_state(
        df,
        "2024_accidents"
    )

    insights.append(
        f"{top_accidents['state']} recorded the "
        f"highest number of reported accidents in 2024 "
        f"({top_accidents['2024_accidents']:,.0f})."
    )

    # Highest fatality count

    top_fatalities = get_top_state(
        df,
        "2024_killed"
    )

    insights.append(
        f"{top_fatalities['state']} recorded the "
        f"highest number of reported fatalities in 2024 "
        f"({top_fatalities['2024_killed']:,.0f})."
    )

    # Highest accident rate

    top_accident_rate = get_top_state(
        df,
        "accidents_per_100k_population"
    )

    insights.append(
        f"{top_accident_rate['state']} had the highest "
        f"reported accidents per 100,000 projected "
        f"population ({top_accident_rate['accidents_per_100k_population']:.2f})."
    )

    # Highest fatality rate

    top_fatality_rate = get_top_state(
        df,
        "fatalities_per_100k_population"
    )

    insights.append(
        f"{top_fatality_rate['state']} had the highest "
        f"reported fatalities per 100,000 projected "
        f"population ({top_fatality_rate['fatalities_per_100k_population']:.2f})."
    )

    return insights

def accident_fatality_correlation(
    df: pd.DataFrame
) -> float:
    """
    Calculate the Pearson correlation between
    reported accidents and reported fatalities.
    """

    return df[
        [
            "2024_accidents",
            "2024_killed"
        ]
    ].corr().loc[
        "2024_accidents",
        "2024_killed"
    ]