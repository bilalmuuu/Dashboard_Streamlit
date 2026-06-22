"""
components/kpi_cards.py
========================
Reusable KPI card components untuk Bank XYZ Dashboard dengan Ikon 80px & Optimasi Ruang.
"""

import streamlit as st
import base64
import os

# ──────────────────────────────────────────────────────────────────────────────
# FUNGSI PEMBACA GAMBAR
# ──────────────────────────────────────────────────────────────────────────────
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

# ──────────────────────────────────────────────────────────────────────────────
# KPI CARDS (MENGGUNAKAN STRING CONCATENATION AGAR KEBAL AUTO-FORMAT)
# ──────────────────────────────────────────────────────────────────────────────

def render_total_respondents_kpi(df):
    total_respondents = len(df) if df is not None else 0
    img_b64 = get_image_base64("assets/respondent.png")

    html = (
        '<div style="display: flex; align-items: center; gap: 10px; height: 90px;">'
            f'<img src="data:image/png;base64,{img_b64}" alt="icon" style="width: 80px; height: 80px; object-fit: contain; flex-shrink: 0; margin-left: -15px;">'
            '<div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center;">'
                '<div class="kpi-title" style="margin-bottom: 2px; font-size: 12px;">Total Respondents</div>'
                f'<div class="kpi-value-large" style="font-size: 24px; line-height: 1;">{total_respondents:,}</div>'
                '<div class="kpi-subtitle" style="margin-top: 4px; font-size: 11px;">Survey Participants</div>'
            '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_usia_kpi(df):
    col = "usia_label"
    if df is None or df.empty or col not in df.columns:
        st.markdown("<div style='color:#94a3b8; height: 90px;'>No data</div>", unsafe_allow_html=True)
        return

    total = len(df)
    counts = df[col].value_counts()
    dominant_label = counts.idxmax()
    dominant_pct = round((counts.max() / total) * 100, 1)
    img_b64 = get_image_base64("assets/umur.png")

    html = (
        '<div style="display: flex; align-items: center; gap: 10px; height: 90px;">'
            f'<img src="data:image/png;base64,{img_b64}" alt="icon" style="width: 80px; height: 80px; object-fit: contain; flex-shrink: 0; margin-left: -15px;">'
            '<div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center;">'
                '<div class="kpi-title" style="margin-bottom: 2px; font-size: 12px;">Top Age Group</div>'
                f'<div class="kpi-value-large" style="font-size: 24px; line-height: 1;">{dominant_pct}%</div>'
                f'<div class="kpi-subtitle" style="margin-top: 4px; font-size: 11px; font-weight: 600;">{dominant_label.title()}</div>'
            '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_tenure_kpi(df):
    col = "Sudah Berapa Lamakah Menjadi Nasabah Bank Xyz"
    if df is None or df.empty:
        st.markdown("<div style='color:#94a3b8; height: 90px;'>No data</div>", unsafe_allow_html=True)
        return

    total         = len(df)
    counts        = df[col].value_counts()
    dominant_code = counts.idxmax()
    dominant_label = df.loc[df[col] == dominant_code, "tenure_label"].iloc[0]
    dominant_pct   = round((counts[dominant_code] / total) * 100, 1)
    img_b64 = get_image_base64("assets/tenure.png")

    html = (
        '<div style="display: flex; align-items: center; gap: 10px; height: 90px;">'
            f'<img src="data:image/png;base64,{img_b64}" alt="icon" style="width: 80px; height: 80px; object-fit: contain; flex-shrink: 0; margin-left: -15px;">'
            '<div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center;">'
                '<div class="kpi-title" style="margin-bottom: 2px; font-size: 12px;">Tenure</div>'
                f'<div class="kpi-value-large" style="font-size: 24px; line-height: 1;">{dominant_pct}%</div>'
                f'<div class="kpi-subtitle" style="margin-top: 4px; font-size: 11px; font-weight: 600;">{dominant_label}</div>'
            '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_kategori_nasabah_kpi(df):
    col = "Kategori Nasabah"
    if df is None or df.empty:
        st.markdown("<div style='color:#94a3b8; height: 90px;'>No data</div>", unsafe_allow_html=True)
        return

    total         = len(df)
    counts        = df[col].value_counts()
    dominant_code = counts.idxmax()
    label_col     = "kategori_nasabah_label"
    dominant_label = df.loc[df[col] == dominant_code, label_col].iloc[0]
    dominant_pct   = round((counts[dominant_code] / total) * 100, 1)
    display_label = dominant_label.replace("Nasabah ", "")
    img_b64 = get_image_base64("assets/type.png")

    html = (
        '<div style="display: flex; align-items: center; gap: 10px; height: 90px;">'
            f'<img src="data:image/png;base64,{img_b64}" alt="icon" style="width: 80px; height: 80px; object-fit: contain; flex-shrink: 0; margin-left: -15px;">'
            '<div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center;">'
                '<div class="kpi-title" style="margin-bottom: 2px; font-size: 12px;">Customer Type</div>'
                f'<div class="kpi-value-large" style="font-size: 24px; line-height: 1;">{dominant_pct}%</div>'
                f'<div class="kpi-subtitle" style="margin-top: 4px; font-size: 11px; font-weight: 600;">{display_label}</div>'
            '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_saving_rate_kpi(df):
    from helpers.loader import calculate_avg_saving_rate
    saving_rate = calculate_avg_saving_rate(df)
    
    rate_class = "saving-positive" if saving_rate >= 0 else "saving-negative"
    img_b64 = get_image_base64("assets/saving.png")

    html = (
        '<div style="display: flex; align-items: center; gap: 10px; height: 90px;">'
            f'<img src="data:image/png;base64,{img_b64}" alt="icon" style="width: 80px; height: 80px; object-fit: contain; flex-shrink: 0; margin-left: -15px;">'
            '<div style="display: flex; flex-direction: column; align-items: flex-start; justify-content: center;">'
                '<div class="kpi-title" style="margin-bottom: 2px; font-size: 12px;">Avg. Saving Rate</div>'
                f'<div class="kpi-value-large {rate_class}" style="font-size: 24px; line-height: 1;">{saving_rate}%</div>'
                '<div class="kpi-subtitle" style="margin-top: 4px; font-size: 11px;">Of Monthly Income</div>'
            '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)