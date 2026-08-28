from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# Project path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# RoadSafe imports

from src.data_loader import load_master_data

# Page configuration

st.set_page_config(
    page_title="RoadSafe India",
    page_icon="🚦",
    layout="wide"
)

# Load data

df = load_master_data()

# Title

st.title("RoadSafe India")

st.subheader(
    "A Data-Driven Analysis of Road Accident Risk, "
    "Severity and Trends in India"
)

st.markdown(
    """
    RoadSafe India explores reported road accidents and fatalities
    across Indian States/UTs using publicly available data.
    """
)

# 2024 OVERVIEW

st.header("India — 2024 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "States/UTs",
        f"{df['state'].nunique()}"
    )

with col2:
    st.metric(
        "Reported Accidents",
        f"{df['2024_accidents'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Reported Fatalities",
        f"{df['2024_killed'].sum():,.0f}"
    )

with col4:
    fatalities_per_100 = (
        df["2024_killed"].sum()
        / df["2024_accidents"].sum()
        * 100
    )

    st.metric(
        "Fatalities / 100 Accidents",
        f"{fatalities_per_100:.2f}"
    )

# NATIONAL TRENDS

st.header("National Trends — 2020 to 2024")

accident_columns = [
    "2020_accidents",
    "2021_accidents",
    "2022_accidents",
    "2023_accidents",
    "2024_accidents"
]

fatality_columns = [
    "2020_killed",
    "2021_killed",
    "2022_killed",
    "2023_killed",
    "2024_killed"
]

years = [2020, 2021, 2022, 2023, 2024]

national_accidents = pd.DataFrame({
    "Year": years,
    "Reported Accidents": df[
        accident_columns
    ].sum().values
})

national_fatalities = pd.DataFrame({
    "Year": years,
    "Reported Fatalities": df[
        fatality_columns
    ].sum().values
})

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    accident_fig = px.line(
        national_accidents,
        x="Year",
        y="Reported Accidents",
        markers=True,
        title="Reported Road Accidents"
    )

    accident_fig.update_layout(
        xaxis=dict(dtick=1)
    )

    st.plotly_chart(
        accident_fig,
        use_container_width=True
    )


with chart_col2:

    fatality_fig = px.line(
        national_fatalities,
        x="Year",
        y="Reported Fatalities",
        markers=True,
        title="Reported Road Fatalities"
    )

    fatality_fig.update_layout(
        xaxis=dict(dtick=1)
    )

    st.plotly_chart(
        fatality_fig,
        use_container_width=True
    )

# STATE COMPARISON

st.header("State/UT Comparison — 2024")

metric_options = {
    "Reported Accidents": "2024_accidents",
    "Reported Fatalities": "2024_killed",
    "Accidents per 100k Population":
        "accidents_per_100k_population",
    "Fatalities per 100k Population":
        "fatalities_per_100k_population",
    "Fatalities per 100 Reported Accidents":
        "fatalities_per_100_accidents"
}

selected_metric = st.selectbox(
    "Select metric:",
    list(metric_options.keys())
)

selected_column = metric_options[selected_metric]

top_n = st.slider(
    "Number of States/UTs to display:",
    min_value=5,
    max_value=20,
    value=10
)

comparison_df = (
    df[
        ["state", selected_column]
    ]
    .sort_values(
        selected_column,
        ascending=False
    )
    .head(top_n)
    .sort_values(
        selected_column,
        ascending=True
    )
)

comparison_fig = px.bar(
    comparison_df,
    x=selected_column,
    y="state",
    orientation="h",
    title=f"Top {top_n} States/UTs — {selected_metric}"
)

st.plotly_chart(
    comparison_fig,
    use_container_width=True
)

# STATE/UT TABLE
 
st.header("State/UT Data")

display_columns = [
    "state",
    "2024_accidents",
    "2024_killed",
    "accidents_per_100k_population",
    "fatalities_per_100k_population",
    "fatalities_per_100_accidents"
]

st.dataframe(
    df[
        display_columns
    ].sort_values(
        "2024_accidents",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)