import streamlit as st
import pandas as pd
from helpers.loader import load_data

from components.experience_chart import (
    calculate_branch_performance,
    render_scorecards_2a,
    render_scatter_4_kuadran,
    render_controls_2b,          
    render_touchpoint_heatmap,
    render_friction_alert
)

# ---------------------------------------------------------------------------
# 1. LOAD DATA & MAPPING
# ---------------------------------------------------------------------------
df = load_data()

mapping_path = "data/Master Mapping.csv"
try:
    df_mapping = pd.read_csv(mapping_path)
except Exception:
    st.error(f"Mapping file not found at: {mapping_path}. Please ensure the file path and filename are correct.")
    st.stop()

# ---------------------------------------------------------------------------
# (1) JUDUL & (2) BUTTON TAB NAVIGATION
# ---------------------------------------------------------------------------
st.title("Branch & Touchpoint Experience")
st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

tabs = [
    "🏛️ Sub-Page 2A: Branch Performance & Loyalty Hub",
    "🔬 Sub-Page 2B: Deep-Dive Touchpoint & Head-to-Head Analysis"
]
selected_tab = st.radio("Navigasi Analisis:", tabs, label_visibility="collapsed")
st.markdown("<hr style='margin-top:5px; margin-bottom:20px; border-color:#e9e9e9;'>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# ROUTING SUB-PAGES
# ---------------------------------------------------------------------------
if selected_tab == tabs[0]:
    # --- SUB-PAGE 2A ---
    branch_summary = calculate_branch_performance(df, df_mapping)
    render_scorecards_2a(df, branch_summary)
    
    with st.container(key="p2_large_card_1"): 
        render_scatter_4_kuadran(branch_summary)

elif selected_tab == tabs[1]:
    # --- SUB-PAGE 2B (MODULAR CARDS) ---
    
    # 📦 KOTAK 1: KONTROL FILTER & PENCARIAN
    with st.container(key="p2_card_filter"):
        st.markdown("""
        <div style="font-size:18px;font-weight:800;color:#1D2433;margin-bottom:15px;">
        Head-to-Head Touchpoint Analysis
        </div>
        """, unsafe_allow_html=True)
        
        selected_branches, selected_category = render_controls_2b(df, df_mapping)
        
    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True) # Jarak antar kotak
    
    if selected_branches:
        
        # 📦 KOTAK 2: VISUALISASI HEATMAP
        with st.container(key="p2_card_heatmap"):
            render_touchpoint_heatmap(df, df_mapping, selected_branches, selected_category)
            
        st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True) # Jarak antar kotak
        
        # 📦 KOTAK 3: VISUALISASI BULLET CHART ALERT
        with st.container(key="p2_card_bullet"):
            render_friction_alert(df, selected_branches)
            
    else:
        st.info("💡 Type and select up to 3 branch offices from the search bar above to begin the analysis.")