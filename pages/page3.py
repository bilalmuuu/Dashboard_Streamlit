import streamlit as st
import pandas as pd
from helpers.loader import load_data

# Import fungsi visualisasi dari komponen yang baru saja kita buat
from components.competitor_chart import (
    render_competitor_kpis,
    render_competitor_macro_charts,
    render_competitor_heatmap
)

# ---------------------------------------------------------------------------
# 1. LOAD DATA & MAPPING
# ---------------------------------------------------------------------------
df = load_data()

# Load mapping khusus Page 3 yang baru saja Anda berikan
mapping_path_p3 = "data/Kompetitor Mapping.csv"
try:
    df_mapping_p3 = pd.read_csv(mapping_path_p3)
except Exception:
    st.error(f"File mapping Page 3 tidak ditemukan di: {mapping_path_p3}. Harap periksa nama filenya di folder 'data/'.")
    st.stop()

# ---------------------------------------------------------------------------
# 2. HEADER PAGE 3
# ---------------------------------------------------------------------------
st.title("Competitor Performance & Benchmarking")
st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 3. BARIS 1: KPI CARDS
# ---------------------------------------------------------------------------
# Menyimpan kembali dataframe yang sudah diparsing nama banknya
df_processed = render_competitor_kpis(df, df_mapping_p3)

st.markdown("<hr style='margin-top:20px; margin-bottom:20px; border-color:#e9e9e9;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 4. BARIS 2: MACRO CHARTS (BAR TOP 5 & RADAR CHART)
# ---------------------------------------------------------------------------
render_competitor_macro_charts(df_processed, df_mapping_p3)

st.markdown("<hr style='margin-top:20px; margin-bottom:20px; border-color:#e9e9e9;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 5. BARIS 3: MICRO HEATMAP DEEP-DIVE
# ---------------------------------------------------------------------------
render_competitor_heatmap(df_processed, df_mapping_p3)