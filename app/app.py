from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

import json

# PROJECT PATH

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ROADSAFE IMPORTS

from src.data_loader import load_master_data

# PAGE CONFIGURATION

st.set_page_config(
    page_title="RoadSafe India",
    page_icon="🚦",
    layout="wide"
)

# LOAD MASTER DATASET

df = load_master_data()

# HEADER

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

# National accident totals

national_accidents = pd.DataFrame({
    "Year": years,
    "Reported Accidents": df[
        accident_columns
    ].sum().values
})

# National fatality totals

national_fatalities = pd.DataFrame({
    "Year": years,
    "Reported Fatalities": df[
        fatality_columns
    ].sum().values
})

# Plot national trends

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
    list(metric_options.keys()),
    key="comparison_metric"
)

selected_column = metric_options[selected_metric]

top_n = st.slider(
    "Number of States/UTs to display:",
    min_value=5,
    max_value=20,
    value=10,
    key="comparison_top_n"
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
# =======================================================
# GEOGRAPHIC VIEW
# =======================================================

st.header("Geographic View — 2024")

import json


# -------------------------------------------------------
# Load dissolved State/UT GeoJSON
# -------------------------------------------------------

geojson_path = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "india_states_final.geojson"
)


if not geojson_path.exists():

    st.error(
        "State-level GeoJSON file was not found."
    )

else:

    with open(
        geojson_path,
        "r",
        encoding="utf-8"
    ) as file:

        india_geojson = json.load(file)


    # ---------------------------------------------------
    # Prepare map DataFrame
    # ---------------------------------------------------

    map_df = df.copy()


    # ---------------------------------------------------
    # RoadSafe → GeoJSON name mapping
    # ---------------------------------------------------

    map_name_mapping = {

    "Andaman & Nicobar Islands":
        "Andaman and Nicobar",

    "N.C.T of Delhi":
        "Delhi",

    "Jammu & Kashmir":
        "Jammu and Kashmir",
    }

    map_df["map_state"] = (
        map_df["state"]
        .astype(str)
        .str.strip()
        .replace(map_name_mapping)
    )


    # ---------------------------------------------------
    # Add normalized GeoJSON key
    # ---------------------------------------------------

    for feature in india_geojson["features"]:

        state_name = (
            feature
            .get("properties", {})
            .get("state", "")
        )

        feature.setdefault(
            "properties",
            {}
        )["_map_state"] = state_name.strip()


    # ---------------------------------------------------
    # Map metric selector
    # ---------------------------------------------------

    map_metric_options = {

        "Reported Accidents":
            "2024_accidents",

        "Reported Fatalities":
            "2024_killed",

        "Accidents per 100k Population":
            "accidents_per_100k_population",

        "Fatalities per 100k Population":
            "fatalities_per_100k_population"
    }


    selected_map_metric = st.selectbox(
        "Select map metric:",
        list(map_metric_options.keys()),
        key="map_metric"
    )


    selected_map_column = (
        map_metric_options[selected_map_metric]
    )


    # ---------------------------------------------------
    # Create State-level choropleth
    # ---------------------------------------------------

    map_fig = px.choropleth(
        map_df,

        geojson=india_geojson,

        locations="map_state",

        featureidkey="properties._map_state",

        color=selected_map_column,

        hover_name="state",

        hover_data={
            "map_state": False,
            "2024_accidents": ":,.0f",
            "2024_killed": ":,.0f",
            "accidents_per_100k_population": ":.2f",
            "fatalities_per_100k_population": ":.2f",
            "fatalities_per_100_accidents": ":.2f"
        },

        title=f"2024 — {selected_map_metric}",

        color_continuous_scale="Viridis"
    )


    # ---------------------------------------------------
    # Map appearance
    # ---------------------------------------------------

    map_fig.update_geos(
        fitbounds="locations",
        visible=False
    )


    map_fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            t=55,
            b=0
        )
    )


    # ---------------------------------------------------
    # Display map
    # ---------------------------------------------------

    st.plotly_chart(
        map_fig,
        width="stretch"
    )


    st.caption(
        "Map geometry: State/UT boundaries. "
        "Analytical values: RoadSafe master dataset."
    )  
# STATE PROFILE

st.header("State/UT Profile")

selected_state = st.selectbox(
    "Select a State/UT:",
    sorted(
        df["state"]
        .dropna()
        .unique()
    ),
    key="selected_state"
)

# Get selected State

state_data = df[
    df["state"] == selected_state
].iloc[0]

# STATE METRICS

profile_col1, profile_col2, profile_col3, profile_col4, profile_col5 = (
    st.columns(5)
)

with profile_col1:
    st.metric(
        "2024 Accidents",
        f"{state_data['2024_accidents']:,.0f}"
    )

with profile_col2:
    st.metric(
        "2024 Fatalities",
        f"{state_data['2024_killed']:,.0f}"
    )

with profile_col3:
    st.metric(
        "Accidents / 100k Population",
        f"{state_data['accidents_per_100k_population']:.2f}"
    )

with profile_col4:
    st.metric(
        "Fatalities / 100k Population",
        f"{state_data['fatalities_per_100k_population']:.2f}"
    )

with profile_col5:
    st.metric(
        "Fatalities / 100 Accidents",
        f"{state_data['fatalities_per_100_accidents']:.2f}"
    )

# NATIONAL BENCHMARKING

st.subheader(
    f"{selected_state} — National Comparison"
)

# Average State/UT values

average_accidents_per_state = (
    df["2024_accidents"].mean()
)

average_fatalities_per_state = (
    df["2024_killed"].mean()
)

average_accident_rate = (
    df["accidents_per_100k_population"].mean()
)

average_fatality_rate = (
    df["fatalities_per_100k_population"].mean()
)

# State rankings

accident_ranks = (
    df["2024_accidents"]
    .rank(
        ascending=False,
        method="min"
    )
)

fatality_ranks = (
    df["2024_killed"]
    .rank(
        ascending=False,
        method="min"
    )
)

accident_rate_ranks = (
    df["accidents_per_100k_population"]
    .rank(
        ascending=False,
        method="min"
    )
)

fatality_rate_ranks = (
    df["fatalities_per_100k_population"]
    .rank(
        ascending=False,
        method="min"
    )
)

accident_rank = accident_ranks[
    df["state"] == selected_state
].iloc[0]

fatality_rank = fatality_ranks[
    df["state"] == selected_state
].iloc[0]

accident_rate_rank = accident_rate_ranks[
    df["state"] == selected_state
].iloc[0]

fatality_rate_rank = fatality_rate_ranks[
    df["state"] == selected_state
].iloc[0]

# Display rankings

benchmark_col1, benchmark_col2, benchmark_col3, benchmark_col4 = (
    st.columns(4)
)

with benchmark_col1:
    st.metric(
        "Accident Rank",
        f"{int(accident_rank)} / {len(df)}"
    )

with benchmark_col2:
    st.metric(
        "Fatality Rank",
        f"{int(fatality_rank)} / {len(df)}"
    )

with benchmark_col3:
    st.metric(
        "Accident Rate Rank",
        f"{int(accident_rate_rank)} / {len(df)}"
    )

with benchmark_col4:
    st.metric(
        "Fatality Rate Rank",
        f"{int(fatality_rate_rank)} / {len(df)}"
    )

# STATE VS AVERAGE TABLE

benchmark_data = pd.DataFrame({
    "Metric": [
        "Reported Accidents",
        "Reported Fatalities",
        "Accidents per 100k Population",
        "Fatalities per 100k Population"
    ],
    selected_state: [
        state_data["2024_accidents"],
        state_data["2024_killed"],
        state_data["accidents_per_100k_population"],
        state_data["fatalities_per_100k_population"]
    ],
    "Average State/UT": [
        average_accidents_per_state,
        average_fatalities_per_state,
        average_accident_rate,
        average_fatality_rate
    ]
})

# Create a separate display copy.
# This prevents us from changing numerical data
# into strings inside the analytical DataFrame.

display_benchmark = benchmark_data.copy()

display_benchmark[selected_state] = (
    display_benchmark[selected_state]
    .map(lambda x: f"{x:,.2f}")
)

display_benchmark["Average State/UT"] = (
    display_benchmark["Average State/UT"]
    .map(lambda x: f"{x:,.2f}")
)

st.dataframe(
    display_benchmark,
    use_container_width=True,
    hide_index=True
)

# STATE VS AVERAGE CHART

benchmark_chart_df = pd.DataFrame({
    "Metric": [
        "Accidents",
        "Fatalities"
    ],
    selected_state: [
        state_data["2024_accidents"],
        state_data["2024_killed"]
    ],
    "Average State/UT": [
        average_accidents_per_state,
        average_fatalities_per_state
    ]
})

benchmark_long = benchmark_chart_df.melt(
    id_vars="Metric",
    var_name="Group",
    value_name="Value"
)

benchmark_fig = px.bar(
    benchmark_long,
    x="Metric",
    y="Value",
    color="Group",
    barmode="group",
    title=f"{selected_state} vs Average State/UT"
)

st.plotly_chart(
    benchmark_fig,
    use_container_width=True
)

# STATE TRENDS
st.subheader(
    f"{selected_state} — Historical Trends"
)

# Accident trend

state_accident_trend = pd.DataFrame({
    "Year": years,
    "Reported Accidents": [
        state_data["2020_accidents"],
        state_data["2021_accidents"],
        state_data["2022_accidents"],
        state_data["2023_accidents"],
        state_data["2024_accidents"]
    ]
})

# Fatality trend

state_fatality_trend = pd.DataFrame({
    "Year": years,
    "Reported Fatalities": [
        state_data["2020_killed"],
        state_data["2021_killed"],
        state_data["2022_killed"],
        state_data["2023_killed"],
        state_data["2024_killed"]
    ]
})

# Plot State trends

trend_col1, trend_col2 = st.columns(2)

with trend_col1:

    state_accident_fig = px.line(
        state_accident_trend,
        x="Year",
        y="Reported Accidents",
        markers=True,
        title=f"{selected_state} — Reported Accidents"
    )

    state_accident_fig.update_layout(
        xaxis=dict(dtick=1)
    )

    st.plotly_chart(
        state_accident_fig,
        use_container_width=True
    )

with trend_col2:

    state_fatality_fig = px.line(
        state_fatality_trend,
        x="Year",
        y="Reported Fatalities",
        markers=True,
        title=f"{selected_state} — Reported Fatalities"
    )

    state_fatality_fig.update_layout(
        xaxis=dict(dtick=1)
    )

    st.plotly_chart(
        state_fatality_fig,
        use_container_width=True
    )

# STATE/UT DATA TABLE

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