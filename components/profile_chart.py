"""
=============================================================================
CUSTOMER PROFILE CHART COMPONENTS
Dashboard Visualization Module
=============================================================================
"""

import os
import json
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import folium
import branca.colormap as cm
from streamlit_folium import st_folium

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

# Semantic UI mapping
TEXT_PRIMARY = TEXT_100
TEXT_SECONDARY = TEXT_200
GRID_COLOR = BG_200
CARD_BG = BG_100
PAGE_BG = BG_200
BORDER_COLOR = BG_300

# ---------------------------------------------------------------------------
# 2. DEMOGRAPHIC PROFILE (STACKED BAR CHART)
# ---------------------------------------------------------------------------
def render_gender_age_chart(df):
    if df is None or df.empty:
        st.warning("No data available.")
        return

    required_cols = ["gender_label", "usia_label"]
    if any(col not in df.columns for col in required_cols):
        st.error("Missing columns for Demographic Chart.")
        return

    st.markdown(f"""
    <div style="font-size:15px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:4px;">
    Respondent Demographic Profile
    </div>
    <div style="font-size:12px;color:{TEXT_SECONDARY};margin-bottom:18px;">
    Distribution of respondents by age group and gender
    </div>
    """, unsafe_allow_html=True)

    chart_source = df.copy()

    chart_source["gender_label"] = (
        chart_source["gender_label"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({
            "pria": "Male",
            "laki-laki": "Male",
            "laki laki": "Male",
            "male": "Male",
            "wanita": "Female",
            "perempuan": "Female",
            "female": "Female",
        })
    )

    chart_source["usia_label"] = (
        chart_source["usia_label"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({
            "17 - 19 tahun": "17–19 Years",
            "17-19 tahun": "17–19 Years",
            "17 -19 tahun": "17–19 Years",
            "17–19 years": "17–19 Years",
            "20 - 25 tahun": "20–25 Years",
            "20-25 tahun": "20–25 Years",
            "20–25 years": "20–25 Years",
            "26 - 30 tahun": "26–30 Years",
            "26-30 tahun": "26–30 Years",
            "26–30 years": "26–30 Years",
            "31 - 35 tahun": "31–35 Years",
            "31-35 tahun": "31–35 Years",
            "31–35 years": "31–35 Years",
            "36 - 40 tahun": "36–40 Years",
            "36-40 tahun": "36–40 Years",
            "36–40 years": "36–40 Years",
            "41 - 45 tahun": "41–45 Years",
            "41-45 tahun": "41–45 Years",
            "41–45 years": "41–45 Years",
            "46 - 50 tahun": "46–50 Years",
            "46-50 tahun": "46–50 Years",
            "46–50 years": "46–50 Years",
            "50 tahun dan ke atas": "Above 50 Years",
            "50 tahun ke atas": "Above 50 Years",
            "di atas 50 tahun": "Above 50 Years",
            "above 50 years": "Above 50 Years",
        })
    )

    chart_df = (
        chart_source
        .groupby(["usia_label", "gender_label"])
        .size()
        .reset_index(name="count")
    )
    chart_df["pct"] = chart_df.groupby("usia_label")["count"].transform(
        lambda values: (values / values.sum()) * 100
    )

    pivot_df = chart_df.pivot(
        index="usia_label",
        columns="gender_label",
        values="pct",
    ).fillna(0)

    age_order = [
        "17–19 Years",
        "20–25 Years",
        "26–30 Years",
        "31–35 Years",
        "36–40 Years",
        "41–45 Years",
        "46–50 Years",
        "Above 50 Years",
    ]
    pivot_df = pivot_df.reindex(age_order).fillna(0)

    for column in ["Male", "Female"]:
        if column not in pivot_df.columns:
            pivot_df[column] = 0

    fig = go.Figure()

    # Male segment
    fig.add_trace(go.Bar(
        name="Male",
        y=pivot_df.index,
        x=pivot_df["Male"],
        orientation="h",
        marker=dict(color=PRIMARY_100),
        text=[f"{v:.0f}%" if v >= 8 else "" for v in pivot_df["Male"]],
        textposition="inside",
        textfont=dict(color=CARD_BG, size=11),
        hovertemplate="<b>Male</b><br>%{y}<br>%{x:.1f}%<extra></extra>"
    ))

    # Female segment
    fig.add_trace(go.Bar(
        name="Female",
        y=pivot_df.index,
        x=pivot_df["Female"],
        orientation="h",
        marker=dict(color=ACCENT_200),
        text=[f"{v:.0f}%" if v >= 8 else "" for v in pivot_df["Female"]],
        textposition="inside",
        textfont=dict(color=TEXT_PRIMARY, size=11),
        hovertemplate="<b>Female</b><br>%{y}<br>%{x:.1f}%<extra></extra>"
    ))

    fig.update_layout(
        barmode="stack",
        height=340,
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", y=1.12, x=0, font=dict(size=11, color=TEXT_SECONDARY)),
        xaxis=dict(range=[0, 100], ticksuffix="%", tickvals=[0, 25, 50, 75, 100], showgrid=True, gridcolor=GRID_COLOR, zeroline=False, tickfont=dict(size=11, color=TEXT_SECONDARY)),
        yaxis=dict(showgrid=False, tickfont=dict(size=11, color=TEXT_PRIMARY))
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# ---------------------------------------------------------------------------
# 3. TRANSACTION FREQUENCY (DONUT CHART)
# ---------------------------------------------------------------------------
def create_transaction_frequency_chart(df, freq_col="Seberapa Sering Melakukan Transaksi Dengan Bank Xyz Baik Secara Online Dengan Mobile Banking Atau Datang Ke Kantor Cabang Bank Xyz"):
    if df is None or df.empty or freq_col not in df.columns:
        st.warning("Data not available for Transaction Frequency.")
        return

    st.markdown(f"""
    <div style="font-size:15px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:4px;">
    Transaction Frequency
    </div>
    <div style="font-size:12px;color:{TEXT_SECONDARY};margin-bottom:18px;">
    Frequency of customer transactions with Bank XYZ
    </div>
    """, unsafe_allow_html=True)

    frequency_mapping = {1: "Monthly", 2: "2+ Times Weekly", 3: "Weekly", 4: "Biweekly"}

    chart_df = df.copy()
    chart_df[freq_col] = pd.to_numeric(chart_df[freq_col], errors="coerce")
    chart_df["frequency_label"] = chart_df[freq_col].map(frequency_mapping)
    chart_df = chart_df["frequency_label"].value_counts().reset_index()
    chart_df.columns = ["frequency", "count"]
    chart_df["pct"] = (chart_df["count"] / chart_df["count"].sum() * 100)

    # Use the original warm dashboard palette with readable label contrast.
    donut_colors = [PRIMARY_100, PRIMARY_200, ACCENT_100, ACCENT_200]
    donut_text_colors = [CARD_BG, CARD_BG, CARD_BG, TEXT_PRIMARY]

    fig = go.Figure(go.Pie(
        labels=chart_df["frequency"],
        values=chart_df["count"],
        hole=0.55,
        marker=dict(colors=donut_colors, line=dict(color=CARD_BG, width=2)),
        text=[f"{pct:.0f}%" if pct >= 5 else "" for pct in chart_df["pct"]],
        textinfo="text",
        textposition="inside",
        textfont=dict(color=donut_text_colors, size=11),
        hovertemplate="<b>%{label}</b><br>Respondents: %{value}<br>Percentage: %{percent}<br><extra></extra>"
    ))

    fig.update_layout(
        height=340, margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center", font=dict(size=11, color=TEXT_SECONDARY)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# ---------------------------------------------------------------------------
# 4. HOUSEHOLD INCOME DISTRIBUTION (TREEMAP)
# ---------------------------------------------------------------------------
def create_income_treemap(df, income_col="ses_penghasilan_label"):
    import pandas as pd
    import plotly.graph_objects as go
    import streamlit as st

    if df is None or df.empty or income_col not in df.columns:
        st.warning("Data not available for Income Distribution.")
        return

    # =========================
    # Header
    # =========================
    st.markdown(f"""
    <div style="font-size:15px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:4px;">
        Household Income Distribution
    </div>
    <div style="font-size:12px;color:{TEXT_SECONDARY};margin-bottom:18px;">
        Distribution of respondents by monthly household income
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # Income Mapping
    # =========================
    income_mapping = {
        "Rp. 1.000.001 - Rp. 1.500.000": "≤ Rp 3 Juta",
        "Rp. 1.500.001 - Rp. 2.000.000": "≤ Rp 3 Juta",
        "Rp. 2.000.001 - Rp. 3.000.000": "≤ Rp 3 Juta",
        "Rp. 3.000.001 - Rp. 4.500.000": "Rp 3–6 Juta",
        "Rp. 4.500.000 - Rp 6.000.000": "Rp 3–6 Juta",
        "Rp 6.000.001 - Rp 7.500.000": "Rp 6–10.5 Juta",
        "Rp 7.500.001- Rp 9.000.000": "Rp 6–10.5 Juta",
        "Rp 9.000.001- Rp 10.500.000": "Rp 6–10.5 Juta",
        "Rp 10.500.0001 - Rp 15.000.000": "Rp 10.5–15 Juta",
        "Rp 15.000.001- Rp 20.000.000": "Rp 15–20 Juta",
        "Rp 20.000.001 - Rp 25.000.000": "Rp 20–25 Juta",
        "Di atas Rp 25.000.000": "> Rp 25 Juta",
        "Menolak Memberikan Jawaban": "Tidak Menjawab"
    }

    chart_df = df.copy()

    chart_df["income_group"] = (
        chart_df[income_col]
        .map(income_mapping)
    )

    chart_df = (
        chart_df["income_group"]
        .value_counts()
        .reset_index()
    )

    chart_df.columns = ["income_group", "count"]

    chart_df["pct"] = (
        chart_df["count"]
        / chart_df["count"].sum()
        * 100
    ).round(1)

    # =========================
    # Custom Color Palette
    # =========================
    colors = [
        "#bb2649",
        "#c92f55",
        "#d9486a",
        "#e86b87",
        "#f08ea1",
        "#f6b0bc",
        "#ffd6a5",
        "#f3e5d0",
    ]
    chart_df["color"] = colors[:len(chart_df)]

    # =========================
    # Treemap
    # =========================
    fig = go.Figure(
        go.Treemap(
            labels=chart_df["income_group"],
            parents=[""] * len(chart_df),
            values=chart_df["count"],

            marker=dict(
                colors=chart_df["color"],
                line=dict(
                    width=2,
                    color="#FFFFFF"
                )
            ),

            text=[
                f"<b>{label}</b><br>{pct:.0f}%"
                for label, pct in zip(
                    chart_df["income_group"],
                    chart_df["pct"]
                )
            ],

            textinfo="text",

            textfont=dict(
                size=15,
                color="#FFFFFF"
            ),

            hovertemplate=
            "<b>%{label}</b><br>"
            "Respondents: %{value}<br>"
            "<extra></extra>",

            tiling=dict(
                pad=3
            ),

            root_color="rgba(0,0,0,0)"
        )
    )

    fig.update_layout(
        height=340,

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        uniformtext=dict(
            minsize=10,
            mode="hide"
        )
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False
        },
        theme=None
    )


# ---------------------------------------------------------------------------
# 5. MULTI BANKING PROFILE (STACKED BAR CHART)
# ---------------------------------------------------------------------------
def create_multibanking_profile_chart(df, bank_col="Bank Mana Saja Yang Saat Ini Masih Aktif Bapak Ibu Gunakan"):
    if df is None or df.empty or bank_col not in df.columns:
        st.warning("Data not available for Multi Banking Profile.")
        return

    st.markdown(f"""
    <div style="font-size:15px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:4px;">
    Multi Banking Profile
    </div>
    <div style="font-size:12px;color:{TEXT_SECONDARY};margin-bottom:18px;">
    Number of banks actively used by respondents
    </div>
    """, unsafe_allow_html=True)

    temp_df = df.copy()
    temp_df["bank_count"] = temp_df[bank_col].fillna("").astype(str).apply(
        lambda x: len([bank.strip() for bank in x.split(";") if bank.strip() != ""])
    )

    def banking_group(x):
        if x <= 1: return "1 Bank"
        elif x == 2: return "2 Bank"
        elif x == 3: return "3 Bank"
        else: return "4+ Bank"

    temp_df["banking_group"] = temp_df["bank_count"].apply(banking_group)
    chart_df = temp_df["banking_group"].value_counts().reset_index()
    chart_df.columns = ["segment", "count"]

    order = ["1 Bank", "2 Bank", "3 Bank", "4+ Bank"]
    chart_df["segment"] = pd.Categorical(chart_df["segment"], categories=order, ordered=True)
    chart_df = chart_df.sort_values("segment")
    chart_df["pct"] = (chart_df["count"] / chart_df["count"].sum() * 100)

    fig = go.Figure()
    bar_colors = [PRIMARY_100, PRIMARY_200, ACCENT_100, ACCENT_200]

    for idx, row in chart_df.iterrows():
        # Preserve readable contrast across the original warm palette.
        font_color = CARD_BG if idx < 3 else TEXT_PRIMARY
        fig.add_trace(go.Bar(
            y=[""], x=[row["pct"]], orientation="h", name=row["segment"],
            marker=dict(color=bar_colors[idx]),
            text=[f"{row['pct']:.0f}%" if row["pct"] >= 8 else ""],
            textposition="inside", textfont=dict(color=font_color, size=11),
            hovertemplate=f"<b>{row['segment']}</b><br>{row['pct']:.1f}%<extra></extra>"
        ))

    fig.update_layout(
        barmode="stack", height=340, paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        margin=dict(l=0, r=0, t=10, b=30), showlegend=True,
        legend=dict(orientation="h", y=-0.20, x=0.5, xanchor="center", font=dict(size=11, color=TEXT_SECONDARY)),
        xaxis=dict(range=[0, 100], showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# ---------------------------------------------------------------------------
# 6. GEOGRAPHIC DISTRIBUTION (FOLIUM CHOROPLETH)
# ---------------------------------------------------------------------------
def create_geomap_distribution(df, city_col="Kab Kota"):
    if df is None or df.empty or city_col not in df.columns:
        st.warning("Data not available for Geographic Distribution.")
        return

    st.markdown(f"""
    <div style="font-size:15px;font-weight:700;color:{TEXT_PRIMARY};margin-bottom:4px;">
    Geographic Distribution
    </div>
    <div style="font-size:12px;color:{TEXT_SECONDARY};margin-bottom:18px;">
    Distribution of respondents across Indonesia
    </div>
    """, unsafe_allow_html=True)

    # Aggregate respondent counts
    map_df = df[city_col].dropna().astype(str).value_counts().reset_index()
    map_df.columns = ["city", "respondents"]

    # Normalize city and regency names
    map_df["city_clean"] = map_df["city"].str.upper()
    map_df["city_clean"] = map_df["city_clean"].str.replace("KABUPATEN ", "", regex=False)
    map_df["city_clean"] = map_df["city_clean"].str.replace("KAB. ", "", regex=False)
    map_df["city_clean"] = map_df["city_clean"].str.replace("KOTA ADMINISTRASI ", "", regex=False)
    map_df["city_clean"] = map_df["city_clean"].str.replace("KOTA ", "", regex=False)
    map_df["city_clean"] = map_df["city_clean"].str.strip().str.title()

    def format_city_name(nama_kota):
        if "Jakarta" in nama_kota:
            return f"Kota Administrasi {nama_kota}"
        kota_spesifik = ["Depok", "Tangerang Selatan", "Cilegon", "Cimahi"]
        if nama_kota in kota_spesifik:
            return f"Kota {nama_kota}"
        return nama_kota

    map_df["city_clean"] = map_df["city_clean"].apply(format_city_name)
    map_dict = dict(zip(map_df["city_clean"], map_df["respondents"]))

    # Load GeoJSON
    geojson_path = os.path.join("data", "Kabupaten_Indonesia.json")
    try:
        with open(geojson_path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        st.error(f"GeoJSON file not found. Expected location: {geojson_path}")
        return

    # Separate active and inactive geographic layers
    geojson_aktif = {"type": "FeatureCollection", "features": []}
    geojson_pasif = {"type": "FeatureCollection", "features": []}

    for feature in geojson_data['features']:
        city_name = feature['properties'].get('WADMKK', '')
        resp_count = map_dict.get(city_name, 0)
        feature['properties']['Jumlah_Responden'] = resp_count

        if resp_count > 0:
            geojson_aktif['features'].append(feature)
        else:
            geojson_pasif['features'].append(feature)

    # Colormap from light warm tones to deep maroon
    min_resp = map_df["respondents"].min() if not map_df.empty else 0
    max_resp = map_df["respondents"].max() if not map_df.empty else 1
    colormap = cm.LinearColormap(colors=[ACCENT_200, PRIMARY_200, PRIMARY_100], vmin=min_resp, vmax=max_resp)
    colormap.caption = "Respondents"

    # Initialize the map
    m = folium.Map(location=[-2.59, 118.04], zoom_start=4.5, tiles="CartoDB positron")

    # Inactive layer: neutral styling without hover
    if geojson_pasif['features']:
        folium.GeoJson(
            geojson_pasif,
            style_function=lambda x: {
                'fillColor': BG_200,
                'color': CARD_BG,
                'weight': 0.5,
                'fillOpacity': 1.0
            },
            tooltip=None
        ).add_to(m)

    # Active layer: blue gradient with hover details
    if geojson_aktif['features']:
        folium.GeoJson(
            geojson_aktif,
            style_function=lambda feature: {
                'fillColor': colormap(feature['properties']['Jumlah_Responden']),
                'color': CARD_BG,
                'weight': 1.0,
                'fillOpacity': 1.0
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['WADMKK', 'Jumlah_Responden'],
                aliases=["City/Regency:", "Respondents:"],
                localize=True,
                style="font-family: Inter, sans-serif; font-size: 13px;"
            )
        ).add_to(m)

    colormap.add_to(m)

    # Render in Streamlit
    st_folium(m, width="100%", height=450, returned_objects=[])