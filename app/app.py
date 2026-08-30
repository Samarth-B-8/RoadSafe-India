from pathlib import Path
import sys
import json

import pandas as pd
import plotly.express as px
import streamlit as st


# =======================================================
# PROJECT PATH
# =======================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =======================================================
# ROADSAFE IMPORTS
# =======================================================

from src.data_loader import load_master_data
from src.insights import (
    generate_overview_insights,
    accident_fatality_correlation
)


# =======================================================
# PAGE CONFIGURATION
# =======================================================

st.set_page_config(
    page_title="RoadSafe India",
    page_icon="🚦",
    layout="wide"
)

# =======================================================
# CUSTOM STYLING
# =======================================================

st.markdown(
    """
    <style>

    /* Main application spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }


    /* Main page title */
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
    }


    /* Section headings */
    h2 {
        margin-top: 2rem;
        margin-bottom: 1rem;
    }


    h3 {
        margin-top: 1.5rem;
    }


    /* Sidebar */
    [data-testid="stSidebar"] {
        padding-top: 1rem;
    }

    [data-testid="stSidebar"] {
        padding: 1.5rem 1rem 1rem 1rem;
    }


    /* Brand */

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 0.8rem;
    }


    .brand-icon {
        font-size: 2rem;
        line-height: 1;
    }


    .brand-title {
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }


    .brand-subtitle {
        font-size: 0.72rem;
        margin-top: 0.15rem;
        opacity: 0.65;
        letter-spacing: 0.04em;
    }


    /* Description */

    .sidebar-description {
        font-size: 0.78rem;
        line-height: 1.55;
        opacity: 0.68;
        margin-top: 0.6rem;
    }


    /* Divider */

    .sidebar-divider {
        height: 1px;
        margin: 1.35rem 0;
        background: rgba(128, 128, 128, 0.25);
    }


    /* Section heading */

    .sidebar-section-title {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        opacity: 0.55;
        margin-bottom: 0.5rem;
    }


    /* Navigation */

    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.25rem;
    }


    [data-testid="stSidebar"] .stRadio label {
        border-radius: 10px;
        padding: 0.55rem 0.7rem;
        margin: 0.1rem 0;
        transition: all 0.2s ease;
    }


    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(128, 128, 128, 0.12);
    }


    /* Data coverage card */

    .coverage-card {
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        padding: 0.9rem;
        margin-top: 0.4rem;
        background: rgba(128, 128, 128, 0.06);
    }


    .coverage-title {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.11em;
        opacity: 0.55;
    }


    .coverage-value {
        font-size: 1rem;
        font-weight: 700;
        margin-top: 0.35rem;
    }


    .coverage-subtext {
        font-size: 0.72rem;
        opacity: 0.6;
        margin-top: 0.15rem;
    }


    /* Footer */

    .sidebar-footer {
        display: flex;
        justify-content: center;
        gap: 0.35rem;
        font-size: 0.65rem;
        opacity: 0.45;
        margin-top: 1.3rem;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #f7f8fa;
        border: 1px solid #e1e4e8;
        border-radius: 12px;
        padding: 1rem;
    }


    /* Metric labels */
    [data-testid="stMetricLabel"] {
        color: #222222 !important;
        font-size: 0.9rem;
    }


    /* Metric values */
    [data-testid="stMetricValue"] {
        color: #222222 !important;
        font-size: 1.8rem;
        font-weight: 700;
    }


    /* Metric value text inside the container */
    [data-testid="stMetricValue"] div {
        color: #222222 !important;
    }


    /* Metric label text */
    [data-testid="stMetricLabel"] div {
        color: #222222 !important;
    }


    /* Metric delta text, if used later */
    [data-testid="stMetricDelta"] {
        color: #222222 !important;
    }


    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }


    /* Captions */
    .stCaption {
        font-size: 0.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =======================================================
# LOAD MASTER DATA
# =======================================================

df = load_master_data()


# =======================================================
# CONSTANTS
# =======================================================

ACCIDENT_COLUMNS = [
    "2020_accidents",
    "2021_accidents",
    "2022_accidents",
    "2023_accidents",
    "2024_accidents"
]

FATALITY_COLUMNS = [
    "2020_killed",
    "2021_killed",
    "2022_killed",
    "2023_killed",
    "2024_killed"
]

YEARS = [2020, 2021, 2022, 2023, 2024]


# =======================================================
# SIDEBAR
# =======================================================

# =======================================================
# SIDEBAR
# =======================================================

st.sidebar.markdown(
    """
<div class="sidebar-brand">
    <div class="brand-icon">🚦</div>
    <div>
        <div class="brand-title">RoadSafe India</div>
        <div class="brand-subtitle">Road Safety Intelligence</div>
    </div>
</div>
""",
    unsafe_allow_html=True
)


st.sidebar.markdown(
    """
<div class="sidebar-description">
    Explore accident burden, fatalities, trends and
    population-normalized indicators across India.
</div>
""",
    unsafe_allow_html=True
)


st.sidebar.markdown(
    "<div class='sidebar-divider'></div>",
    unsafe_allow_html=True
)


st.sidebar.markdown(
    "<div class='sidebar-section-title'>EXPLORE</div>",
    unsafe_allow_html=True
)


page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Overview",
        "📈 State Comparison",
        "🗺️ Geographic View",
        "🔎 State Profile",
        "ℹ️ About RoadSafe"
    ],
    label_visibility="collapsed"
)


st.sidebar.markdown(
    "<div class='sidebar-divider'></div>",
    unsafe_allow_html=True
)


st.sidebar.markdown(
    f"""
<div class="coverage-card">
    <div class="coverage-title">DATA COVERAGE</div>
    <div class="coverage-value">2020 — 2024</div>
    <div class="coverage-subtext">
        {df['state'].nunique()} States / UTs
    </div>
</div>
""",
    unsafe_allow_html=True
)


st.sidebar.markdown(
    """
<div class="sidebar-footer">
    <span>RoadSafe India</span>
    <span>•</span>
    <span>Data Analysis</span>
</div>
""",
    unsafe_allow_html=True
)

# =======================================================
# PAGE 1 — OVERVIEW
# =======================================================

if page == "📊 Overview":

    st.title("RoadSafe India")

    st.markdown(
        """
        ### Road Accident Risk, Severity & Trends in India
        """
    )

    st.markdown(
        """
        Explore reported road accidents and fatalities across Indian
        States/UTs through trends, population-normalized indicators,
        geographic analysis and State-level comparisons.
        """
    )
    st.markdown(
        """
        RoadSafe India explores reported road accidents and fatalities
        across Indian States/UTs using publicly available data.
        """
    )


    # ---------------------------------------------------
    # 2024 overview
    # ---------------------------------------------------

    st.header("India — 2024 Overview")

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "States / UTs Covered",
            f"{df['state'].nunique()}"
        )


    with col2:

        st.metric(
            "2024 Reported Accidents",
            f"{df['2024_accidents'].sum():,.0f}"
        )


    with col3:

        st.metric(
            "2024 Reported Fatalities",
            f"{df['2024_killed'].sum():,.0f}"
        )


    with col4:

        fatalities_per_100 = (
            df["2024_killed"].sum()
            / df["2024_accidents"].sum()
            * 100
        )

        st.metric(
            "Fatalities per 100 Accidents",
            f"{fatalities_per_100:.2f}"
        )


    # ---------------------------------------------------
    # National trends
    # ---------------------------------------------------

    st.header("National Trends — 2020 to 2024")


    national_accidents = pd.DataFrame({
        "Year": YEARS,
        "Reported Accidents": df[
            ACCIDENT_COLUMNS
        ].sum().values
    })


    national_fatalities = pd.DataFrame({
        "Year": YEARS,
        "Reported Fatalities": df[
            FATALITY_COLUMNS
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
            width="stretch"
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
            width="stretch"
        )
    # =======================================================
    # KEY INSIGHTS
    # =======================================================

    st.header("Key Insights")

    overview_insights = generate_overview_insights(df)
    correlation = accident_fatality_correlation(df)

    st.info(
        "Reported accidents and reported fatalities show "
        f"a Pearson correlation of {correlation:.3f} across "
        "States/UTs in 2024."
    )

    for insight in overview_insights:

        st.info(insight)

# =======================================================
# PAGE 2 — STATE COMPARISON
# =======================================================

elif page == "📈 State Comparison":

    st.title("State/UT Comparison")

    st.markdown(
        """
        Compare States/UTs using absolute accident and fatality counts,
        as well as population-normalized indicators.
        """
    )


    metric_options = {

        "Reported Accidents":
            "2024_accidents",

        "Reported Fatalities":
            "2024_killed",

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


    selected_column = (
        metric_options[selected_metric]
    )


    top_n = st.slider(
        "Number of States/UTs:",
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
        title=(
            f"Top {top_n} States/UTs — "
            f"{selected_metric}"
        )
    )


    st.plotly_chart(
        comparison_fig,
        width="stretch"
    )


    st.subheader("State/UT Data")


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
        width="stretch",
        hide_index=True
    )


# =======================================================
# PAGE 3 — GEOGRAPHIC VIEW
# =======================================================

elif page == "🗺️ Geographic View":

    st.title("Geographic View")

    st.markdown(
        """
        Explore how reported accident and fatality burden varies
        geographically across India.
        """
    )


    # ---------------------------------------------------
    # GeoJSON path
    # ---------------------------------------------------

    geojson_path = (
        PROJECT_ROOT
        / "data"
        / "external"
        / "india_states_final.geojson"
    )


    if not geojson_path.exists():

        st.error(
            "State/UT GeoJSON file was not found."
        )

    else:

        with open(
            geojson_path,
            "r",
            encoding="utf-8"
        ) as file:

            india_geojson = json.load(file)


        # ------------------------------------------------
        # RoadSafe → GeoJSON names
        # ------------------------------------------------

        map_name_mapping = {

            "Andaman & Nicobar Islands":
                "Andaman and Nicobar",

            "N.C.T of Delhi":
                "Delhi",

            "Jammu & Kashmir":
                "Jammu and Kashmir",

            "Uttarakhand":
                "Uttaranchal"
        }


        map_df = df.copy()


        map_df["map_state"] = (
            map_df["state"]
            .astype(str)
            .str.strip()
            .replace(map_name_mapping)
        )


        # ------------------------------------------------
        # Create map key in GeoJSON
        # ------------------------------------------------

        for feature in india_geojson["features"]:

            state_name = (
                feature
                .get("properties", {})
                .get("state", "")
            )

            feature.setdefault(
                "properties",
                {}
            )["_map_state"] = (
                state_name.strip()
            )


        # ------------------------------------------------
        # Map metric
        # ------------------------------------------------

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
            list(map_metric_options.keys())
        )


        selected_map_column = (
            map_metric_options[
                selected_map_metric
            ]
        )


        # ------------------------------------------------
        # Map
        # ------------------------------------------------

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
            title=(
                f"2024 — {selected_map_metric}"
            ),
            color_continuous_scale="Viridis"
        )


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


        st.plotly_chart(
            map_fig,
            width="stretch"
        )


        st.caption(
            "Map geometry: State/UT boundaries. "
            "Analytical values: RoadSafe master dataset."
        )


# =======================================================
# PAGE 4 — STATE PROFILE
# =======================================================

elif page == "🔎 State Profile":

    st.title("State/UT Profile")

    st.markdown(
    """
    Select a State/UT to examine its 2024 indicators,
    national rankings and 2020–2024 trends.
    """
)

    selected_state = st.selectbox(
        "Select a State/UT:",
        sorted(
            df["state"]
            .dropna()
            .unique()
        )
    )


    state_data = df[
        df["state"] == selected_state
    ].iloc[0]


    # ---------------------------------------------------
    # State metrics
    # ---------------------------------------------------

    st.subheader(
        f"{selected_state} — 2024 Metrics"
    )


    col1, col2, col3, col4, col5 = (
        st.columns(5)
    )


    with col1:

        st.metric(
            "Reported Accidents",
            f"{state_data['2024_accidents']:,.0f}"
        )


    with col2:

        st.metric(
            "Reported Fatalities",
            f"{state_data['2024_killed']:,.0f}"
        )


    with col3:

        st.metric(
            "Accidents / 100k",
            f"{state_data['accidents_per_100k_population']:.2f}"
        )


    with col4:

        st.metric(
            "Fatalities / 100k",
            f"{state_data['fatalities_per_100k_population']:.2f}"
        )


    with col5:

        st.metric(
            "Fatalities / 100 Accidents",
            f"{state_data['fatalities_per_100_accidents']:.2f}"
        )


    # ---------------------------------------------------
    # State rankings
    # ---------------------------------------------------

    accident_rank = (
        df["2024_accidents"]
        .rank(
            ascending=False,
            method="min"
        )[
            df["state"] == selected_state
        ]
        .iloc[0]
    )


    fatality_rank = (
        df["2024_killed"]
        .rank(
            ascending=False,
            method="min"
        )[
            df["state"] == selected_state
        ]
        .iloc[0]
    )


    accident_rate_rank = (
        df["accidents_per_100k_population"]
        .rank(
            ascending=False,
            method="min"
        )[
            df["state"] == selected_state
        ]
        .iloc[0]
    )


    fatality_rate_rank = (
        df["fatalities_per_100k_population"]
        .rank(
            ascending=False,
            method="min"
        )[
            df["state"] == selected_state
        ]
        .iloc[0]
    )


    st.subheader(
        f"{selected_state} — National Ranking"
    )


    rank_col1, rank_col2, rank_col3, rank_col4 = (
        st.columns(4)
    )


    with rank_col1:

        st.metric(
            "Accident Rank",
            f"{int(accident_rank)} / {len(df)}"
        )


    with rank_col2:

        st.metric(
            "Fatality Rank",
            f"{int(fatality_rank)} / {len(df)}"
        )


    with rank_col3:

        st.metric(
            "Accident Rate Rank",
            f"{int(accident_rate_rank)} / {len(df)}"
        )


    with rank_col4:

        st.metric(
            "Fatality Rate Rank",
            f"{int(fatality_rate_rank)} / {len(df)}"
        )


    # ---------------------------------------------------
    # State vs average
    # ---------------------------------------------------

    average_accidents = (
        df["2024_accidents"].mean()
    )

    average_fatalities = (
        df["2024_killed"].mean()
    )

    average_accident_rate = (
        df["accidents_per_100k_population"].mean()
    )

    average_fatality_rate = (
        df["fatalities_per_100k_population"].mean()
    )


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
            average_accidents,
            average_fatalities,
            average_accident_rate,
            average_fatality_rate
        ]
    })


    display_benchmark = benchmark_data.copy()


    display_benchmark[selected_state] = (
        display_benchmark[selected_state]
        .map(
            lambda x: f"{x:,.2f}"
        )
    )


    display_benchmark["Average State/UT"] = (
        display_benchmark["Average State/UT"]
        .map(
            lambda x: f"{x:,.2f}"
        )
    )


    st.dataframe(
        display_benchmark,
        width="stretch",
        hide_index=True
    )


    # ---------------------------------------------------
    # State trends
    # ---------------------------------------------------

    st.subheader(
        f"{selected_state} — Historical Trends"
    )


    state_accident_trend = pd.DataFrame({

        "Year": YEARS,

        "Reported Accidents": [
            state_data["2020_accidents"],
            state_data["2021_accidents"],
            state_data["2022_accidents"],
            state_data["2023_accidents"],
            state_data["2024_accidents"]
        ]
    })


    state_fatality_trend = pd.DataFrame({

        "Year": YEARS,

        "Reported Fatalities": [
            state_data["2020_killed"],
            state_data["2021_killed"],
            state_data["2022_killed"],
            state_data["2023_killed"],
            state_data["2024_killed"]
        ]
    })


    trend_col1, trend_col2 = st.columns(2)


    with trend_col1:

        state_accident_fig = px.line(
            state_accident_trend,
            x="Year",
            y="Reported Accidents",
            markers=True,
            title=(
                f"{selected_state} — "
                "Reported Accidents"
            )
        )

        state_accident_fig.update_layout(
            xaxis=dict(dtick=1)
        )

        st.plotly_chart(
            state_accident_fig,
            width="stretch"
        )


    with trend_col2:

        state_fatality_fig = px.line(
            state_fatality_trend,
            x="Year",
            y="Reported Fatalities",
            markers=True,
            title=(
                f"{selected_state} — "
                "Reported Fatalities"
            )
        )

        state_fatality_fig.update_layout(
            xaxis=dict(dtick=1)
        )

        st.plotly_chart(
            state_fatality_fig,
            width="stretch"
        )


# =======================================================
# PAGE 5 — ABOUT
# =======================================================

elif page == "ℹ️ About RoadSafe":

    st.title("About RoadSafe India")

    st.markdown(
        """
        RoadSafe India is a data-driven road-safety analysis project
        that examines reported road accidents and fatalities across
        Indian States/UTs.
        """
    )

    st.header("What does RoadSafe analyse?")

    st.markdown(
        """
        **Accident burden**
        
        The number of reported road accidents across States/UTs.

        **Fatality burden**
        
        The number of reported road fatalities.

        **Population-normalized indicators**
        
        Reported accidents and fatalities per 100,000 projected population.

        **Fatality-to-accident indicator**
        
        Reported fatalities per 100 reported accidents.

        **Temporal trends**
        
        Changes in reported accidents and fatalities from 2020 to 2024.
        """
    )

    st.header("Study Period")

    st.info("2020–2024")

    st.header("Important Methodological Limitations")

    st.markdown(
        """
        **Population is an exposure proxy, not a complete exposure measure.**
        
        Population-normalized indicators do not directly capture
        vehicle-kilometres travelled, traffic volume or time spent on roads.

        **The population denominator is projected.**
        
        The 2024 State/UT population figures used by RoadSafe are
        projected population values rather than a 2024 Census enumeration.

        **Reported data has limitations.**
        
        Results depend on the underlying reporting and collection
        practices of the source datasets.

        **State-level observations are aggregated.**
        
        The statistical analysis uses State/UT-level observations rather
        than individual accident records.

        **Association does not imply causation.**
        
        Statistical relationships identified by RoadSafe should not be
        interpreted as evidence that one variable directly causes another.

        **2020 and 2021 were exceptional years.**
        
        Mobility conditions during this period differed substantially
        from normal conditions, so temporal comparisons should be
        interpreted carefully.
        """
    )

    st.header("Analytical Pipeline")

    st.code(
        """
    Government / Public Data
              ↓
        Data Understanding
              ↓
         Data Cleaning
              ↓
      Exploratory Analysis
              ↓
       Contextual Data
              ↓
      Master Analytical Data
              ↓
      Statistical Analysis
              ↓
      Interactive Dashboard
        """,
        language="text"
    )

    st.header("Project Structure")

    st.code(
        """
    data/        → Raw and processed datasets
    notebooks/   → Analysis and experimentation
    src/         → Reusable Python modules
    app/         → Streamlit dashboard
    tests/       → Project tests
    reports/     → Generated reports
        """,
        language="text"
    )

    st.caption(
        "RoadSafe India — Data Visualization & Analysis Project"
    )