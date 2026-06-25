import streamlit as st
import pandas as pd

from components.sidebar import apply_global_filters

from components.experience_chart import (
    calculate_branch_performance,
    render_scorecards_2a,
    render_scatter_4_kuadran,
    render_controls_2b,
    render_touchpoint_heatmap,
    render_friction_alert
)


@st.cache_data(show_spinner=False)
def load_mapping_data(mapping_path: str = "data/Master Mapping.csv") -> pd.DataFrame:
    """Load the branch mapping once and reuse it across page reruns."""
    return pd.read_csv(mapping_path)


def render_page(source_df: pd.DataFrame) -> None:
    """Render the Branch & Touchpoint Experience page from shared app data."""
    df = apply_global_filters(source_df.copy())

    if df.empty:
        st.warning(
            "No respondents match the currently selected sidebar filters. "
            "Reset or adjust the filters to display this page."
        )
        return

    mapping_path = "data/Master Mapping.csv"
    try:
        df_mapping = load_mapping_data(mapping_path)
    except Exception as exc:
        st.error(
            f"Unable to load the mapping file from `{mapping_path}`. "
            "Verify that the file exists and that its filename is correct."
        )
        st.caption(f"Technical detail: {exc}")
        return

    # ---------------------------------------------------------------------------
    # PAGE TITLE AND ANALYSIS NAVIGATION
    # ---------------------------------------------------------------------------
    st.title("Branch & Touchpoint Experience")
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    tabs = [
        "🏛️ Sub-Page 2A: Branch Performance & Loyalty Hub",
        "🔬 Sub-Page 2B: Deep-Dive Touchpoint & Head-to-Head Analysis",
    ]
    selected_tab = st.radio(
        "Analysis Navigation",
        tabs,
        label_visibility="collapsed",
    )
    st.markdown(
        "<hr style='margin-top:5px;margin-bottom:20px;border:none;border-top:1px solid #E9E9E9;'>",
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------------------------------
    # ANALYSIS ROUTING
    # ---------------------------------------------------------------------------
    if selected_tab == tabs[0]:
        # Branch performance and loyalty view
        branch_summary = calculate_branch_performance(df, df_mapping)
        render_scorecards_2a(df, branch_summary)

        with st.container(key="p2_large_card_1"):
            render_scatter_4_kuadran(branch_summary)

    elif selected_tab == tabs[1]:
        # Touchpoint comparison and queue-friction view
        with st.container(key="p2_card_filter"):
            st.markdown("""
            <div style="font-size:18px;font-weight:800;color:#1D2433;margin-bottom:15px;">
                Head-to-Head Touchpoint Analysis
            </div>
            """, unsafe_allow_html=True)

            selected_branches, selected_category = render_controls_2b(df, df_mapping)

        st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True) # Spacing between analysis cards

        if selected_branches:
            # Touchpoint heatmap
            with st.container(key="p2_card_heatmap"):
                render_touchpoint_heatmap(df, df_mapping, selected_branches, selected_category)

            st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True) # Spacing between analysis cards

            # Queue-friction indicators
            with st.container(key="p2_card_bullet"):
                render_friction_alert(df, selected_branches)

        else:
            st.info(
                "💡 Type and select up to 3 branch offices from the search bar above to begin the analysis."
            )
