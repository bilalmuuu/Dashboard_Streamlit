"""
=============================================================================
EXPERIENCE & TOUCHPOINT COMPONENTS
Dashboard Visualization Module for Page 2
=============================================================================
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import base64
from pathlib import Path
ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"


def _asset_data_uri(filename: str) -> str:
    asset_path = ASSET_DIR / filename
    if not asset_path.exists():
        return ""
    encoded = base64.b64encode(asset_path.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def _kpi_asset(filename: str, alt_text: str) -> str:
    uri = _asset_data_uri(filename)
    if not uri:
        return ""
    return (
        f'<img src="{uri}" alt="{alt_text}" '
        'style="width:72px;height:72px;object-fit:contain;display:block;" />'
    )

# ---------------------------------------------------------------------------
# 1. CORPORATE DESIGN SYSTEM & COLOR PALETTE
# ---------------------------------------------------------------------------
PRIMARY_100 = "#bb2649"
PRIMARY_200 = "#f35d74"
PRIMARY_300 = "#ffc3d4"
ACCENT_100 = "#ffadad"
ACCENT_200 = "#ffd6a5"
TEXT_100 = "#4b4f5d"
TEXT_200 = "#6a738b"
BG_100 = "#ffffff"
BG_200 = "#f5f5f5"
BG_300 = "#cccccc"
POSITIVE_COLOR = "#2FBF71"
NEGATIVE_COLOR = "#bb2649"

TEXT_PRIMARY = TEXT_100
TEXT_SECONDARY = TEXT_200
GRID_COLOR = BG_200
CARD_BG = BG_100
BORDER_COLOR = BG_300

NPS_COL = "Nps Bank Xyz"
BRANCH_COL = "Nama Kantor Cabang"

# ---------------------------------------------------------------------------
# 2. DATA PROCESSING: CSI & NPS CALCULATION
# ---------------------------------------------------------------------------
@st.cache_data
def calculate_branch_performance(df, df_mapping):
    harapan_cols = df_mapping['Nama Kolom KPI Harapan / Deskripsi'].tolist()
    realita_cols = df_mapping['Nama Kolom KPI Bank XYZ / Fisik'].tolist()

    valid_harapan = []
    valid_realita = []
    for h_col, r_col in zip(harapan_cols, realita_cols):
        if h_col in df.columns and r_col in df.columns:
            valid_harapan.append(h_col)
            valid_realita.append(r_col)

    if not valid_harapan or not valid_realita:
        return pd.DataFrame()

    national_harapan_mean = df[valid_harapan].apply(pd.to_numeric, errors='coerce').mean()
    total_harapan = national_harapan_mean.sum()
    weight_factors = national_harapan_mean / total_harapan

    branch_stats = []
    grouped = df.groupby(BRANCH_COL)

    for branch, group in grouped:
        realita_mean = group[valid_realita].apply(pd.to_numeric, errors='coerce').mean()
        realita_mean.index = valid_harapan
        csi_score = (realita_mean * weight_factors).sum() * 20

        nps_score = 0
        if NPS_COL in group.columns:
            nps_data = pd.to_numeric(group[NPS_COL], errors='coerce').dropna()
            if len(nps_data) > 0:
                promoters = len(nps_data[nps_data >= 9]) / len(nps_data)
                detractors = len(nps_data[nps_data <= 6]) / len(nps_data)
                nps_score = (promoters - detractors) * 100

        branch_stats.append({
            "Branch": branch,
            "Total_Respondents": len(group),
            "CSI": csi_score,
            "NPS": nps_score
        })

    return pd.DataFrame(branch_stats)

# ---------------------------------------------------------------------------
# 3. SUB-PAGE 2A COMPONENTS
# ---------------------------------------------------------------------------
def render_scorecards_2a(df, branch_summary):
    if branch_summary.empty: return

    kpi_cols = st.columns(4, gap="medium")
    total_resp = len(df)
    total_branch = branch_summary['Branch'].nunique()
    avg_csi = branch_summary['CSI'].mean()
    avg_nps = branch_summary['NPS'].mean()

    def build_kpi_html(icon_html, title, value, subtitle=""):
        return (
            '<div style="display:flex;align-items:center;gap:16px;min-height:116px;width:100%;padding:6px 2px;">'
                '<div style="width:76px;height:76px;flex-shrink:0;'
                'display:flex;align-items:center;justify-content:center;">'
                    f'{icon_html}'
                '</div>'
                '<div style="display:flex;flex-direction:column;align-items:flex-start;'
                'justify-content:center;min-width:0;">'
                    f'<div class="kpi-title" style="margin-bottom:5px;font-size:12px;'
                    f'text-transform:uppercase;color:{TEXT_SECONDARY};white-space:normal;'
                    f'line-height:1.25;overflow-wrap:anywhere;">{title}</div>'
                    f'<div class="kpi-value-large" style="font-size:27px;line-height:1.05;'
                    f'font-weight:800;color:{TEXT_PRIMARY};white-space:nowrap;">{value}</div>'
                    f'<div class="kpi-subtitle" style="margin-top:6px;font-size:11px;'
                    f'font-weight:600;color:{PRIMARY_100};white-space:normal;line-height:1.3;'
                    f'overflow-wrap:anywhere;">{subtitle}</div>'
                '</div>'
            '</div>'
        )

    with kpi_cols[0]:
        with st.container(key="card_kpi_1"):
            st.markdown(
                build_kpi_html(
                    _kpi_asset("bank.png", "Total respondents"),
                    "Total Respondents",
                    f"{total_resp:,}",
                    "All survey records",
                ),
                unsafe_allow_html=True,
            )

    with kpi_cols[1]:
        with st.container(key="card_kpi_2"):
            st.markdown(
                build_kpi_html(
                    _kpi_asset("cabang.png", "Total branches"),
                    "Total Branches",
                    f"{total_branch:,}",
                    "Active branches",
                ),
                unsafe_allow_html=True,
            )

    with kpi_cols[2]:
        with st.container(key="card_kpi_3"):
            st.markdown(
                build_kpi_html(
                    _kpi_asset("csi.png", "Customer satisfaction index"),
                    "National Avg. CSI",
                    f"{avg_csi:.1f}%",
                    "IPA weighting",
                ),
                unsafe_allow_html=True,
            )

    with kpi_cols[3]:
        with st.container(key="card_kpi_4"):
            st.markdown(
                build_kpi_html(
                    _kpi_asset("nps.png", "Net promoter score"),
                    "National Avg. NPS",
                    f"{avg_nps:.1f}",
                    "Net Promoter Score",
                ),
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

def render_scatter_4_kuadran(branch_summary):
    if branch_summary.empty: return

    st.markdown(f"""
    <div style="font-size:16px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:4px;">Branch Competitiveness Mapping (CSI vs NPS)</div>
    <div style="font-size:13px;color:{TEXT_SECONDARY};margin-bottom:18px;">Four-quadrant comparison of branch satisfaction and advocacy performance.</div>
    """, unsafe_allow_html=True)

    med_csi = branch_summary['CSI'].median()
    med_nps = branch_summary['NPS'].median()

    colors = []
    for _, row in branch_summary.iterrows():
        if row['CSI'] >= med_csi and row['NPS'] >= med_nps:
            colors.append(POSITIVE_COLOR)
        elif row['CSI'] >= med_csi and row['NPS'] < med_nps:
            colors.append(ACCENT_200)
        elif row['CSI'] < med_csi and row['NPS'] >= med_nps:
            colors.append(BG_300)
        else:
            colors.append(PRIMARY_100)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=branch_summary['CSI'], y=branch_summary['NPS'], mode='markers', text=branch_summary['Branch'],
        marker=dict(size=12, color=colors, line=dict(width=1, color=BG_100), opacity=0.8),
        hovertemplate="<b>%{text}</b><br>CSI: %{x:.1f}<br>NPS: %{y:.1f}<extra></extra>"
    ))

    fig.add_hline(y=med_nps, line_dash="dash", line_color=TEXT_200, opacity=0.5)
    fig.add_vline(x=med_csi, line_dash="dash", line_color=TEXT_200, opacity=0.5)

    fig.add_annotation(x=branch_summary['CSI'].max(), y=branch_summary['NPS'].max(), text="STARS", showarrow=False, font=dict(color=POSITIVE_COLOR, size=14, weight="bold"), opacity=0.3)
    fig.add_annotation(x=branch_summary['CSI'].max(), y=branch_summary['NPS'].min(), text="TRANSACTIONAL ONLY", showarrow=False, font=dict(color=ACCENT_200, size=14, weight="bold"), opacity=0.3)
    fig.add_annotation(x=branch_summary['CSI'].min(), y=branch_summary['NPS'].min(), text="UNDERPERFORMING", showarrow=False, font=dict(color=PRIMARY_100, size=14, weight="bold"), opacity=0.3)

    fig.update_layout(height=500, margin=dict(l=0, r=0, t=20, b=0), xaxis_title="Customer Satisfaction Index (CSI)", yaxis_title="Net Promoter Score (NPS)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=True, gridcolor=GRID_COLOR), yaxis=dict(showgrid=True, gridcolor=GRID_COLOR))
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

# ---------------------------------------------------------------------------
# 4. SUB-PAGE 2B COMPONENTS (HEATMAP NATIVE, ALERT)
# ---------------------------------------------------------------------------
def render_controls_2b(df, df_mapping):
    excluded_keywords = ["9. Durasi", "10. Kondisi", "11. Varian"]
    categories = [
        cat for cat in df_mapping['Kategori'].unique()
        if not any(keyword in cat for keyword in excluded_keywords)
    ]

    col_cat, col_search = st.columns([1, 2], gap="large")
    with col_cat:
        # Remove the optional suffix from the displayed category label only.
        selected_category = st.selectbox(
            "📂 Touchpoint Category",
            categories,
            format_func=lambda x: x.replace(" (Tambahan)", "").strip()
        )
    with col_search:
        branches = df[BRANCH_COL].dropna().unique().tolist()
        selected_branches = st.multiselect("🔍 Compare Branches (maximum 3)", branches, max_selections=3)

    return selected_branches, selected_category

def render_touchpoint_heatmap(df, df_mapping, selected_branches, selected_category):
    if len(selected_branches) == 0:
        return

    cat_mapping = df_mapping[df_mapping["Kategori"] == selected_category]
    touchpoints = cat_mapping["Nama Kolom KPI Bank XYZ / Fisik"].tolist()
    labels = cat_mapping["Nama Kolom KPI Harapan / Deskripsi"].tolist()

    valid_pairs = [(tp, lbl) for tp, lbl in zip(touchpoints, labels) if tp in df.columns]

    if len(valid_pairs) == 0:
        st.warning("No touchpoints were found for the selected category.")
        return

    matrix = []
    for tp, label in valid_pairs:
        row = {"Touchpoint": label}
        for branch in selected_branches:
            score = df[df[BRANCH_COL] == branch][tp].apply(pd.to_numeric, errors='coerce').mean()
            row[branch] = round(score, 2)
        matrix.append(row)

    heatmap_df = pd.DataFrame(matrix)

    header_cols = st.columns([3] + [1.5] * len(selected_branches))
    with header_cols[0]:
        st.markdown("""<div style="font-weight:700; font-size:18px; color:#1D2433; padding-top:10px;">Attribute</div>""", unsafe_allow_html=True)

    for i, branch in enumerate(selected_branches):
        with header_cols[i+1]:
            st.markdown(f"""<div style="text-align:center; font-weight:700; font-size:16px; color:#5E6677; padding-top:10px;">{branch}</div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    for _, row in heatmap_df.iterrows():
        cols = st.columns([3] + [1.5] * len(selected_branches))
        with cols[0]:
            st.markdown(f"""<div style="height:46px; display:flex; align-items:center; font-weight:600; color:#1D2433; font-size:13px;">{row['Touchpoint']}</div>""", unsafe_allow_html=True)

        for i, branch in enumerate(selected_branches):
            score = row[branch]

            intensity = min(max((score - 4.5) / 1.5, 0), 1) if not pd.isna(score) else 0
            green = int(120 + intensity * 80)
            bg = f"rgb(34,{green},84)" if not pd.isna(score) else "#cccccc"
            disp_score = f"{score:.2f}" if not pd.isna(score) else "N/A"

            with cols[i+1]:
                st.markdown(f"""
                <div style="background:{bg}; border-radius:14px; height:44px; display:flex; align-items:center; justify-content:center; color:white; font-weight:700; font-size:16px; margin-bottom:4px;">
                {disp_score}
                </div>
                """, unsafe_allow_html=True)

def render_friction_alert(df, selected_branches):
    # Title and reading guide
    st.markdown(f"""
    <div style="font-size:18px;font-weight:800;color:{TEXT_PRIMARY};margin-top:20px;margin-bottom:4px;">
        Queue Friction Time (Real Emotion Analysis)
    </div>
    <div style="font-size:13px;color:{TEXT_SECONDARY};margin-bottom:20px;">
        Compares <b>actual waiting time</b> against the <b>customer tolerance threshold</b>.<br>
        The <span style="background-color:#EEF8F2; color:#2FBF71; padding:2px 6px; border-radius:4px; font-weight:600;">green zone</span> is within tolerance, while the <span style="background-color:#FFF0F4; color:#BB2649; padding:2px 6px; border-radius:4px; font-weight:600;">red zone</span> indicates rising customer frustration.
    </div>
    """, unsafe_allow_html=True)

    t_wait = "Berapa Lama Waktu Tunggu Antri Teller Anda Untuk Kunjungan Hari Ini Menit"
    t_tol = "Berapa Lamakah Waktu Tunggu Antri Teller Yang Anda Bisa Terima Toleransi Menit"
    cs_wait = "Berapa Lama Waktu Tunggu Antri Cs Anda Untuk Kunjungan Hari Ini Menit"
    cs_tol = "Berapa Lamakah Waktu Tunggu Antri Cs Yang Anda Bisa Terima Toleransi Menit"

    cols = [t_wait, t_tol, cs_wait, cs_tol]
    if any(col not in df.columns for col in cols):
        st.info("Queue-time data is incomplete for this dataset.")
        return

    for branch in selected_branches:
        branch_df = df[df[BRANCH_COL] == branch]

        # Calculate branch averages
        avg_t_wait = pd.to_numeric(branch_df[t_wait], errors='coerce').mean()
        avg_t_tol = pd.to_numeric(branch_df[t_tol], errors='coerce').mean()
        avg_cs_wait = pd.to_numeric(branch_df[cs_wait], errors='coerce').mean()
        avg_cs_tol = pd.to_numeric(branch_df[cs_tol], errors='coerce').mean()

        if pd.isna(avg_t_wait): avg_t_wait = 0
        if pd.isna(avg_t_tol): avg_t_tol = 1
        if pd.isna(avg_cs_wait): avg_cs_wait = 0
        if pd.isna(avg_cs_tol): avg_cs_tol = 1

        # Calculate queue friction
        friction_teller = avg_t_wait - avg_t_tol
        friction_cs = avg_cs_wait - avg_cs_tol

        max_t = max(avg_t_wait, avg_t_tol) * 1.3
        max_cs = max(avg_cs_wait, avg_cs_tol) * 1.3

        # Branch header
        st.markdown(f"""
        <div style="font-size:16px; font-weight:800; color:{TEXT_PRIMARY}; border-bottom:2px solid {GRID_COLOR}; padding-bottom:8px; margin-top:10px;">
            🏢 Branch: {branch}
        </div>
        """, unsafe_allow_html=True)

        fig = go.Figure()

        # ---------------------------------------------------------
        # BULLET CHART TELLER
        # ---------------------------------------------------------
        t_color = NEGATIVE_COLOR if friction_teller > 0 else POSITIVE_COLOR

        fig.add_trace(go.Indicator(
            mode = "number+gauge+delta",
            value = avg_t_wait,
            number = {'suffix': " min", 'font': {'size': 24, 'color': t_color, 'weight': 'bold'}},
            delta = {
                'reference': avg_t_tol,
                'position': "right",
                'increasing': {'color': NEGATIVE_COLOR},
                'decreasing': {'color': POSITIVE_COLOR},
                'font': {'size': 13}
            },
            domain = {'x': [0.2, 1], 'y': [0.65, 0.95]},
            # Add spacing between the metric title and tolerance label.
            title = {
                'text': f"<b>TELLER</b><br><span style='font-size:6px;'><br></span><span style='color:{TEXT_SECONDARY}; font-size:12px; font-weight:normal;'>Tolerance: {avg_t_tol:.1f} min</span>",
                'align': "left",
                'font': {'size': 15, 'color': TEXT_PRIMARY}
            },
            gauge = {
                'shape': "bullet",
                'axis': {'range': [0, max_t], 'tickfont': {'color': TEXT_SECONDARY}, 'ticksuffix': "m"},
                'threshold': {'line': {'color': "#1D2433", 'width': 4}, 'thickness': 0.8, 'value': avg_t_tol},
                'bar': {'color': t_color, 'thickness': 0.5},
                'steps': [
                    {'range': [0, avg_t_tol], 'color': "#eefaf2"},
                    {'range': [avg_t_tol, max_t], 'color': "#ffeef0"}
                ]
            }
        ))

        # ---------------------------------------------------------
        # BULLET CHART CS
        # ---------------------------------------------------------
        cs_color = NEGATIVE_COLOR if friction_cs > 0 else POSITIVE_COLOR

        fig.add_trace(go.Indicator(
            mode = "number+gauge+delta",
            value = avg_cs_wait,
            number = {'suffix': " min", 'font': {'size': 24, 'color': cs_color, 'weight': 'bold'}},
            delta = {
                'reference': avg_cs_tol,
                'position': "right",
                'increasing': {'color': NEGATIVE_COLOR},
                'decreasing': {'color': POSITIVE_COLOR},
                'font': {'size': 13}
            },
            domain = {'x': [0.2, 1], 'y': [0.1, 0.4]},
            # Add spacing between the metric title and tolerance label.
            title = {
                'text': f"<b>CS</b><br><span style='font-size:6px;'><br></span><span style='color:{TEXT_SECONDARY}; font-size:12px; font-weight:normal;'>Tolerance: {avg_cs_tol:.1f} min</span>",
                'align': "left",
                'font': {'size': 15, 'color': TEXT_PRIMARY}
            },
            gauge = {
                'shape': "bullet",
                'axis': {'range': [0, max_cs], 'tickfont': {'color': TEXT_SECONDARY}, 'ticksuffix': "m"},
                'threshold': {'line': {'color': "#1D2433", 'width': 4}, 'thickness': 0.8, 'value': avg_cs_tol},
                'bar': {'color': cs_color, 'thickness': 0.5},
                'steps': [
                    {'range': [0, avg_cs_tol], 'color': "#eefaf2"},
                    {'range': [avg_cs_tol, max_cs], 'color': "#ffeef0"}
                ]
            }
        ))

        fig.update_layout(
            height=200,
            margin=dict(l=10, r=40, t=20, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

        # Executive summary
        insight_html = ""

        if friction_teller > 0:
            insight_html += f"<div style='margin-bottom:6px;'>🔴 <b>Teller:</b> Above tolerance by <b style='color:{NEGATIVE_COLOR};'>{friction_teller:.1f} minutes</b>.</div>"
        else:
            insight_html += f"<div style='margin-bottom:6px;'>🟢 <b>Teller:</b> Within tolerance by <b style='color:{POSITIVE_COLOR};'>{abs(friction_teller):.1f} minutes</b>.</div>"

        if friction_cs > 0:
            insight_html += f"<div>🔴 <b>Customer Service:</b> Above tolerance by <b style='color:{NEGATIVE_COLOR};'>{friction_cs:.1f} minutes</b>.</div>"
        else:
            insight_html += f"<div>🟢 <b>Customer Service:</b> Within tolerance by <b style='color:{POSITIVE_COLOR};'>{abs(friction_cs):.1f} minutes</b>.</div>"

        st.markdown(f"""
        <div style="background-color:#f8fafc; padding:15px; border-radius:8px; border:1px solid #e2e8f0; margin-bottom:35px;">
            <div style="font-size:12px; font-weight:700; color:{TEXT_SECONDARY}; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px;">Branch Summary — {branch}</div>
            <div style="font-size:14px; color:{TEXT_PRIMARY}; line-height:1.5;">
                {insight_html}
            </div>
        </div>
        """, unsafe_allow_html=True)