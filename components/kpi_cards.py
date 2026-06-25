"""
Reusable KPI card components for the Bank XYZ CX Dashboard.
"""


import streamlit as st
import base64
import os

# Customer type translation mapping
CUSTOMER_TYPE_TRANSLATION = {
    "nasabah prioritas": "Priority Customer",
    "priority customer": "Priority Customer",
    "nasabah reguler": "Regular Customer",
    "regular customer": "Regular Customer",
    "nasabah tabungan xyz reguler": "Regular Bank XYZ Savings Customer",
    "nasabah tabungan bank xyz reguler": "Regular Bank XYZ Savings Customer",
    "regular bank xyz savings customer": "Regular Bank XYZ Savings Customer",
}

# ──────────────────────────────────────────────────────────────────────────────
# IMAGE UTILITIES
# ──────────────────────────────────────────────────────────────────────────────
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


def render_empty_kpi(message="No data available"):
    st.markdown(
        f"""
        <div style="height:90px;display:flex;align-items:center;color:#98A1B3;font-size:12px;font-weight:600;">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────────────────────────────────────
# KPI CARDS
# ──────────────────────────────────────────────────────────────────────────────

def render_total_respondents_kpi(df):
    total_respondents = len(df) if df is not None else 0
    img_b64 = get_image_base64("assets/respondent.png")

    html = (
        '<div style="display:flex;align-items:center;gap:12px;height:90px;width:100%;">'
            f'<img src="data:image/png;base64,{img_b64}" alt="icon" style="width: 68px; height: 68px; object-fit: contain; flex-shrink: 0; margin-left: -8px;">'
            '<div style="display:flex;flex-direction:column;align-items:flex-start;justify-content:center;min-width:0;">'
                '<div class="kpi-title" style="margin-bottom:3px;">Total Respondents</div>'
                f'<div class="kpi-value-large" style="font-size:24px;line-height:1;">{total_respondents:,}</div>'
                '<div class="kpi-subtitle" style="margin-top:5px;">Survey respondents</div>'
            '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_usia_kpi(df):
    col = "usia_label"
    if df is None or df.empty or col not in df.columns:
        render_empty_kpi()
        return

    total = len(df)
    counts = df[col].value_counts()
    dominant_label = counts.idxmax()
    dominant_pct = round((counts.max() / total) * 100, 1)
    img_b64 = get_image_base64("assets/umur.png")

    html = (
        '<div style="display:flex;align-items:center;gap:12px;height:90px;width:100%;">'
            f'<img src="data:image/png;base64,{img_b64}" alt="icon" style="width: 68px; height: 68px; object-fit: contain; flex-shrink: 0; margin-left: -8px;">'
            '<div style="display:flex;flex-direction:column;align-items:flex-start;justify-content:center;min-width:0;">'
                '<div class="kpi-title" style="margin-bottom:3px;">Top Age Group</div>'
                f'<div class="kpi-value-large" style="font-size:24px;line-height:1;">{dominant_pct}%</div>'
                f'<div class="kpi-subtitle" style="margin-top:5px;">{dominant_label.title()}</div>'
            '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_tenure_kpi(df):
    col = "Sudah Berapa Lamakah Menjadi Nasabah Bank Xyz"
    required_columns = {col, "tenure_label"}
    if df is None or df.empty or not required_columns.issubset(df.columns):
        render_empty_kpi()
        return

    total         = len(df)
    counts        = df[col].value_counts()
    dominant_code = counts.idxmax()
    dominant_label = df.loc[df[col] == dominant_code, "tenure_label"].iloc[0]
    dominant_pct   = round((counts[dominant_code] / total) * 100, 1)
    img_b64 = get_image_base64("assets/tenure.png")

    html = (
        '<div style="display:flex;align-items:center;gap:12px;height:90px;width:100%;">'
            f'<img src="data:image/png;base64,{img_b64}" alt="icon" style="width: 68px; height: 68px; object-fit: contain; flex-shrink: 0; margin-left: -8px;">'
            '<div style="display:flex;flex-direction:column;align-items:flex-start;justify-content:center;min-width:0;">'
                '<div class="kpi-title" style="margin-bottom:3px;">Tenure</div>'
                f'<div class="kpi-value-large" style="font-size:24px;line-height:1;">{dominant_pct}%</div>'
                f'<div class="kpi-subtitle" style="margin-top:5px;">{dominant_label}</div>'
            '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_kategori_nasabah_kpi(df):
    col = "Kategori Nasabah"
    label_col = "kategori_nasabah_label"
    required_columns = {col, label_col}
    if df is None or df.empty or not required_columns.issubset(df.columns):
        render_empty_kpi()
        return

    total         = len(df)
    counts        = df[col].value_counts()
    dominant_code = counts.idxmax()
    dominant_label = df.loc[df[col] == dominant_code, label_col].iloc[0]
    dominant_pct   = round((counts[dominant_code] / total) * 100, 1)
    normalized_label = str(dominant_label).strip()
    display_label = CUSTOMER_TYPE_TRANSLATION.get(
        normalized_label.lower(),
        normalized_label,
    )
    img_b64 = get_image_base64("assets/type.png")

    html = (
        '<div style="display:flex;align-items:center;gap:12px;height:90px;width:100%;">'
            f'<img src="data:image/png;base64,{img_b64}" alt="icon" style="width: 68px; height: 68px; object-fit: contain; flex-shrink: 0; margin-left: -8px;">'
            '<div style="display:flex;flex-direction:column;align-items:flex-start;justify-content:center;min-width:0;">'
                '<div class="kpi-title" style="margin-bottom:3px;">Customer Type</div>'
                f'<div class="kpi-value-large" style="font-size:24px;line-height:1;">{dominant_pct}%</div>'
                f'<div class="kpi-subtitle" style="margin-top:5px;">{display_label}</div>'
            '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

def render_saving_rate_kpi(df):
    if df is None or df.empty:
        render_empty_kpi()
        return
    from helpers.loader import calculate_avg_saving_rate
    saving_rate = calculate_avg_saving_rate(df)

    rate_class = "saving-positive" if saving_rate >= 0 else "saving-negative"
    img_b64 = get_image_base64("assets/saving.png")

    html = (
        '<div style="display:flex;align-items:center;gap:12px;height:90px;width:100%;">'
            f'<img src="data:image/png;base64,{img_b64}" alt="icon" style="width: 68px; height: 68px; object-fit: contain; flex-shrink: 0; margin-left: -8px;">'
            '<div style="display:flex;flex-direction:column;align-items:flex-start;justify-content:center;min-width:0;">'
                '<div class="kpi-title" style="margin-bottom:3px;">Avg. Saving Rate</div>'
                f'<div class="kpi-value-large {rate_class}" style="font-size:24px;line-height:1;">{saving_rate}%</div>'
                '<div class="kpi-subtitle" style="margin-top:5px;">Of monthly income</div>'
            '</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)