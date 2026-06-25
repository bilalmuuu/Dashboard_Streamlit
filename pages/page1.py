import streamlit as st
import pandas as pd


from components.sidebar import apply_global_filters

from components.kpi_cards import (
    render_total_respondents_kpi,
    render_usia_kpi,
    render_tenure_kpi,
    render_kategori_nasabah_kpi,
    render_saving_rate_kpi
)

from components.profile_chart import (
    render_gender_age_chart,
    create_transaction_frequency_chart,
    create_income_treemap,
    create_multibanking_profile_chart,
    create_geomap_distribution
)

from components.persona_card import render_persona_dashboard


@st.cache_data
def get_exploded_data(data):
    df_expl = data.copy()
    target_col = "Apa Tujuan Anda Pertama Kali Membuka Rekening Di Bank Xyz"

    if target_col not in df_expl.columns:
        df_expl['Pilar_Motif'] = "Other"
        return df_expl

    # KAMUS TRANSLATOR KODE ANGKA KE TEKS (Berdasarkan Metadata Anda)
    tujuan_dict = {
        1: 'sebagai syarat ketika mengambil kredit',
        2: 'sebagai syarat ketika mengambil kredit;untuk melakukan transaksi finansial saya sehari-hari',
        3: 'sebagai syarat ketika mengambil kredit;untuk melakukan transaksi finansial saya sehari-hari;untuk menerima gaji dari tempat saya bekerja',
        4: 'sebagai syarat ketika mengambil kredit;untuk melakukan transaksi finansial saya sehari-hari;untuk menunjang bisnis saya',
        5: 'sebagai syarat ketika mengambil kredit;untuk menerima gaji dari tempat saya bekerja',
        6: 'sebagai syarat ketika mengambil kredit;untuk menunjang bisnis saya',
        7: 'untuk melakukan transaksi finansial saya sehari-hari',
        8: 'untuk melakukan transaksi finansial saya sehari-hari;lainnya',
        9: 'untuk melakukan transaksi finansial saya sehari-hari;untuk menerima gaji dari tempat saya bekerja',
        10: 'untuk melakukan transaksi finansial saya sehari-hari;untuk menunjang bisnis saya',
        11: 'untuk melakukan transaksi finansial saya sehari-hari;untuk menunjang bisnis saya;untuk menerima gaji dari tempat saya bekerja',
        12: 'untuk menabung',
        13: 'untuk menabung;lainnya',
        14: 'untuk menabung;sebagai syarat ketika mengambil kredit',
        15: 'untuk menabung;sebagai syarat ketika mengambil kredit;untuk melakukan transaksi finansial saya sehari-hari',
        16: 'untuk menabung;sebagai syarat ketika mengambil kredit;untuk melakukan transaksi finansial saya sehari-hari;untuk menerima gaji dari tempat saya bekerja',
        17: 'untuk menabung;sebagai syarat ketika mengambil kredit;untuk melakukan transaksi finansial saya sehari-hari;untuk menerima gaji dari tempat saya bekerja;lainnya',
        18: 'untuk menabung;sebagai syarat ketika mengambil kredit;untuk melakukan transaksi finansial saya sehari-hari;untuk menunjang bisnis saya',
        19: 'untuk menabung;sebagai syarat ketika mengambil kredit;untuk melakukan transaksi finansial saya sehari-hari;untuk menunjang bisnis saya;untuk menerima gaji dari tempat saya bekerja',
        20: 'untuk menabung;sebagai syarat ketika mengambil kredit;untuk menerima gaji dari tempat saya bekerja',
        21: 'untuk menabung;sebagai syarat ketika mengambil kredit;untuk menunjang bisnis saya',
        22: 'untuk menabung;sebagai syarat ketika mengambil kredit;untuk menunjang bisnis saya;untuk menerima gaji dari tempat saya bekerja',
        23: 'untuk menabung;untuk melakukan transaksi finansial saya sehari-hari',
        24: 'untuk menabung;untuk melakukan transaksi finansial saya sehari-hari;lainnya',
        25: 'untuk menabung;untuk melakukan transaksi finansial saya sehari-hari;untuk menerima gaji dari tempat saya bekerja',
        26: 'untuk menabung;untuk melakukan transaksi finansial saya sehari-hari;untuk menunjang bisnis saya',
        27: 'untuk menabung;untuk melakukan transaksi finansial saya sehari-hari;untuk menunjang bisnis saya;lainnya',
        28: 'untuk menabung;untuk melakukan transaksi finansial saya sehari-hari;untuk menunjang bisnis saya;untuk menerima gaji dari tempat saya bekerja',
        29: 'untuk menabung;untuk menerima gaji dari tempat saya bekerja',
        30: 'untuk menabung;untuk menerima gaji dari tempat saya bekerja;lainnya',
        31: 'untuk menabung;untuk menunjang bisnis saya',
        32: 'untuk menabung;untuk menunjang bisnis saya;lainnya', 33: 'untuk menabung;untuk menunjang bisnis saya;untuk menerima gaji dari tempat saya bekerja',
        34: 'untuk menerima gaji dari tempat saya bekerja',
        35: 'untuk menerima gaji dari tempat saya bekerja;lainnya',
        36: 'untuk menunjang bisnis saya',
        37: 'untuk menunjang bisnis saya;lainnya',
        38: 'untuk menunjang bisnis saya;untuk menerima gaji dari tempat saya bekerja'
    }

    def parse_pillars(val):
        if pd.isna(val):
            return ["Other"]

        # 1. Terjemahkan angka ke teks (Jika gagal, asumsikan sudah berupa teks)
        try:
            val_num = int(val)
            val_str = tujuan_dict.get(val_num, str(val)).lower()
        except ValueError:
            val_str = str(val).lower()

        # 2. Lakukan pencarian 6 Pilar Utama
        pillars = []
        if "menabung" in val_str: pillars.append("Saving")
        if "gaji" in val_str: pillars.append("Income Stream")
        if "transaksi" in val_str or "sehari-hari" in val_str: pillars.append("Daily Spending")
        if "bisnis" in val_str: pillars.append("Business Cashflow")
        if "kredit" in val_str or "pinjaman" in val_str: pillars.append("Financing Access")

        # Jika menjawab lainnya, ATAU tidak ada keyword yang cocok sama sekali
        if "lainnya" in val_str or not pillars:
            pillars.append("General Needs")

        # Hilangkan pilar duplikat menggunakan set()
        return list(set(pillars))

    # Aplikasikan fungsi dan pecah (explode) baris ganda
    df_expl['Pilar_Motif'] = df_expl[target_col].apply(parse_pillars)
    df_exploded_final = df_expl.explode('Pilar_Motif')

    return df_exploded_final

def render_page(source_df: pd.DataFrame) -> None:
    """Render the Respondent Profile page using the shared application dataframe."""
    df = apply_global_filters(source_df.copy())

    if df.empty:
        st.warning(
            "No respondents match the currently selected sidebar filters. "
            "Reset or adjust the filters to display this page."
        )
        return

    df_exploded = get_exploded_data(df)


    ##################################################################
    # PAGE TITLE
    ##################################################################

    st.title("Respondent Profile")
    st.caption(
        "Demographic, financial, behavioral, geographic, and persona overview of Bank XYZ respondents."
    )

    st.markdown(
        "<div style='height:8px;'></div>",
        unsafe_allow_html=True,
    )

    ##################################################################
    # ROW 1 — KPI CARDS
    ##################################################################

    kpi_cols = st.columns(5, gap="medium")

    with kpi_cols[0]:
        with st.container(key="card_kpi_1"):
            render_total_respondents_kpi(df)

    with kpi_cols[1]:
        with st.container(key="card_kpi_2"):
            render_usia_kpi(df)

    with kpi_cols[2]:
        with st.container(key="card_kpi_3"):
            render_tenure_kpi(df)

    with kpi_cols[3]:
        with st.container(key="card_kpi_4"):
            render_kategori_nasabah_kpi(df)

    with kpi_cols[4]:
        with st.container(key="card_kpi_5"):
            render_saving_rate_kpi(df)

    st.markdown(
        "<div style='height:18px;'></div>",
        unsafe_allow_html=True
    )

    ##################################################################
    # ROW 2 — FULL WIDTH GEOMAP
    ##################################################################

    with st.container(key="geomap_card"):
        create_geomap_distribution(df)

    st.markdown(
        "<div style='height:18px;'></div>",
        unsafe_allow_html=True
    )

    ##################################################################
    # ROW 3 — LARGE CONTAINERS
    ##################################################################

    row3_col1, row3_col2 = st.columns(2, gap="large")

    with row3_col1:
        with st.container(key="large_card_1"):
            render_gender_age_chart(df)

    with row3_col2:
        with st.container(key="large_card_2"):
            create_income_treemap(df)

    st.markdown(
        "<div style='height:18px;'></div>",
        unsafe_allow_html=True
    )

    ##################################################################
    # ROW 4 — MEDIUM CONTAINERS
    ##################################################################

    row4_col1, row4_col2 = st.columns(2, gap="large")

    with row4_col1:
        with st.container(key="medium_card_1"):
            create_transaction_frequency_chart(df)

    with row4_col2:
        with st.container(key="medium_card_2"):
            create_multibanking_profile_chart(df)

    # ---------------------------------------------------------------------------
    # 4. INTERACTIVE BUBBLE CLUSTER & PERSONA MAPPING
    # ---------------------------------------------------------------------------
    # Render the interactive persona segmentation and customer-motivation view.
    render_persona_dashboard(df_exploded)


# Transitional compatibility for Streamlit's current st.Page execution.
# Once app.py directly imports and calls render_page(), this block can be removed.
if __name__ == "__main__":
    shared_df = st.session_state.get("cx_source_df")
    if shared_df is None:
        st.error("Shared application data is unavailable. Start the dashboard from app.py.")
    else:
        render_page(shared_df)