"""
=============================================================================
COMPETITOR CHART COMPONENTS
Dashboard Visualization Module for Page 3
=============================================================================
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------------------
# 1. CORPORATE DESIGN SYSTEM & COLOR PALETTE (Diselaraskan dengan Page 2)
# ---------------------------------------------------------------------------
PRIMARY_100 = "#bb2649" 
PRIMARY_200 = "#f35d74"
PRIMARY_300 = "#ffc3d4"
ACCENT_100  = "#ffadad"
ACCENT_200  = "#ffd6a5"
TEXT_100    = "#4b4f5d"
TEXT_200    = "#6a738b"
BG_100      = "#ffffff" 
BG_200      = "#f5f5f5" 
BG_300      = "#cccccc"
POSITIVE_COLOR = "#2FBF71" 

TEXT_PRIMARY   = TEXT_100
TEXT_SECONDARY = TEXT_200
GRID_COLOR     = BG_200
CARD_BG        = BG_100 
BORDER_COLOR   = BG_300

# -------------------------------------------------------------------------
# FUNGSI 1: MENGHITUNG KPI (BARIS 1)
# -------------------------------------------------------------------------
def render_competitor_kpis(df, df_mapping):
    total_responden = len(df)
    
    # Menghitung Top Kompetitor Dana
    dana_col = "Bank Manakah Yang Merupakan Rekening Utama Untuk Bapak Ibu Menyimpan Dana"
    bank_dict = {
        1: "Bank BCA", 2: "Bank Mandiri", 3: "Bank BRI", 4: "Bank BNI", 
        5: "Bank Syariah Indonesia (BSI)", 6: "Bank Danamon", 7: "Bank Permata", 
        8: "Bank CIMB Niaga", 9: "Bank Mega", 10: "Bank OCBC NISP"
    }
    
    if dana_col in df.columns:
        df['Nama_Bank_Dana'] = df[dana_col].map(bank_dict).fillna("Bank Lainnya")
        df_kompetitor = df[df['Nama_Bank_Dana'] != "Bank XYZ"]
        total_bank_kompetitor = df_kompetitor['Nama_Bank_Dana'].nunique()
    else:
        df['Nama_Bank_Dana'] = "Tidak Diketahui"
        total_bank_kompetitor = 0

    # Menghitung Rata-rata CSI
    xyz_cols = df_mapping['Nama Kolom Bank XYZ'].dropna().tolist()
    komp_cols = df_mapping['Nama Kolom Kompetitor'].dropna().tolist()
    
    valid_xyz = [c for c in xyz_cols if c in df.columns]
    valid_komp = [c for c in komp_cols if c in df.columns]

    avg_csi_xyz = df[valid_xyz].mean().mean() if valid_xyz else 0
    avg_csi_komp = df[valid_komp].mean().mean() if valid_komp else 0

    # Menghitung NPS/Loyalty
    nps_xyz_col = "Ke Depannya Saya Pasti Akan Tetap Menggunakan Layanan Dari Bank Xyz" 
    nps_xyz = df[nps_xyz_col].mean() if nps_xyz_col in df.columns else 0
    nps_komp = avg_csi_komp * 2 if avg_csi_komp > 0 else 0 

    # UI HTML Untuk KPI CARD (Style persis seperti Page 2)
    def build_kpi_html(title, value, subtitle=""):
        return (
            '<div style="display: flex; align-items: center; gap: 10px; height: 90px;">'
                '<div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center;">'
                    f'<div class="kpi-title" style="margin-bottom: 2px; font-size: 13px; text-transform: uppercase; color:{TEXT_SECONDARY};">{title}</div>'
                    f'<div class="kpi-value-large" style="font-size: 28px; line-height: 1.2; font-weight:bold; color:{TEXT_PRIMARY};">{value}</div>'
                    f'<div class="kpi-subtitle" style="margin-top: 4px; font-size: 11px; font-weight: 600; color:{PRIMARY_100};">{subtitle}</div>'
                '</div>'
            '</div>'
        )

    kpi_cols = st.columns(4)
    
    with kpi_cols[0]:
        with st.container(key="kpi_comp_1"): 
            st.markdown(build_kpi_html("Total Responden", f"{total_responden:,}", "Keseluruhan Data"), unsafe_allow_html=True)
    with kpi_cols[1]:
        with st.container(key="kpi_comp_2"): 
            st.markdown(build_kpi_html("Bank Kompetitor", f"{total_bank_kompetitor}", "Bank Terdeteksi"), unsafe_allow_html=True)
    with kpi_cols[2]:
        with st.container(key="kpi_comp_3"): 
            st.markdown(build_kpi_html("Avg. CSI XYZ", f"{avg_csi_xyz:.2f}", f"vs Comp Avg: {avg_csi_komp:.2f}"), unsafe_allow_html=True)
    with kpi_cols[3]:
        with st.container(key="kpi_comp_4"): 
            st.markdown(build_kpi_html("Avg. Loyalty XYZ", f"{nps_xyz:.2f}", f"vs Comp Proxy: {nps_komp:.2f}"), unsafe_allow_html=True)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
    
    return df

# -------------------------------------------------------------------------
# FUNGSI 2: BAR CHART TOP 5 KOMPETITOR & RADAR CHART (BARIS 2)
# -------------------------------------------------------------------------
def render_competitor_macro_charts(df, df_mapping):
    col_bar, col_radar = st.columns([1, 1])

    # KOTAK KIRI: BAR CHART KOMPETITOR
    with col_bar:
        st.markdown(f"<div style='font-size:16px; font-weight:800; color:{TEXT_PRIMARY}; margin-bottom:15px;'>Top 5 Bank Kompetitor (Menyimpan Dana)</div>", unsafe_allow_html=True)
        
        top_5_banks = df['Nama_Bank_Dana'].value_counts().head(5).reset_index()
        top_5_banks.columns = ['Bank', 'Total']
        top_5_banks = top_5_banks.sort_values(by='Total', ascending=True)

        fig_bar = px.bar(
            top_5_banks, x='Total', y='Bank', orientation='h',
            text='Total', color_discrete_sequence=[PRIMARY_100]
        )
        
        fig_bar.update_traces(
            textposition='outside', textfont=dict(size=13, weight='bold', color=TEXT_PRIMARY),
            marker=dict(line=dict(width=0))
        )
        
        fig_bar.update_layout(
            height=300, margin=dict(l=0, r=30, t=10, b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False, title=""),
            yaxis=dict(title="", tickfont=dict(size=13, color=TEXT_PRIMARY, weight="bold"))
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    # KOTAK KANAN: RADAR CHART CSI
    with col_radar:
        st.markdown(f"<div style='font-size:16px; font-weight:800; color:{TEXT_PRIMARY}; margin-bottom:5px;'>Radar CSI: XYZ vs Average Competitor</div>", unsafe_allow_html=True)
        
        categories = df_mapping['Kategori Touchpoint'].unique()
        radar_data = []

        for cat in categories:
            cat_map = df_mapping[df_mapping['Kategori Touchpoint'] == cat]
            cols_xyz = [c for c in cat_map['Nama Kolom Bank XYZ'] if c in df.columns]
            cols_komp = [c for c in cat_map['Nama Kolom Kompetitor'] if c in df.columns]

            val_xyz = df[cols_xyz].mean().mean() if cols_xyz else 0
            val_komp = df[cols_komp].mean().mean() if cols_komp else 0
            
            short_cat = str(cat).replace(" Touchpoint", "").replace(" & ", "<br>& ")
            radar_data.append({"Category": short_cat, "XYZ": val_xyz, "Kompetitor": val_komp})

        df_radar = pd.DataFrame(radar_data)

        fig_radar = go.Figure()

        # Garis Kompetitor
        fig_radar.add_trace(go.Scatterpolar(
            r=df_radar['Kompetitor'].tolist() + [df_radar['Kompetitor'].tolist()[0]],
            theta=df_radar['Category'].tolist() + [df_radar['Category'].tolist()[0]],
            fill='toself', name='Avg Competitor', fillcolor='rgba(148, 163, 184, 0.2)',
            line=dict(color='#94a3b8', width=2, dash='dash')
        ))

        # Garis Bank XYZ
        fig_radar.add_trace(go.Scatterpolar(
            r=df_radar['XYZ'].tolist() + [df_radar['XYZ'].tolist()[0]],
            theta=df_radar['Category'].tolist() + [df_radar['Category'].tolist()[0]],
            fill='toself', name='Bank XYZ', fillcolor=f'{PRIMARY_100}33', # Hex dengan opacity
            line=dict(color=PRIMARY_100, width=3)
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(size=10, color=TEXT_SECONDARY)),
                angularaxis=dict(tickfont=dict(size=11, color=TEXT_PRIMARY))
            ),
            showlegend=True, height=320, margin=dict(l=40, r=40, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

# -------------------------------------------------------------------------
# FUNGSI 3: HEATMAP NATIVE HTML (BARIS 3)
# -------------------------------------------------------------------------
def render_competitor_heatmap(df, df_mapping):
    st.markdown(f"<div style='font-size:18px; font-weight:800; color:{TEXT_PRIMARY}; margin-bottom:15px;'>Head-to-Head Touchpoint Gap Analysis</div>", unsafe_allow_html=True)
    
    categories = df_mapping['Kategori Touchpoint'].unique().tolist()
    selected_category = st.selectbox("📂 Pilih Area Touchpoint yang Ingin Dibandingkan:", categories)

    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
    
    cat_map = df_mapping[df_mapping['Kategori Touchpoint'] == selected_category]
    
    # ---------------------------------------------------------------------
    # HEADER HEATMAP
    # ---------------------------------------------------------------------
    header_cols = st.columns([3, 1.5, 1.5, 1.5])
    with header_cols[0]: 
        st.markdown(f"<div style='font-weight:700; font-size:16px; color:#374151; padding-top:10px;'>Attribute / Touchpoint</div>", unsafe_allow_html=True)
    with header_cols[1]:
        st.markdown(f"<div style='text-align:center; font-weight:700; font-size:15px; color:#4b5563; padding-top:10px;'>Bank XYZ</div>", unsafe_allow_html=True)
    with header_cols[2]:
        st.markdown(f"<div style='text-align:center; font-weight:700; font-size:15px; color:#4b5563; padding-top:10px;'>Kompetitor</div>", unsafe_allow_html=True)
    with header_cols[3]:
        st.markdown(f"<div style='text-align:center; font-weight:700; font-size:15px; color:#4b5563; padding-top:10px;'>Gap (XYZ - Komp)</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # BODY HEATMAP
    # ---------------------------------------------------------------------
    for _, row in cat_map.iterrows():
        indikator = row['Indikator Core Touchpoint']
        col_xyz = row['Nama Kolom Bank XYZ']
        col_komp = row['Nama Kolom Kompetitor']
        
        val_xyz = df[col_xyz].apply(pd.to_numeric, errors='coerce').mean() if col_xyz in df.columns else np.nan
        val_komp = df[col_komp].apply(pd.to_numeric, errors='coerce').mean() if col_komp in df.columns else np.nan
        gap = val_xyz - val_komp if not pd.isna(val_xyz) and not pd.isna(val_komp) else np.nan
        
        cols = st.columns([3, 1.5, 1.5, 1.5])
        
        # Kolom 1: Nama Indikator
        with cols[0]:
            st.markdown(f"<div style='height:46px; display:flex; align-items:center; font-weight:600; color:#1f2937; font-size:13px;'>{indikator}</div>", unsafe_allow_html=True)

        # Kolom 2: Bank XYZ 
        intensity_xyz = min(max((val_xyz - 3.5) / 1.5, 0), 1) if not pd.isna(val_xyz) else 0
        green_xyz = int(120 + intensity_xyz * 80)
        bg_xyz = f"rgb(34,{green_xyz},84)" if not pd.isna(val_xyz) else "#cccccc"
        disp_xyz = f"{val_xyz:.2f}" if not pd.isna(val_xyz) else "N/A"
        
        with cols[1]:
            st.markdown(f"""
            <div style="background:{bg_xyz}; border-radius:14px; height:44px; display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:16px; margin-bottom:4px;">
            {disp_xyz}
            </div>
            """, unsafe_allow_html=True)

        # Kolom 3: Kompetitor 
        intensity_komp = min(max((val_komp - 3.5) / 1.5, 0), 1) if not pd.isna(val_komp) else 0
        green_komp = int(120 + intensity_komp * 80)
        bg_komp = f"rgb(34,{green_komp},84)" if not pd.isna(val_komp) else "#cccccc"
        disp_komp = f"{val_komp:.2f}" if not pd.isna(val_komp) else "N/A"

        with cols[2]:
            st.markdown(f"""
            <div style="background:{bg_komp}; border-radius:14px; height:44px; display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:16px; margin-bottom:4px;">
            {disp_komp}
            </div>
            """, unsafe_allow_html=True)

        # Kolom 4: GAP Analysis (Merah jika Kalah, Hijau jika Menang)
        if pd.isna(gap):
            bg_gap = "#cccccc"
            disp_gap = "N/A"
        else:
            bg_gap = POSITIVE_COLOR if gap > 0 else PRIMARY_100
            disp_gap = f"{gap:+.2f}"
            
        with cols[3]:
            st.markdown(f"""
            <div style="background:{bg_gap}; border-radius:14px; height:44px; display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:16px; margin-bottom:4px;">
            {disp_gap}
            </div>
            """, unsafe_allow_html=True)