import streamlit as st

# ──────────────────────────────────────────────────────────────────────────────
# 1. PAGE CONFIG (Harus selalu di baris paling atas)
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bank XYZ CX Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# 2. GLOBAL CSS & THEME SYSTEM
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />

<style>
/* ── Reset Global Font ── */
html, body, [class*="st-"] {
    font-family: 'Inter', -apple-system, sans-serif !important;
}

[data-testid="stSidebarCollapseButton"] { display: none !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

.block-container {
    padding-top: 1.8rem !important; padding-left: 2rem !important;
    padding-right: 2rem !important; padding-bottom: 2rem !important;
    max-width: 100% !important;
}

[data-testid="stAppViewContainer"] { background-color: #FFF5F8 !important; }
[data-testid="stHeader"] { background-color: transparent !important; }

[data-testid="stSidebar"] {
    background-color : #ffffff !important; border-right : none !important;
    min-width : 18rem !important; max-width : 18rem !important; 
}

[data-testid="collapsedControl"], [data-testid="stSidebarResizer"] {
    display: none !important; width: 0px !important;
}

[data-testid="stSidebarNav"] a {
    background-color: transparent !important; border-radius: 8px !important; margin-bottom: 4px !important; transition: all 0.2s ease !important;
}
[data-testid="stSidebarNav"] a span { color: #5E6677 !important; font-weight: 500 !important; }
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: #0067ff !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important; 
}
[data-testid="stSidebarNav"] a[aria-current="page"] span { color: #ffffff !important; font-weight: 800 !important; }

[data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stMultiSelect label, [data-testid="stSidebar"] .stRadio label {
    color: #1D2433 !important; font-size: 11px !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important;
}

/* ── 1. KPI CARDS SYSTEM ── */
.st-key-card_kpi_1, .st-key-card_kpi_2, .st-key-card_kpi_3, .st-key-card_kpi_4, .st-key-card_kpi_5 {
    background-color : #FFFFFF !important; border-radius : 20px !important; border : none !important;
    box-shadow : 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03) !important;
    padding : 1.5rem !important; transition : all 0.3s ease; height : 150px !important; display : flex !important; align-items : center !important; 
}

/* ── 2. CHART CONTAINERS SYSTEM ── */
.st-key-large_card_1, .st-key-large_card_2, 
.st-key-medium_card_1, .st-key-medium_card_2,
.st-key-geomap_card, .st-key-p2_large_card_1,
.st-key-p2_card_filter, .st-key-p2_card_heatmap, .st-key-p2_card_bullet,
.st-key-p1_card_bubble, .st-key-p1_card_persona,
.st-key-p3_card_bar, .st-key-p3_card_radar, .st-key-p3_card_filter, .st-key-p3_card_heatmap { /* <--- TAMBAHAN PAGE 3 */
    background-color : #FCFDFF !important; border-radius : 20px !important; border : none !important;
    box-shadow : 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03) !important;
    padding : 1.5rem !important; transition : all 0.3s ease;
}

/* ── KUNCI TINGGI CONTAINER KHUSUS PAGE 1 ── */
.st-key-p1_card_bubble, .st-key-p1_card_persona { height: 480px !important; }

/* ── 3. EFFECT HOVER ── */
.st-key-card_kpi_1:hover, .st-key-card_kpi_2:hover, .st-key-card_kpi_3:hover, .st-key-card_kpi_4:hover, .st-key-card_kpi_5:hover,
.st-key-large_card_1:hover, .st-key-large_card_2:hover, .st-key-medium_card_1:hover, .st-key-medium_card_2:hover,
.st-key-geomap_card:hover, .st-key-p2_large_card_1:hover,
.st-key-p2_card_filter:hover, .st-key-p2_card_heatmap:hover, .st-key-p2_card_bullet:hover,
.st-key-p1_card_bubble:hover, .st-key-p1_card_persona:hover,
.st-key-p3_card_bar:hover, .st-key-p3_card_radar:hover, .st-key-p3_card_filter:hover, .st-key-p3_card_heatmap:hover { /* <--- TAMBAHAN PAGE 3 */
    transform : translateY(-3px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04) !important;
}}

/* ── TYPOGRAPHY & OTHERS ── */
.kpi-title { font-size: 14px; font-weight: 600; color: #5E6677; letter-spacing: -0.2px; }
.kpi-value-large { font-size: 32px; font-weight: 800; color: #1D2433; line-height: 1; letter-spacing: -1px; }
.kpi-subtitle { font-size: 14px; font-weight: 500; color: #98A1B3; }
.js-plotly-plot .plotly .modebar { display: none !important; }

div.stRadio > div[role="radiogroup"] { flex-direction: row; gap: 10px; }
div.stRadio > div[role="radiogroup"] label { background-color: #f5f5f5; padding: 10px 20px; border-radius: 8px; border: 1px solid #cccccc; cursor: pointer; font-weight: 600; color: #4b4f5d !important; transition: all 0.2s ease; }
div.stRadio > div[role="radiogroup"] label[data-checked="true"] { background-color: #0067ff !important; border-color: #0067ff !important; }
div.stRadio > div[role="radiogroup"] label[data-checked="true"] p { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# 3. NAVIGATION PAGES DEFINITION
# ──────────────────────────────────────────────────────────────────────────────
pg = st.navigation([
    st.Page("pages/page1.py", title="Respondent Profile", icon="👥"),
    st.Page("pages/page2.py", title="Bank XYZ Performance", icon="🏦"),
    st.Page("pages/page3.py", title="Competitor Performance", icon="⚔️"),
])

pg.run()