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

    avg_csi_xyz = df[valid_xyz].mean().mean() if valid_xyz else 0
    avg_csi_competitor = (
        df[valid_competitor].mean().mean() if valid_competitor else 0
    )

    loyalty_col = "Ke Depannya Saya Pasti Akan Tetap Menggunakan Layanan Dari Bank Xyz"
    loyalty_xyz = df[loyalty_col].mean() if loyalty_col in df.columns else 0
    competitor_loyalty_proxy = (
        avg_csi_competitor * 2 if avg_csi_competitor > 0 else 0
    )

    def build_kpi_html(icon_html, title, value, subtitle=""):
        return (
            '<div style="display:flex;align-items:center;gap:16px;min-height:116px;width:100%;padding:6px 2px;">'
            '<div style="width:76px;height:76px;flex-shrink:0;'
            'display:flex;align-items:center;justify-content:center;">'
            f'{icon_html}'
            '</div>'
            '<div style="display:flex;flex-direction:column;align-items:flex-start;'
            'justify-content:center;min-width:0;">'
            f'<div class="kpi-title" style="margin-bottom:5px;white-space:normal;line-height:1.25;overflow-wrap:anywhere;">{title}</div>'
            f'<div class="kpi-value-large" style="font-size:27px;line-height:1.1;white-space:nowrap;">{value}</div>'
            f'<div class="kpi-subtitle" style="margin-top:6px;white-space:normal;line-height:1.3;overflow-wrap:anywhere;">{subtitle}</div>'
            "</div>"
            "</div>"
        )

    kpi_cols = st.columns(4, gap="medium")

    with kpi_cols[0]:
        with st.container(key="kpi_comp_1"):
            st.markdown(
                build_kpi_html(
                    _kpi_asset("bank.png", "Total respondents"),
                    "Total Respondents",
                    f"{total_respondents:,}",
                    "All survey records",
                ),
                unsafe_allow_html=True,
            )

    with kpi_cols[1]:
        with st.container(key="kpi_comp_2"):
            st.markdown(
                build_kpi_html(
                    _kpi_asset("cabang.png", "Competitor banks"),
                    "Competitor Banks",
                    f"{total_competitor_banks}",
                    "Detected institutions",
                ),
                unsafe_allow_html=True,
            )

    with kpi_cols[2]:
        with st.container(key="kpi_comp_3"):
            st.markdown(
                build_kpi_html(
                    _kpi_asset("csi.png", "Customer satisfaction index"),
                    "Bank XYZ Avg. CSI",
                    f"{avg_csi_xyz:.2f}",
                    f"Competitor avg.: {avg_csi_competitor:.2f}",
                ),
                unsafe_allow_html=True,
            )

    with kpi_cols[3]:
        with st.container(key="kpi_comp_4"):
            st.markdown(
                build_kpi_html(
                    _kpi_asset("nps.png", "Average loyalty"),
                    "Bank XYZ Loyalty",
                    f"{loyalty_xyz:.2f}",
                    f"Competitor proxy: {competitor_loyalty_proxy:.2f}",
                ),
                unsafe_allow_html=True,
            )

    return df


# ---------------------------------------------------------------------------
# 3. TOP COMPETITORS AND CSI RADAR
# ---------------------------------------------------------------------------
def render_competitor_macro_charts(df, df_mapping):
    col_bar, col_radar = st.columns([1, 1], gap="large")

    with col_bar:
        with st.container(key="p3_card_bar"):
            st.markdown(
                f"""
                <div style="font-size:16px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:15px;">
                    Top 5 Competitor Banks by Primary Savings Account
                </div>
                """,
                unsafe_allow_html=True,
            )

            top_5_banks = (
                df["Nama_Bank_Dana"]
                .value_counts()
                .head(5)
                .reset_index()
            )
            top_5_banks.columns = ["Bank", "Total"]
            top_5_banks = top_5_banks.sort_values(by="Total", ascending=True)

            fig_bar = px.bar(
                top_5_banks,
                x="Total",
                y="Bank",
                orientation="h",
                text="Total",
                color_discrete_sequence=[PRIMARY_100],
            )

            fig_bar.update_traces(
                textposition="outside",
                textfont=dict(size=13, weight="bold", color=TEXT_PRIMARY),
                marker=dict(line=dict(width=0)),
                hovertemplate="<b>%{y}</b><br>Respondents: %{x}<extra></extra>",
            )

            fig_bar.update_layout(
                height=341,
                margin=dict(l=0, r=30, t=10, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, showticklabels=False, title=""),
                yaxis=dict(
                    title="",
                    tickfont=dict(size=13, color=TEXT_PRIMARY, weight="bold"),
                ),
            )

            st.plotly_chart(
                fig_bar,
                width="stretch",
                config={"displayModeBar": False},
            )

    with col_radar:
        with st.container(key="p3_card_radar"):
            st.markdown(
                f"""
                <div style="font-size:16px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:5px;">
                    CSI Radar: Bank XYZ vs. Competitor Average
                </div>
                """,
                unsafe_allow_html=True,
            )

            categories = df_mapping["Kategori Touchpoint"].dropna().unique()
            radar_data = []

            for category in categories:
                category_mapping = df_mapping[
                    df_mapping["Kategori Touchpoint"] == category
                ]
                xyz_columns = [
                    column
                    for column in category_mapping["Nama Kolom Bank XYZ"]
                    if column in df.columns
                ]
                competitor_columns = [
                    column
                    for column in category_mapping["Nama Kolom Kompetitor"]
                    if column in df.columns
                ]

                xyz_value = (
                    df[xyz_columns].mean().mean() if xyz_columns else 0
                )
                competitor_value = (
                    df[competitor_columns].mean().mean()
                    if competitor_columns
                    else 0
                )

                short_category = (
                    str(category)
                    .replace(" Touchpoint", "")
                    .replace(" & ", "<br>& ")
                )
                radar_data.append(
                    {
                        "Category": short_category,
                        "XYZ": xyz_value,
                        "Competitor": competitor_value,
                    }
                )

            radar_df = pd.DataFrame(radar_data)

            if radar_df.empty:
                st.info("Radar data is unavailable for the selected dataset.")
                return

            competitor_color = "#2563eb"
            competitor_fill = "rgba(37,99,235,0.08)"
            xyz_fill = "rgba(187,38,73,0.08)"

            all_values = (
                radar_df["XYZ"].tolist()
                + radar_df["Competitor"].tolist()
            )
            non_zero_values = [value for value in all_values if value > 0]

            if non_zero_values:
                radial_min = max(0.0, round(min(non_zero_values) - 0.5, 1))
                radial_max = min(7.0, round(max(non_zero_values) + 0.2, 1))
            else:
                radial_min, radial_max = 0.0, 7.0

            span = radial_max - radial_min
            radial_tick = round(span / 4, 1) if span > 0 else 1

            competitor_values = (
                radar_df["Competitor"].tolist()
                + [radar_df["Competitor"].iloc[0]]
            )
            xyz_values = (
                radar_df["XYZ"].tolist()
                + [radar_df["XYZ"].iloc[0]]
            )
            theta = (
                radar_df["Category"].tolist()
                + [radar_df["Category"].iloc[0]]
            )

            competitor_labels = [
                f"{value:.2f}" for value in radar_df["Competitor"]
            ] + [""]
            xyz_labels = [f"{value:.2f}" for value in radar_df["XYZ"]] + [""]

            fig_radar = go.Figure()

            fig_radar.add_trace(
                go.Scatterpolar(
                    r=competitor_values,
                    theta=theta,
                    name="Competitor Average",
                    fill="toself",
                    fillcolor=competitor_fill,
                    line=dict(color=competitor_color, width=2.5, dash="dash"),
                    mode="lines+markers+text",
                    text=competitor_labels,
                    textposition="top center",
                    textfont=dict(
                        size=10,
                        color=competitor_color,
                        weight="bold",
                    ),
                    marker=dict(
                        size=9,
                        symbol="diamond",
                        color=competitor_color,
                        line=dict(width=2, color="#FFFFFF"),
                    ),
                )
            )

            fig_radar.add_trace(
                go.Scatterpolar(
                    r=xyz_values,
                    theta=theta,
                    name="Bank XYZ",
                    fill="toself",
                    fillcolor=xyz_fill,
                    line=dict(color=PRIMARY_100, width=3),
                    mode="lines+markers+text",
                    text=xyz_labels,
                    textposition="top center",
                    textfont=dict(size=10, color=PRIMARY_100, weight="bold"),
                    marker=dict(
                        size=10,
                        symbol="circle",
                        color=PRIMARY_100,
                        line=dict(width=2.5, color="#FFFFFF"),
                    ),
                )
            )

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[radial_min, radial_max],
                        dtick=radial_tick,
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
                fig_radar,
                width="stretch",
                config={"displayModeBar": False},
            )


# ---------------------------------------------------------------------------
# 4. TOUCHPOINT GAP HEATMAP
# ---------------------------------------------------------------------------
def render_competitor_heatmap(df, df_mapping):
    st.markdown(
        """
        <style>
        .ht-cell {
            position: relative;
            cursor: help;
            overflow: visible;
        }

        .ht-tip {
            visibility: hidden;
            opacity: 0;
            position: absolute;
            bottom: calc(100% + 8px);
            left: 50%;
            transform: translateX(-50%);
            background: #1D2433;
            color: #FFFFFF;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-family: Inter, sans-serif;
            line-height: 1.6;
            white-space: nowrap;
            z-index: 99999;
            box-shadow: 0 6px 20px rgba(0,0,0,0.30);
            pointer-events: none;
            transition: opacity 0.15s ease, visibility 0.15s ease;
        }

        .ht-tip::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 5px solid transparent;
            border-top-color: #1D2433;
        }

        .ht-cell:hover .ht-tip {
            visibility: visible;
            opacity: 1;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key="p3_card_filter"):
        st.markdown(
            f"""
            <div style="font-size:18px;font-weight:800;color:{TEXT_PRIMARY};margin-bottom:4px;">
                Touchpoint Gap Analysis
            </div>
            <div style="font-size:12px;color:{TEXT_SECONDARY};margin-bottom:15px;">
                Compare Bank XYZ performance with the competitor average across service attributes.
            </div>
            """,
            unsafe_allow_html=True,
        )

        categories = (
            df_mapping["Kategori Touchpoint"].dropna().unique().tolist()
        )
        selected_category = st.selectbox(
            "Touchpoint Category",
            categories,
        )

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    with st.container(key="p3_card_heatmap"):
        category_mapping = df_mapping[
            df_mapping["Kategori Touchpoint"] == selected_category
        ]

        header_cols = st.columns([3, 1.5, 1.5])

        with header_cols[0]:
            st.markdown(
                '<div style="font-weight:700;font-size:18px;color:#1D2433;padding-top:10px;">'
                "Attribute / Touchpoint</div>",
                unsafe_allow_html=True,
            )

        with header_cols[1]:
            st.markdown(
                '<div style="text-align:center;font-weight:700;font-size:16px;color:#5E6677;padding-top:10px;">'
                "Bank XYZ</div>",
                unsafe_allow_html=True,
            )

        with header_cols[2]:
            st.markdown(
                '<div style="text-align:center;font-weight:700;font-size:16px;color:#5E6677;padding-top:10px;">'
                "Competitor Average</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        cell_style = (
            "border-radius:14px;height:44px;display:flex;"
            "align-items:center;justify-content:center;"
            "font-weight:700;font-size:16px;margin-bottom:4px;transition:0.2s;"
        )

        for _, row in category_mapping.iterrows():
            indicator = row["Indikator Core Touchpoint"]
            xyz_column = row["Nama Kolom Bank XYZ"]
            competitor_column = row["Nama Kolom Kompetitor"]

            xyz_value = (
                df[xyz_column].apply(pd.to_numeric, errors="coerce").mean()
                if xyz_column in df.columns
                else np.nan
            )
            competitor_value = (
                df[competitor_column]
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
                xyz_bg, xyz_text = "#f8fafc", "#94a3b8"
                competitor_bg, competitor_text = "#f8fafc", "#94a3b8"
            elif gap > 0:
                xyz_bg, xyz_text = POSITIVE_COLOR, "#ffffff"
                competitor_bg, competitor_text = "#f1f5f9", "#64748b"
            elif gap < 0:
                xyz_bg, xyz_text = "#f1f5f9", "#64748b"
                competitor_bg, competitor_text = POSITIVE_COLOR, "#ffffff"
            else:
                xyz_bg, xyz_text = "#e2e8f0", "#475569"
                competitor_bg, competitor_text = "#e2e8f0", "#475569"

            xyz_display = f"{xyz_value:.2f}" if not pd.isna(xyz_value) else "N/A"
            competitor_display = (
                f"{competitor_value:.2f}"
                if not pd.isna(competitor_value)
                else "N/A"
            )

            if pd.isna(gap):
                xyz_tooltip = "<b>Bank XYZ</b><br>Incomplete data"
                competitor_tooltip = (
                    "<b>Competitor Average</b><br>Incomplete data"
                )
            elif gap > 0:
                xyz_tooltip = (
                    f"<b>Bank XYZ</b><br>Score: {xyz_display}<br>"
                    f"Leads by {abs(gap):.2f} points over the competitor average"
                )
                competitor_tooltip = (
                    f"<b>Competitor Average</b><br>Score: {competitor_display}<br>"
                    f"Trails by {abs(gap):.2f} points behind Bank XYZ"
                )
            elif gap < 0:
                xyz_tooltip = (
                    f"<b>Bank XYZ</b><br>Score: {xyz_display}<br>"
                    f"Trails by {abs(gap):.2f} points behind the competitor average"
                )
                competitor_tooltip = (
                    f"<b>Competitor Average</b><br>Score: {competitor_display}<br>"
                    f"Leads by {abs(gap):.2f} points over Bank XYZ"
                )
            else:
                xyz_tooltip = (
                    f"<b>Bank XYZ</b><br>Score: {xyz_display}<br>Equal score"
                )
                competitor_tooltip = (
                    f"<b>Competitor Average</b><br>Score: {competitor_display}<br>Equal score"
                )

            cols = st.columns([3, 1.5, 1.5])

            with cols[0]:
                st.markdown(
                    f'<div style="height:46px;display:flex;align-items:center;'
                    f'font-weight:600;color:#1D2433;font-size:13px;">{indicator}</div>',
                    unsafe_allow_html=True,
                )

            with cols[1]:
                st.markdown(
                    f'<div class="ht-cell">'
                    f'<div class="ht-tip">{xyz_tooltip}</div>'
                    f'<div style="background:{xyz_bg};color:{xyz_text};{cell_style}">'
                    f"{xyz_display}</div></div>",
                    unsafe_allow_html=True,
                )

            with cols[2]:
                st.markdown(
                    f'<div class="ht-cell">'
                    f'<div class="ht-tip">{competitor_tooltip}</div>'
                    f'<div style="background:{competitor_bg};color:{competitor_text};{cell_style}">'
                    f"{competitor_display}</div></div>",
                    unsafe_allow_html=True,
                )