import streamlit as st
import pandas as pd
import os
from components.sidebar import apply_global_filters

from components.competitor_chart import (
    render_competitor_kpis,
    render_competitor_macro_charts,
    render_competitor_heatmap
)



@st.cache_data(show_spinner=False)
def load_competitor_mapping() -> pd.DataFrame:
    """Load the competitor mapping once and reuse it across reruns."""
    path_1 = "data/Kompetitor Mapping.csv"
    path_2 = (
        "data/Mapping Touchpoint Bank XYZ vs Kompetitor - Page 3 - "
        "Mapping Touchpoint Bank XYZ vs Kompetitor - Page 3.csv"
    )

    if os.path.exists(path_1):
        return pd.read_csv(path_1)
    if os.path.exists(path_2):
        return pd.read_csv(path_2)

    raise FileNotFoundError(
        "Competitor mapping file was not found in the data directory."
    )


def render_page(source_df: pd.DataFrame) -> None:
    """Render the Competitor Performance page using shared app data."""
    df = apply_global_filters(source_df.copy())

    if df.empty:
        st.warning(
            "No respondents match the currently selected sidebar filters. "
            "Reset or adjust the filters to display this page."
        )
        return

    try:
        df_mapping_p3 = load_competitor_mapping()
    except Exception as exc:
        st.error(
            "Page 3 mapping file not found. Please make sure the mapping file is placed in the 'data/' folder."
        )
        st.caption(f"Technical detail: {exc}")
        return

    ##################################################################
    # HEADER
    ##################################################################

    st.title("Competitor Performance & Benchmarking")
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    ##################################################################
    # ROW 1 — KPI CARDS
    ##################################################################

    df_processed = render_competitor_kpis(df, df_mapping_p3)

    st.markdown(
        "<div style='height:18px;'></div>",
        unsafe_allow_html=True
    )

    ##################################################################
    # ROW 2 — MACRO CHARTS (BAR TOP 5 & RADAR CHART)
    ##################################################################

    render_competitor_macro_charts(df_processed, df_mapping_p3)

    st.markdown(
        "<div style='height:18px;'></div>",
        unsafe_allow_html=True
    )

    ##################################################################
    # ROW 3 — MICRO HEATMAP DEEP-DIVE
    ##################################################################

    render_competitor_heatmap(df_processed, df_mapping_p3)

