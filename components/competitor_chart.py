"""
Competitor-analysis chart components for Page 3 of the Bank XYZ CX Dashboard.
"""

import numpy as np
import pandas as pd
import plotly.express as px
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
# 1. CORPORATE DESIGN SYSTEM
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


# ---------------------------------------------------------------------------
# 2. KPI CARDS
# ---------------------------------------------------------------------------
def render_competitor_kpis(df, df_mapping):
    total_respondents = len(df)

    primary_bank_col = (
        "Bank Manakah Yang Merupakan Rekening Utama Untuk Bapak Ibu Menyimpan Dana"
    )
    bank_dict = {
        1: "Bank BCA",
        2: "Bank Mandiri",
        3: "Bank BRI",
        4: "Bank BNI",
        5: "Bank Syariah Indonesia (BSI)",
        6: "Bank Danamon",
        7: "Bank Permata",
        8: "Bank CIMB Niaga",
        9: "Bank Mega",
        10: "Bank OCBC NISP",
    }

    if primary_bank_col in df.columns:
        df["Nama_Bank_Dana"] = (
            df[primary_bank_col].map(bank_dict).fillna("Other Banks")
        )
        competitor_df = df[df["Nama_Bank_Dana"] != "Bank XYZ"]
        total_competitor_banks = competitor_df["Nama_Bank_Dana"].nunique()
    else:
        df["Nama_Bank_Dana"] = "Unknown"
        total_competitor_banks = 0

    xyz_cols = df_mapping["Nama Kolom Bank XYZ"].dropna().tolist()
    competitor_cols = df_mapping["Nama Kolom Kompetitor"].dropna().tolist()

    valid_xyz = [column for column in xyz_cols if column in df.columns]
    valid_competitor = [column for column in competitor_cols if column in df.columns]

    # [Opsi 2] Membersihkan 99 dan 999 dari skala Likert (1-6)
    df_clean_xyz = df[valid_xyz].replace([99, 999, 99.0, 999.0], np.nan)
    raw_csi_xyz = df_clean_xyz.mean().mean() if valid_xyz else 0
    # Konversi ke Persentase (Skala 1-6)
    avg_csi_xyz = ((raw_csi_xyz - 1) / 5) * 100 if raw_csi_xyz >= 1 else 0
    
    df_clean_competitor = df[valid_competitor].replace([99, 999, 99.0, 999.0], np.nan)
    raw_csi_competitor = (
        df_clean_competitor.mean().mean() if valid_competitor else 0
    )
    # Konversi ke Persentase (Skala 1-6)
    avg_csi_competitor = ((raw_csi_competitor - 1) / 5) * 100 if raw_csi_competitor >= 1 else 0

    loyalty_col = "Ke Depannya Saya Pasti Akan Tetap Menggunakan Layanan Dari Bank Xyz"
    raw_loyalty_xyz = df[loyalty_col].replace([99, 999, 99.0, 999.0], np.nan).mean() if loyalty_col in df.columns else 0
    # Konversi ke Persentase agar konsisten dengan CSI
    loyalty_xyz = ((raw_loyalty_xyz - 1) / 5) * 100 if raw_loyalty_xyz >= 1 else 0
    
    competitor_loyalty_proxy = avg_csi_competitor

    def build_kpi_html(icon_html, title, value, subtitle=""):
        return f"""
        <div style="display:flex;align-items:center;gap:16px;height:100px;">
            {icon_html}
            <div style="display:flex;flex-direction:column;justify-content:center;">
                <div style="font-size:13px;font-weight:600;color:{TEXT_SECONDARY};text-transform:uppercase;letter-spacing:0.5px;">
                    {title}
                </div>
                <div style="font-size:28px;font-weight:800;color:{TEXT_PRIMARY};line-height:1.2;">
                    {value}
                </div>
                <div style="font-size:12px;font-weight:600;color:{PRIMARY_100};margin-top:2px;">
                    {subtitle}
                </div>
            </div>
        </div>
        """

    cols = st.columns(4, gap="large")

    with cols[0]:
        with st.container(key="kpi_comp_1"):
            icon = _kpi_asset("respondent.png", "Respondents")
            st.markdown(
                build_kpi_html(
                    icon, "Respondents", f"{total_respondents:,}", "Complete Dataset"
                ),
                unsafe_allow_html=True,
            )

    with cols[1]:
        with st.container(key="kpi_comp_2"):
            icon = _kpi_asset("cabang.png", "Banks")
            st.markdown(
                build_kpi_html(
                    icon,
                    "Competitor Banks",
                    f"{total_competitor_banks}",
                    "Detected Banks",
                ),
                unsafe_allow_html=True,
            )

    with cols[2]:
        with st.container(key="kpi_comp_3"):
            icon = _kpi_asset("csi.png", "CSI")
            st.markdown(
                build_kpi_html(
                    icon,
                    "Avg. CSI XYZ",
                    f"{avg_csi_xyz:.1f}%", # <-- Menampilkan Format Persentase
                    f"vs Comp Avg: {avg_csi_competitor:.1f}%",
                ),
                unsafe_allow_html=True,
            )

    with cols[3]:
        with st.container(key="kpi_comp_4"):
            icon = _kpi_asset("nps.png", "NPS")
            st.markdown(
                build_kpi_html(
                    icon,
                    "Avg. Loyalty XYZ",
                    f"{loyalty_xyz:.1f}%", # <-- Menampilkan Format Persentase
                    f"vs Comp Proxy: {competitor_loyalty_proxy:.1f}%",
                ),
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    return df


# ---------------------------------------------------------------------------
# 3. MACRO CHARTS (BAR & RADAR)
# ---------------------------------------------------------------------------
def render_competitor_macro_charts(df, df_mapping):
    col_bar, col_radar = st.columns([1, 1], gap="large")

    with col_bar:
        with st.container(key="p3_card_bar"):
            st.markdown(
                f'<div style="font-size:16px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:12px;">'
                'Top 5 Competitor Banks by Primary Savings Account</div>',
                unsafe_allow_html=True,
            )

            top_5_banks = (
                df["Nama_Bank_Dana"]
                .value_counts()
                .head(5)
                .reset_index()
            )
            top_5_banks.columns = ["Bank", "Total"]
            top_5_banks = top_5_banks.sort_values("Total", ascending=True)

            max_val = top_5_banks["Total"].max()

            # ── Warna per-batang: peringkat 1 (nilai tertinggi) = merah,
            #    sisanya = abu-abu — menggunakan go.Bar agar bisa assign per-bar ──
            bar_colors = [
                PRIMARY_100 if v == max_val else BG_300
                for v in top_5_banks["Total"]
            ]
            text_colors = [
                TEXT_PRIMARY if v == max_val else TEXT_SECONDARY
                for v in top_5_banks["Total"]
            ]

            fig_bar = go.Figure(go.Bar(
                x=top_5_banks["Total"],
                y=top_5_banks["Bank"],
                orientation="h",
                text=top_5_banks["Total"],
                textposition="outside",
                cliponaxis=False,
                textfont=dict(size=12, color=TEXT_PRIMARY, family="Inter"),
                marker=dict(
                    color=bar_colors,
                    line=dict(width=0),
                    cornerradius=6,
                ),
                hovertemplate="<b>%{y}</b><br>Respondents: %{x}<extra></extra>",
            ))

            fig_bar.update_layout(
                height=345,
                bargap=0.28,
                margin=dict(l=0, r=50, t=0, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    title="",
                    showgrid=False,
                    showticklabels=False,
                    showline=False,
                    zeroline=False,
                    range=[0, max_val * 1.18],   # ruang label di kanan
                ),
                yaxis=dict(
                    title="",
                    tickfont=dict(size=12, color=TEXT_PRIMARY, weight="bold"),
                    automargin=True,
                ),
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with col_radar:
        with st.container(key="p3_card_radar"):
            st.markdown(
                f"""
                <div style="font-size:16px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:5px;">
                    Radar CSI: XYZ vs Average Competitor
                </div>
                """,
                unsafe_allow_html=True,
            )

            categories = df_mapping["Kategori Touchpoint"].dropna().unique()
            radar_data = []

            for category in categories:
                cat_map = df_mapping[df_mapping["Kategori Touchpoint"] == category]
                xyz_columns = [
                    column
                    for column in cat_map["Nama Kolom Bank XYZ"]
                    if column in df.columns
                ]
                competitor_columns = [
                    column
                    for column in cat_map["Nama Kolom Kompetitor"]
                    if column in df.columns
                ]

                # [Opsi 2] Membersihkan 99 dan 999 dari skala Likert (1-6) pada Radar Chart
                xyz_value = (
                    df[xyz_columns].replace([99, 999, 99.0, 999.0], np.nan).mean().mean() if xyz_columns else 0
                )
                competitor_value = (
                    df[competitor_columns].replace([99, 999, 99.0, 999.0], np.nan).mean().mean()
                    if competitor_columns
                    else 0
                )

                short_category = (
                    str(category).replace(" Touchpoint", "").replace(" & ", "<br>& ")
                )
                radar_data.append(
                    {
                        "Category": short_category,
                        "XYZ": xyz_value,
                        "Kompetitor": competitor_value,
                    }
                )

            df_radar = pd.DataFrame(radar_data)

            COMPETITOR_COLOR = "#2563eb"
            COMPETITOR_FILL = "rgba(37, 99, 235, 0.08)"

            all_values = df_radar["XYZ"].tolist() + df_radar["Kompetitor"].tolist()
            non_zero_values = [value for value in all_values if value > 0]

            if non_zero_values:
                r_min = max(1.0, round(min(non_zero_values) - 0.5, 1))
                r_max = min(6.0, round(max(non_zero_values) + 0.2, 1)) # <-- Radar disesuaikan max skala 6
            else:
                r_min, r_max = 1.0, 6.0

            span = r_max - r_min
            dtick = round(span / 4, 1) if span > 0 else 1

            r_competitor = df_radar["Kompetitor"].tolist() + [
                df_radar["Kompetitor"].iloc[0]
            ]
            r_xyz = df_radar["XYZ"].tolist() + [df_radar["XYZ"].iloc[0]]
            theta = df_radar["Category"].tolist() + [df_radar["Category"].iloc[0]]

            label_competitor = [f"{value:.2f}" for value in df_radar["Kompetitor"]] + [""]
            label_xyz = [f"{value:.2f}" for value in df_radar["XYZ"]] + [""]

            fig_radar = go.Figure()

            fig_radar.add_trace(
                go.Scatterpolar(
                    r=r_competitor,
                    theta=theta,
                    name="Avg Competitor",
                    fill="toself",
                    fillcolor=COMPETITOR_FILL,
                    line=dict(color=COMPETITOR_COLOR, width=2.5, dash="dash"),
                    mode="lines+markers+text",
                    text=label_competitor,
                    textposition="top center",
                    textfont=dict(size=10, color=COMPETITOR_COLOR, weight="bold"),
                    marker=dict(
                        size=9,
                        symbol="diamond",
                        color=COMPETITOR_COLOR,
                        line=dict(width=2, color="white"),
                    ),
                    hovertemplate="<b>%{theta}</b><br>Competitor: %{r:.2f}<extra></extra>",
                )
            )

            fig_radar.add_trace(
                go.Scatterpolar(
                    r=r_xyz,
                    theta=theta,
                    name="Bank XYZ",
                    fill="toself",
                    fillcolor="rgba(187, 38, 73, 0.2)",
                    line=dict(color=PRIMARY_100, width=3),
                    mode="lines+markers+text",
                    text=label_xyz,
                    textposition="top center",
                    textfont=dict(size=10, color=PRIMARY_100, weight="bold"),
                    marker=dict(
                        size=10,
                        symbol="circle",
                        color=PRIMARY_100,
                        line=dict(width=2.5, color="white"),
                    ),
                    hovertemplate="<b>%{theta}</b><br>Bank XYZ: %{r:.2f}<extra></extra>",
                )
            )

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
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12, color=TEXT_PRIMARY),
                    bgcolor="rgba(0,0,0,0)",
                    itemsizing="constant",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(
                fig_radar, use_container_width=True, config={"displayModeBar": False}
            )

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 4. MICRO HEATMAP DEEP-DIVE
# ---------------------------------------------------------------------------
def render_competitor_heatmap(df, df_mapping):
    st.markdown(
        """
        <style>
        .ht-cell { position:relative; cursor:help; overflow:visible; }
        .ht-tip {
            visibility:hidden; opacity:0;
            position:absolute; bottom:calc(100% + 8px); left:50%;
            transform:translateX(-50%);
            background:#1D2433; color:#ffffff;
            padding:10px 14px; border-radius:8px;
            font-size:12px; font-family:Inter,sans-serif;
            line-height:1.6; white-space:nowrap;
            z-index:99999; box-shadow:0 6px 20px rgba(0,0,0,0.3);
            pointer-events:none;
            transition:opacity 0.15s ease,visibility 0.15s ease;
        }
        .ht-tip::after {
            content:""; position:absolute; top:100%; left:50%;
            transform:translateX(-50%);
            border:5px solid transparent; border-top-color:#1D2433;
        }
        .ht-cell:hover .ht-tip { visibility:visible; opacity:1; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key="p3_card_filter"):
        st.markdown(
            f"""
            <div style="font-size:18px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:15px;">
                Head-to-Head Touchpoint Gap Analysis
            </div>
            """,
            unsafe_allow_html=True,
        )
        categories = df_mapping["Kategori Touchpoint"].dropna().unique().tolist()
        selected_category = st.selectbox(
            "📂 Select Touchpoint Area to Compare:", categories
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    with st.container(key="p3_card_heatmap"):
        cat_map = df_mapping[df_mapping["Kategori Touchpoint"] == selected_category]

        header_cols = st.columns([3, 1.5, 1.5])
        with header_cols[0]:
            st.markdown(
                '<div style="font-weight:700;font-size:18px;color:#374151;padding-top:10px;">'
                "Attribute / Touchpoint</div>",
                unsafe_allow_html=True,
            )
        with header_cols[1]:
            st.markdown(
                '<div style="text-align:center;font-weight:700;font-size:16px;color:#4b5563;padding-top:10px;">'
                "Bank XYZ</div>",
                unsafe_allow_html=True,
            )
        with header_cols[2]:
            st.markdown(
                '<div style="text-align:center;font-weight:700;font-size:16px;color:#4b5563;padding-top:10px;">'
                "Competitor</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        CELL_STYLE = (
            "border-radius:14px; height:44px; display:flex; "
            "align-items:center; justify-content:center; "
            "font-weight:700; font-size:16px; margin-bottom:4px; transition:0.2s;"
        )

        for _, row in cat_map.iterrows():
            indicator = row["Indikator Core Touchpoint"]
            xyz_column = row["Nama Kolom Bank XYZ"]
            competitor_column = row["Nama Kolom Kompetitor"]

            # [Opsi 2] Membersihkan 99 dan 999 dari skala Likert (1-6) pada Heatmap
            xyz_value = (
                df[xyz_column].replace([99, 999, 99.0, 999.0], np.nan).apply(pd.to_numeric, errors="coerce").mean()
                if xyz_column in df.columns
                else np.nan
            )
            competitor_value = (
                df[competitor_column].replace([99, 999, 99.0, 999.0], np.nan)
                .apply(pd.to_numeric, errors="coerce")
                .mean()
                if competitor_column in df.columns
                else np.nan
            )
            
            gap = (
                xyz_value - competitor_value
                if not pd.isna(xyz_value) and not pd.isna(competitor_value)
                else np.nan
            )

            if pd.isna(gap):
                xyz_bg, xyz_txt = "#f8fafc", "#94a3b8"
                competitor_bg, competitor_txt = "#f8fafc", "#94a3b8"
                gap_text = "N/A"
            elif gap > 0:
                xyz_bg, xyz_txt = POSITIVE_COLOR, "#ffffff"
                competitor_bg, competitor_txt = "#f1f5f9", "#64748b"
                gap_text = f"+{gap:.2f}"
            elif gap < 0:
                xyz_bg, xyz_txt = "#f1f5f9", "#64748b"
                competitor_bg, competitor_txt = POSITIVE_COLOR, "#ffffff"
                gap_text = f"{gap:.2f}"
            else:
                xyz_bg, xyz_txt = "#e2e8f0", "#475569"
                competitor_bg, competitor_txt = "#e2e8f0", "#475569"
                gap_text = "0.00"

            display_xyz = f"{xyz_value:.2f}" if not pd.isna(xyz_value) else "N/A"
            display_competitor = (
                f"{competitor_value:.2f}" if not pd.isna(competitor_value) else "N/A"
            )

            if pd.isna(gap):
                tooltip_xyz = "<b>🏦 Bank XYZ</b><br>Incomplete Data"
                tooltip_competitor = "<b>🏛️ Avg Competitor</b><br>Incomplete Data"
            else:
                if gap > 0:
                    status_xyz = f"🏆 Winning! Ahead by {abs(gap):.2f} pts"
                    status_competitor = f"Trailing (Behind by {abs(gap):.2f} pts vs XYZ)"
                elif gap < 0:
                    status_xyz = f"Trailing (Behind by {abs(gap):.2f} pts vs Comp)"
                    status_competitor = f"🏆 Winning! Ahead by {abs(gap):.2f} pts vs XYZ"
                else:
                    status_xyz = "Tie Score"
                    status_competitor = "Tie Score"

                tooltip_xyz = f"<b>🏦 Bank XYZ</b><br>Score: {display_xyz}<br>{status_xyz}"
                tooltip_competitor = (
                    f"<b>🏛️ Avg Competitor</b><br>Score: {display_competitor}<br>{status_competitor}"
                )

            cols = st.columns([3, 1.5, 1.5])

            with cols[0]:
                st.markdown(
                    f'<div style="height:46px;display:flex;align-items:center;'
                    f'font-weight:600;color:#1f2937;font-size:13px;">{indicator}</div>',
                    unsafe_allow_html=True,
                )

            with cols[1]:
                st.markdown(
                    f'<div class="ht-cell">'
                    f'<div class="ht-tip">{tooltip_xyz}</div>'
                    f'<div style="background:{xyz_bg};color:{xyz_txt};{CELL_STYLE}">{display_xyz}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

            with cols[2]:
                st.markdown(
                    f'<div class="ht-cell">'
                    f'<div class="ht-tip">{tooltip_competitor}</div>'
                    f'<div style="background:{competitor_bg};color:{competitor_txt};{CELL_STYLE}">{display_competitor}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )