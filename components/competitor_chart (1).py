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
# 1. CORPORATE DESIGN SYSTEM & COLOR PALETTE
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
    
    dana_col = "Bank Manakah Yang Merupakan Rekening Utama Untuk Bapak Ibu Menyimpan Dana"
    bank_dict = {
        1: "Bank BCA", 2: "Bank Mandiri", 3: "Bank BRI", 4: "Bank BNI", 
        5: "Bank Syariah Indonesia (BSI)", 6: "Bank Danamon", 7: "Bank Permata", 
        8: "Bank CIMB Niaga", 9: "Bank Mega", 10: "Bank OCBC NISP"
    }
    
    if dana_col in df.columns:
        df['Nama_Bank_Dana'] = df[dana_col].map(bank_dict).fillna("Other Banks")
        df_kompetitor = df[df['Nama_Bank_Dana'] != "Bank XYZ"]
        total_bank_kompetitor = df_kompetitor['Nama_Bank_Dana'].nunique()
    else:
        df['Nama_Bank_Dana'] = "Unknown"
        total_bank_kompetitor = 0

    xyz_cols = df_mapping['Nama Kolom Bank XYZ'].dropna().tolist()
    komp_cols = df_mapping['Nama Kolom Kompetitor'].dropna().tolist()
    
    valid_xyz = [c for c in xyz_cols if c in df.columns]
    valid_komp = [c for c in komp_cols if c in df.columns]

    avg_csi_xyz = df[valid_xyz].mean().mean() if valid_xyz else 0
    avg_csi_komp = df[valid_komp].mean().mean() if valid_komp else 0

    nps_xyz_col = "Ke Depannya Saya Pasti Akan Tetap Menggunakan Layanan Dari Bank Xyz" 
    nps_xyz = df[nps_xyz_col].mean() if nps_xyz_col in df.columns else 0
    nps_komp = avg_csi_komp * 2 if avg_csi_komp > 0 else 0 

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
            st.markdown(build_kpi_html("Total Respondents", f"{total_responden:,}", "Complete Dataset"), unsafe_allow_html=True)
    with kpi_cols[1]:
        with st.container(key="kpi_comp_2"): 
            st.markdown(build_kpi_html("Competitor Banks", f"{total_bank_kompetitor}", "Detected Banks"), unsafe_allow_html=True)
    with kpi_cols[2]:
        with st.container(key="kpi_comp_3"): 
            st.markdown(build_kpi_html("Avg. CSI XYZ", f"{avg_csi_xyz:.2f}", f"vs Comp Avg: {avg_csi_komp:.2f}"), unsafe_allow_html=True)
    with kpi_cols[3]:
        with st.container(key="kpi_comp_4"): 
            st.markdown(build_kpi_html("Avg. Loyalty XYZ", f"{nps_xyz:.2f}", f"vs Comp Proxy: {nps_komp:.2f}"), unsafe_allow_html=True)
    
    return df

# -------------------------------------------------------------------------
# FUNGSI 2: BAR CHART TOP 5 KOMPETITOR & RADAR CHART (BARIS 2)
# -------------------------------------------------------------------------
def render_competitor_macro_charts(df, df_mapping):
    col_bar, col_radar = st.columns([1, 1])

    # KOTAK KIRI: BAR CHART KOMPETITOR (Sudah dibungkus st.container)
    with col_bar:
        with st.container(key="p3_card_bar"):
            st.markdown(f"<div style='font-size:16px; font-weight:800; color:{TEXT_PRIMARY}; margin-bottom:15px;'>Top 5 Competitor Banks (Savings Account)</div>", unsafe_allow_html=True)
            
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
                height=341, margin=dict(l=0, r=30, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False, title=""),
                yaxis=dict(title="", tickfont=dict(size=13, color=TEXT_PRIMARY, weight="bold"))
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    # KOTAK KANAN: RADAR CHART CSI (Sudah dibungkus st.container)
    with col_radar:
        with st.container(key="p3_card_radar"):
            st.markdown(
                f"<div style='font-size:16px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:5px;'>"
                "Radar CSI: XYZ vs Average Competitor</div>",
                unsafe_allow_html=True,
            )

            categories = df_mapping['Kategori Touchpoint'].unique()
            radar_data = []

            for cat in categories:
                cat_map  = df_mapping[df_mapping['Kategori Touchpoint'] == cat]
                cols_xyz  = [c for c in cat_map['Nama Kolom Bank XYZ']   if c in df.columns]
                cols_komp = [c for c in cat_map['Nama Kolom Kompetitor'] if c in df.columns]

                val_xyz  = df[cols_xyz].mean().mean()  if cols_xyz  else 0
                val_komp = df[cols_komp].mean().mean() if cols_komp else 0

                # Label kategori ringkas (line-break setelah "&")
                short_cat = str(cat).replace(" Touchpoint", "").replace(" & ", "<br>& ")
                radar_data.append({"Category": short_cat, "XYZ": val_xyz, "Kompetitor": val_komp})

            df_radar = pd.DataFrame(radar_data)

            # ── Warna kompetitor: biru, berbeda keluarga dari merah XYZ ──────
            COMP_COLOR   = "#2563eb"   # biru  → kontras kuat vs PRIMARY_100 (merah)
            COMP_FILL    = "rgba(37, 99, 235, 0.08)"
            XYZ_FILL     = "rgba(187, 38, 73, 0.08)"

            # ── Auto-zoom: rentang berdasarkan nilai aktual ───────────────────
            # FIX: cap atas pakai 7.0 bukan 5.0 — data Likert skala 1–7
            all_vals = df_radar['XYZ'].tolist() + df_radar['Kompetitor'].tolist()
            non_zero = [v for v in all_vals if v > 0]
            if non_zero:
                r_min = max(0.0, round(min(non_zero) - 0.5, 1))
                r_max = min(7.0, round(max(non_zero) + 0.2, 1))
            else:
                r_min, r_max = 0.0, 7.0

            span  = r_max - r_min
            dtick = round(span / 4, 1)

            # ── Tutup polygon (titik pertama diulang di akhir) ────────────────
            r_komp = df_radar['Kompetitor'].tolist() + [df_radar['Kompetitor'].iloc[0]]
            r_xyz  = df_radar['XYZ'].tolist()        + [df_radar['XYZ'].iloc[0]]
            theta  = df_radar['Category'].tolist()   + [df_radar['Category'].iloc[0]]

            # ── Label nilai (titik penutup tidak diberi label) ────────────────
            lbl_komp = [f"{v:.2f}" for v in df_radar['Kompetitor']] + [""]
            lbl_xyz  = [f"{v:.2f}" for v in df_radar['XYZ']]        + [""]

            fig_radar = go.Figure()

            # Trace 1 — Avg Competitor: biru, dashed, diamond marker, fill tipis
            fig_radar.add_trace(go.Scatterpolar(
                r=r_komp, theta=theta,
                name="Avg Competitor",
                fill="toself", fillcolor=COMP_FILL,
                line=dict(color=COMP_COLOR, width=2.5, dash="dash"),
                mode="lines+markers+text",
                text=lbl_komp, textposition="top center",
                textfont=dict(size=10, color=COMP_COLOR, weight="bold"),
                marker=dict(
                    size=9, symbol="diamond", color=COMP_COLOR,
                    line=dict(width=2, color="white"),
                ),
            ))

            # Trace 2 — Bank XYZ: merah, solid, circle marker, fill tipis
            fig_radar.add_trace(go.Scatterpolar(
                r=r_xyz, theta=theta,
                name="Bank XYZ",
                fill="toself", fillcolor=XYZ_FILL,
                line=dict(color=PRIMARY_100, width=3),
                mode="lines+markers+text",
                text=lbl_xyz, textposition="top center",
                textfont=dict(size=10, color=PRIMARY_100, weight="bold"),
                marker=dict(
                    size=10, symbol="circle", color=PRIMARY_100,
                    line=dict(width=2.5, color="white"),
                ),
            ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[r_min, r_max],
                        dtick=dtick,
                        tickfont=dict(size=9, color=TEXT_SECONDARY),
                        gridcolor="rgba(0,0,0,0.08)",
                        linecolor="rgba(0,0,0,0.12)",
                        tickcolor="rgba(0,0,0,0.12)",
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=11, color=TEXT_PRIMARY, weight="bold"),
                        gridcolor="rgba(0,0,0,0.08)",
                        linecolor="rgba(0,0,0,0.12)",
                    ),
                    bgcolor="rgba(0,0,0,0)",
                ),
                showlegend=True,
                height=350,
                margin=dict(l=40, r=40, t=50, b=0),
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.25,
                    xanchor="center", x=0.5,
                    font=dict(size=12, color=TEXT_PRIMARY),
                    bgcolor="rgba(0,0,0,0)",
                    itemsizing="constant",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

# -------------------------------------------------------------------------
# FUNGSI 3: HEATMAP NATIVE HTML (BARIS 3)
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# FUNGSI 3: HEATMAP NATIVE HTML (BARIS 3) - REVISI UI/UX TOOLTIP
# -------------------------------------------------------------------------
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
# 1. CORPORATE DESIGN SYSTEM & COLOR PALETTE
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
    
    dana_col = "Bank Manakah Yang Merupakan Rekening Utama Untuk Bapak Ibu Menyimpan Dana"
    bank_dict = {
        1: "Bank BCA", 2: "Bank Mandiri", 3: "Bank BRI", 4: "Bank BNI", 
        5: "Bank Syariah Indonesia (BSI)", 6: "Bank Danamon", 7: "Bank Permata", 
        8: "Bank CIMB Niaga", 9: "Bank Mega", 10: "Bank OCBC NISP"
    }
    
    if dana_col in df.columns:
        df['Nama_Bank_Dana'] = df[dana_col].map(bank_dict).fillna("Other Banks")
        df_kompetitor = df[df['Nama_Bank_Dana'] != "Bank XYZ"]
        total_bank_kompetitor = df_kompetitor['Nama_Bank_Dana'].nunique()
    else:
        df['Nama_Bank_Dana'] = "Unknown"
        total_bank_kompetitor = 0

    xyz_cols = df_mapping['Nama Kolom Bank XYZ'].dropna().tolist()
    komp_cols = df_mapping['Nama Kolom Kompetitor'].dropna().tolist()
    
    valid_xyz = [c for c in xyz_cols if c in df.columns]
    valid_komp = [c for c in komp_cols if c in df.columns]

    avg_csi_xyz = df[valid_xyz].mean().mean() if valid_xyz else 0
    avg_csi_komp = df[valid_komp].mean().mean() if valid_komp else 0

    nps_xyz_col = "Ke Depannya Saya Pasti Akan Tetap Menggunakan Layanan Dari Bank Xyz" 
    nps_xyz = df[nps_xyz_col].mean() if nps_xyz_col in df.columns else 0
    nps_komp = avg_csi_komp * 2 if avg_csi_komp > 0 else 0 

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
            st.markdown(build_kpi_html("Total Respondents", f"{total_responden:,}", "Complete Dataset"), unsafe_allow_html=True)
    with kpi_cols[1]:
        with st.container(key="kpi_comp_2"): 
            st.markdown(build_kpi_html("Competitor Banks", f"{total_bank_kompetitor}", "Detected Banks"), unsafe_allow_html=True)
    with kpi_cols[2]:
        with st.container(key="kpi_comp_3"): 
            st.markdown(build_kpi_html("Avg. CSI XYZ", f"{avg_csi_xyz:.2f}", f"vs Comp Avg: {avg_csi_komp:.2f}"), unsafe_allow_html=True)
    with kpi_cols[3]:
        with st.container(key="kpi_comp_4"): 
            st.markdown(build_kpi_html("Avg. Loyalty XYZ", f"{nps_xyz:.2f}", f"vs Comp Proxy: {nps_komp:.2f}"), unsafe_allow_html=True)
    
    return df

# -------------------------------------------------------------------------
# FUNGSI 2: BAR CHART TOP 5 KOMPETITOR & RADAR CHART (BARIS 2)
# -------------------------------------------------------------------------
def render_competitor_macro_charts(df, df_mapping):
    col_bar, col_radar = st.columns([1, 1])

    # KOTAK KIRI: BAR CHART KOMPETITOR (Sudah dibungkus st.container)
    with col_bar:
        with st.container(key="p3_card_bar"):
            st.markdown(f"<div style='font-size:16px; font-weight:800; color:{TEXT_PRIMARY}; margin-bottom:15px;'>Top 5 Competitor Banks (Savings Account)</div>", unsafe_allow_html=True)
            
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
                height=341, margin=dict(l=0, r=30, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False, title=""),
                yaxis=dict(title="", tickfont=dict(size=13, color=TEXT_PRIMARY, weight="bold"))
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    # KOTAK KANAN: RADAR CHART CSI (Sudah dibungkus st.container)
    with col_radar:
        with st.container(key="p3_card_radar"):
            st.markdown(
                f"<div style='font-size:16px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:5px;'>"
                "Radar CSI: XYZ vs Average Competitor</div>",
                unsafe_allow_html=True,
            )

            categories = df_mapping['Kategori Touchpoint'].unique()
            radar_data = []

            for cat in categories:
                cat_map  = df_mapping[df_mapping['Kategori Touchpoint'] == cat]
                cols_xyz  = [c for c in cat_map['Nama Kolom Bank XYZ']   if c in df.columns]
                cols_komp = [c for c in cat_map['Nama Kolom Kompetitor'] if c in df.columns]

                val_xyz  = df[cols_xyz].mean().mean()  if cols_xyz  else 0
                val_komp = df[cols_komp].mean().mean() if cols_komp else 0

                # Label kategori ringkas (line-break setelah "&")
                short_cat = str(cat).replace(" Touchpoint", "").replace(" & ", "<br>& ")
                radar_data.append({"Category": short_cat, "XYZ": val_xyz, "Kompetitor": val_komp})

            df_radar = pd.DataFrame(radar_data)

            # ── Warna kompetitor: biru, berbeda keluarga dari merah XYZ ──────
            COMP_COLOR   = "#2563eb"   # biru  → kontras kuat vs PRIMARY_100 (merah)
            COMP_FILL    = "rgba(37, 99, 235, 0.08)"
            XYZ_FILL     = "rgba(187, 38, 73, 0.08)"

            # ── Auto-zoom: rentang berdasarkan nilai aktual ───────────────────
            # FIX: cap atas pakai 7.0 bukan 5.0 — data Likert skala 1–7
            all_vals = df_radar['XYZ'].tolist() + df_radar['Kompetitor'].tolist()
            non_zero = [v for v in all_vals if v > 0]
            if non_zero:
                r_min = max(0.0, round(min(non_zero) - 0.5, 1))
                r_max = min(7.0, round(max(non_zero) + 0.2, 1))
            else:
                r_min, r_max = 0.0, 7.0

            span  = r_max - r_min
            dtick = round(span / 4, 1)

            # ── Tutup polygon (titik pertama diulang di akhir) ────────────────
            r_komp = df_radar['Kompetitor'].tolist() + [df_radar['Kompetitor'].iloc[0]]
            r_xyz  = df_radar['XYZ'].tolist()        + [df_radar['XYZ'].iloc[0]]
            theta  = df_radar['Category'].tolist()   + [df_radar['Category'].iloc[0]]

            # ── Label nilai (titik penutup tidak diberi label) ────────────────
            lbl_komp = [f"{v:.2f}" for v in df_radar['Kompetitor']] + [""]
            lbl_xyz  = [f"{v:.2f}" for v in df_radar['XYZ']]        + [""]

            fig_radar = go.Figure()

            # Trace 1 — Avg Competitor: biru, dashed, diamond marker, fill tipis
            fig_radar.add_trace(go.Scatterpolar(
                r=r_komp, theta=theta,
                name="Avg Competitor",
                fill="toself", fillcolor=COMP_FILL,
                line=dict(color=COMP_COLOR, width=2.5, dash="dash"),
                mode="lines+markers+text",
                text=lbl_komp, textposition="top center",
                textfont=dict(size=10, color=COMP_COLOR, weight="bold"),
                marker=dict(
                    size=9, symbol="diamond", color=COMP_COLOR,
                    line=dict(width=2, color="white"),
                ),
            ))

            # Trace 2 — Bank XYZ: merah, solid, circle marker, fill tipis
            fig_radar.add_trace(go.Scatterpolar(
                r=r_xyz, theta=theta,
                name="Bank XYZ",
                fill="toself", fillcolor=XYZ_FILL,
                line=dict(color=PRIMARY_100, width=3),
                mode="lines+markers+text",
                text=lbl_xyz, textposition="top center",
                textfont=dict(size=10, color=PRIMARY_100, weight="bold"),
                marker=dict(
                    size=10, symbol="circle", color=PRIMARY_100,
                    line=dict(width=2.5, color="white"),
                ),
            ))

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[r_min, r_max],
                        dtick=dtick,
                        tickfont=dict(size=9, color=TEXT_SECONDARY),
                        gridcolor="rgba(0,0,0,0.08)",
                        linecolor="rgba(0,0,0,0.12)",
                        tickcolor="rgba(0,0,0,0.12)",
                    ),
                    angularaxis=dict(
                        tickfont=dict(size=11, color=TEXT_PRIMARY, weight="bold"),
                        gridcolor="rgba(0,0,0,0.08)",
                        linecolor="rgba(0,0,0,0.12)",
                    ),
                    bgcolor="rgba(0,0,0,0)",
                ),
                showlegend=True,
                height=350,
                margin=dict(l=40, r=40, t=50, b=0),
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.25,
                    xanchor="center", x=0.5,
                    font=dict(size=12, color=TEXT_PRIMARY),
                    bgcolor="rgba(0,0,0,0)",
                    itemsizing="constant",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

# -------------------------------------------------------------------------
# FUNGSI 3: HEATMAP NATIVE HTML (BARIS 3) - REVISI UI/UX TOOLTIP
# -------------------------------------------------------------------------
def render_competitor_heatmap(df, df_mapping):

    # ── CSS GLOBAL: styling tooltip (Diadaptasi dari konsep Hovertemplate) ──
    st.markdown(
        '<style>'
        '.ht-cell{position:relative;cursor:help;overflow:visible;}'
        '.ht-tip{'
        'visibility:hidden;opacity:0;'
        'position:absolute;bottom:calc(100% + 8px);left:50%;'
        'transform:translateX(-50%);'
        'background:#1D2433;color:#ffffff;'
        'padding:10px 14px;border-radius:8px;'
        'font-size:12px;font-family:Inter,sans-serif;'
        'line-height:1.6;white-space:nowrap;'
        'z-index:99999;'
        'box-shadow:0 6px 20px rgba(0,0,0,0.3);'
        'pointer-events:none;'
        'transition:opacity 0.15s ease,visibility 0.15s ease;}'
        '.ht-tip::after{'
        'content:"";position:absolute;top:100%;left:50%;'
        'transform:translateX(-50%);'
        'border:5px solid transparent;border-top-color:#1D2433;}'
        '.ht-cell:hover .ht-tip{visibility:visible;opacity:1;}'
        '</style>',
        unsafe_allow_html=True,
    )

    # ── Container filter kategori ──
    with st.container(key="p3_card_filter"):
        st.markdown(
            f'<div style="font-size:18px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:15px;">'
            'Head-to-Head Touchpoint Gap Analysis</div>',
            unsafe_allow_html=True,
        )
        categories = df_mapping["Kategori Touchpoint"].dropna().unique().tolist()
        selected_category = st.selectbox(
            "📂 Select Touchpoint Area to Compare:", categories
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── Container heatmap ──
    with st.container(key="p3_card_heatmap"):
        cat_map = df_mapping[df_mapping["Kategori Touchpoint"] == selected_category]

        # ── KONSISTENSI EXPERIENCE CHART: Header kolom rasio [3, 1.5, 1.5] ──
        header_cols = st.columns([3, 1.5, 1.5])
        with header_cols[0]:
            st.markdown(
                '<div style="font-weight:700; font-size:18px; color:#374151; padding-top:10px;">'
                'Attribute / Touchpoint</div>',
                unsafe_allow_html=True,
            )
        with header_cols[1]:
            st.markdown(
                '<div style="text-align:center; font-weight:700; font-size:16px; color:#4b5563; padding-top:10px;">'
                'Bank XYZ</div>',
                unsafe_allow_html=True,
            )
        with header_cols[2]:
            st.markdown(
                '<div style="text-align:center; font-weight:700; font-size:16px; color:#4b5563; padding-top:10px;">'
                'Competitor</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # ── KONSISTENSI EXPERIENCE CHART: Style Base Kotak (Score Container) ──
        CELL_STYLE = (
            "border-radius:14px; height:44px; display:flex; "
            "align-items:center; justify-content:center; "
            "font-weight:700; font-size:16px; margin-bottom:4px; transition:0.2s;"
        )

        # Baris data
        for _, row in cat_map.iterrows():
            indikator = row["Indikator Core Touchpoint"]
            col_xyz   = row["Nama Kolom Bank XYZ"]
            col_komp  = row["Nama Kolom Kompetitor"]

            val_xyz = (
                df[col_xyz].apply(pd.to_numeric, errors="coerce").mean()
                if col_xyz in df.columns else np.nan
            )
            val_komp = (
                df[col_komp].apply(pd.to_numeric, errors="coerce").mean()
                if col_komp in df.columns else np.nan
            )
            gap = (
                val_xyz - val_komp
                if not pd.isna(val_xyz) and not pd.isna(val_komp)
                else np.nan
            )

            # ── LOGIKA WARNA KOTAK (Menang vs Kalah) ──
            if pd.isna(gap):
                xyz_bg,  xyz_txt  = "#f8fafc", "#94a3b8"
                komp_bg, komp_txt = "#f8fafc", "#94a3b8"
                gap_text          = "N/A"
            elif gap > 0:
                xyz_bg,  xyz_txt  = POSITIVE_COLOR, "#ffffff"
                komp_bg, komp_txt = "#f1f5f9", "#64748b"
                gap_text          = f"+{gap:.2f}"
            elif gap < 0:
                xyz_bg,  xyz_txt  = "#f1f5f9", "#64748b"
                komp_bg, komp_txt = POSITIVE_COLOR, "#ffffff"
                gap_text          = f"{gap:.2f}"
            else:
                xyz_bg,  xyz_txt  = "#e2e8f0", "#475569"
                komp_bg, komp_txt = "#e2e8f0", "#475569"
                gap_text          = "0.00"

            disp_xyz  = f"{val_xyz:.2f}"  if not pd.isna(val_xyz)  else "N/A"
            disp_komp = f"{val_komp:.2f}" if not pd.isna(val_komp) else "N/A"

            # ── ISI TOOLTIP HOVER ──
            if pd.isna(gap):
                tip_xyz = "<b>🏦 Bank XYZ</b><br>Incomplete Data"
                tip_komp = "<b>🏛️ Avg Kompetitor</b><br>Incomplete Data"
            else:
                if gap > 0:
                    tt_xyz = f"🏆 Leading by {abs(gap):.2f} points over competitors"
                    tt_komp = f"Trailing by {abs(gap):.2f} points behind XYZ"
                elif gap < 0:
                    tt_xyz = f"Trailing by {abs(gap):.2f} points behind competitors"
                    tt_komp = f"🏆 Leading by {abs(gap):.2f} points over XYZ"
                else:
                    tt_xyz = "Equal Score"
                    tt_komp = "Equal Score"
                    
                tip_xyz = f"<b>🏦 Bank XYZ</b><br>Skor: {disp_xyz}<br>{tt_xyz}"
                tip_komp = f"<b>🏛️ Avg Competitor</b><br>Skor: {disp_komp}<br>{tt_komp}"

            # ── KONSISTENSI EXPERIENCE CHART: Rasio Baris [3, 1.5, 1.5] ──
            cols = st.columns([3, 1.5, 1.5])

            # Kolom 1: Nama Touchpoint
            with cols[0]:
                st.markdown(
                    f'<div style="height:46px; display:flex; align-items:center; '
                    f'font-weight:600; color:#1f2937; font-size:13px;">{indikator}</div>',
                    unsafe_allow_html=True,
                )
            
            # Kolom 2: Kotak Bank XYZ + Tooltip
            with cols[1]:
                st.markdown(
                    f'<div class="ht-cell">'
                    f'<div class="ht-tip">{tip_xyz}</div>'
                    f'<div style="background:{xyz_bg}; color:{xyz_txt}; {CELL_STYLE}">{disp_xyz}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            
            # Kolom 3: Kotak Kompetitor + Tooltip
            with cols[2]:
                st.markdown(
                    f'<div class="ht-cell">'
                    f'<div class="ht-tip">{tip_komp}</div>'
                    f'<div style="background:{komp_bg}; color:{komp_txt}; {CELL_STYLE}">{disp_komp}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )