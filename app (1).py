
import streamlit as st

from components.sidebar import render_sidebar
from helpers.loader import load_data
from pages.page1 import render_page as render_respondent_profile
from pages.page2 import render_page as render_bank_performance
from pages.page3 import render_page as render_competitor_performance


# ──────────────────────────────────────────────────────────────────────────────
# 1. PAGE CONFIG
# Must remain the first Streamlit command in the application.
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bank XYZ CX Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ──────────────────────────────────────────────────────────────────────────────
# 2. GLOBAL DESIGN SYSTEM
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0,0" rel="stylesheet">

    <style>
    :root {
        --cx-blue: #0069FF;
        --cx-blue-dark: #0055D4;
        --cx-red: #BB2649;
        --cx-red-soft: #FFF0F4;
        --cx-red-dark: #9F1F3E;
        --cx-red-border: #FFC3D4;
        --cx-green: #2FBF71;
        --cx-text-primary: #1D2433;
        --cx-text-secondary: #5E6677;
        --cx-text-muted: #98A1B3;
        --cx-page-bg: #FFF5F8;
        --cx-card-bg: #FFFFFF;
        --cx-chart-bg: #FCFDFF;
        --cx-border: #E8ECF2;
        --cx-shadow: 0 10px 22px rgba(29, 36, 51, 0.06);
        --cx-shadow-hover: 0 18px 30px rgba(29, 36, 51, 0.10);
    }

    html,
    body,
    [data-testid="stAppViewContainer"],
    button,
    input,
    textarea,
    select {
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        color: var(--cx-text-primary);
    }

    p,
    label,
    [data-testid="stCaptionContainer"] {
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        color: var(--cx-text-secondary);
    }

    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-symbols-outlined {
        font-family: "Material Symbols Rounded" !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 20px !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: "liga" !important;
        -webkit-font-smoothing: antialiased !important;
        font-feature-settings: "liga" !important;
    }

    [data-testid="stAppViewContainer"] {
        background: var(--cx-page-bg) !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Hide Streamlit's automatic pages navigation. */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNavItems"],
    section[data-testid="stSidebar"] nav {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }

    .block-container {
        max-width: 100% !important;
        padding-top: 1.5rem !important;
        padding-right: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
    }

    h1,
    h2,
    h3 {
        color: var(--cx-text-primary) !important;
        letter-spacing: -0.03em !important;
    }

    h1 {
        font-size: 2rem !important;
        font-weight: 800 !important;
    }


    #MainMenu,
    footer,
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarResizer"] {
        visibility: hidden !important;
        display: none !important;
    }

    /* KPI cards */
    .st-key-card_kpi_1,
    .st-key-card_kpi_2,
    .st-key-card_kpi_3,
    .st-key-card_kpi_4,
    .st-key-card_kpi_5,
    .st-key-kpi_comp_1,
    .st-key-kpi_comp_2,
    .st-key-kpi_comp_3,
    .st-key-kpi_comp_4 {
        height: 150px !important;
        display: flex !important;
        align-items: center !important;
        padding: 1.35rem !important;
        overflow: hidden !important;
        background: var(--cx-card-bg) !important;
        border: 1px solid rgba(232, 236, 242, 0.75) !important;
        border-radius: 18px !important;
        box-shadow: var(--cx-shadow) !important;
        transition: transform 0.22s ease, box-shadow 0.22s ease !important;
    }

    /* Chart and analysis containers */
    .st-key-large_card_1,
    .st-key-large_card_2,
    .st-key-medium_card_1,
    .st-key-medium_card_2,
    .st-key-geomap_card,
    .st-key-p2_large_card_1,
    .st-key-p2_card_filter,
    .st-key-p2_card_heatmap,
    .st-key-p2_card_bullet,
    .st-key-p1_card_bubble,
    .st-key-p1_card_persona,
    .st-key-p3_card_bar,
    .st-key-p3_card_radar,
    .st-key-p3_card_filter,
    .st-key-p3_card_heatmap {
        padding: 1.4rem !important;
        overflow: visible !important;
        background: var(--cx-chart-bg) !important;
        border: 1px solid rgba(232, 236, 242, 0.75) !important;
        border-radius: 18px !important;
        box-shadow: var(--cx-shadow) !important;
        transition: transform 0.22s ease, box-shadow 0.22s ease !important;
    }

    .st-key-p1_card_bubble,
    .st-key-p1_card_persona {
        height: 480px !important;
    }

    .st-key-card_kpi_1:hover,
    .st-key-card_kpi_2:hover,
    .st-key-card_kpi_3:hover,
    .st-key-card_kpi_4:hover,
    .st-key-card_kpi_5:hover,
    .st-key-kpi_comp_1:hover,
    .st-key-kpi_comp_2:hover,
    .st-key-kpi_comp_3:hover,
    .st-key-kpi_comp_4:hover,
    .st-key-large_card_1:hover,
    .st-key-large_card_2:hover,
    .st-key-medium_card_1:hover,
    .st-key-medium_card_2:hover,
    .st-key-geomap_card:hover,
    .st-key-p2_large_card_1:hover,
    .st-key-p2_card_filter:hover,
    .st-key-p2_card_heatmap:hover,
    .st-key-p2_card_bullet:hover,
    .st-key-p1_card_bubble:hover,
    .st-key-p1_card_persona:hover,
    .st-key-p3_card_bar:hover,
    .st-key-p3_card_radar:hover,
    .st-key-p3_card_filter:hover,
    .st-key-p3_card_heatmap:hover {
        transform: translateY(-2px);
        box-shadow: var(--cx-shadow-hover) !important;
    }

    /* Shared KPI typography */
    .kpi-title {
        color: var(--cx-text-secondary) !important;
        font-size: 12px !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        text-transform: uppercase;
    }

    .kpi-value-large {
        color: var(--cx-text-primary) !important;
        font-size: 30px !important;
        font-weight: 800 !important;
        line-height: 1 !important;
        letter-spacing: -0.04em !important;
    }

    .kpi-subtitle {
        color: var(--cx-text-muted) !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }

    .saving-positive {
        color: var(--cx-green) !important;
    }

    .saving-negative {
        color: var(--cx-red) !important;
    }

    /* Page-level tab radios only; sidebar navigation is handled separately. */
    .main div.stRadio > div[role="radiogroup"] {
        display: flex;
        flex-direction: row;
        gap: 8px;
    }

    .main div.stRadio > div[role="radiogroup"] label {
        min-height: 40px;
        padding: 9px 16px;
        cursor: pointer;
        background: #FFFFFF;
        border: 1px solid var(--cx-border);
        border-radius: 10px;
        transition: all 0.18s ease;
    }

    .main div.stRadio > div[role="radiogroup"] label:hover {
        border-color: var(--cx-red-border);
        background: var(--cx-red-soft);
    }

    .main div.stRadio > div[role="radiogroup"] label:has(input:checked) {
        color: #FFFFFF !important;
        background: linear-gradient(135deg, var(--cx-red), var(--cx-red-dark)) !important;
        border-color: transparent !important;
        box-shadow: 0 7px 16px rgba(187, 38, 73, 0.20);
    }

    .main div.stRadio > div[role="radiogroup"] label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    .js-plotly-plot .plotly .modebar {
        display: none !important;
    }

    @media (max-width: 1100px) {
        .block-container {
            padding-right: 1.2rem !important;
            padding-left: 1.2rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────────────────────────────────────
# 3. CENTRALIZED APPLICATION DATA
# Load the source dataframe once per user session and share it with every page.
# ──────────────────────────────────────────────────────────────────────────────
if "cx_source_df" not in st.session_state:
    st.session_state["cx_source_df"] = load_data()

app_df = st.session_state["cx_source_df"]


# ──────────────────────────────────────────────────────────────────────────────
# 4. SHARED SIDEBAR
# The sidebar is rendered once by the application shell, not by individual pages.
# ──────────────────────────────────────────────────────────────────────────────
render_sidebar(app_df)


# ──────────────────────────────────────────────────────────────────────────────
# 5. CENTRALIZED PAGE ROUTING
# Render pages directly from session state to avoid browser-level page reloads.
# ──────────────────────────────────────────────────────────────────────────────
current_page = st.session_state.get(
    "cx_current_page",
    "respondent_profile",
)

if current_page == "respondent_profile":
    render_respondent_profile(app_df)
elif current_page == "bank_performance":
    render_bank_performance(app_df)
elif current_page == "competitor_performance":
    render_competitor_performance(app_df)
else:
    st.session_state["cx_current_page"] = "respondent_profile"
    st.rerun()