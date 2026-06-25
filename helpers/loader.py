"""
data/loader.py
==============
Shared data loading & decoding untuk Bank XYZ Dashboard.
Menggunakan data_encoded - Sheet1 (1).csv + metadata_kategori.xlsx.
Semua decode dilakukan secara dinamis dari metadata — tidak ada hardcode map.
"""

import pandas as pd
import streamlit as st
import re

# ──────────────────────────────────────────────────────────────────────────────
# PATH CONFIG
# ──────────────────────────────────────────────────────────────────────────────

DATA_PATH     = "data/data_encoded.csv"
METADATA_PATH = "data/metadata_kategori.xlsx"


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 1: RAW LOAD
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_raw_data() -> pd.DataFrame:
    """Load CSV mentah tanpa transformasi apapun."""
    return pd.read_csv(DATA_PATH)


@st.cache_data(show_spinner=False)
def load_metadata() -> pd.DataFrame:
    """
    Load metadata dari Sheet1 (2) — kolom: kolom_asal, kategori_asli, kode_numerik.
    Sheet1 (2) dipakai karena tidak memiliki kolom keterangan ekstra
    dan format kode_numerik lebih bersih (int, bukan float).
    """
    meta = pd.read_excel(METADATA_PATH, sheet_name="Sheet1 (2)")
    meta["kolom_asal"] = (
        meta["kolom_asal"]
        .ffill()
        .astype(str)
        .str.strip()
    )
    return meta


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 2: BUILD MAPPING DICT DARI METADATA
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def build_metadata_mapping() -> dict:
    """
    Bangun dictionary { nama_kolom_asli: { kode_int: label_string } }
    dari metadata. Digunakan untuk decode semua kolom kategorikal.
    """
    meta = load_metadata()
    mapping_dict = {}

    for col_name in meta["kolom_asal"].unique():
        temp = meta[meta["kolom_asal"] == col_name]
        mapping_dict[col_name] = dict(
            zip(temp["kode_numerik"], temp["kategori_asli"])
        )

    return mapping_dict


# ──────────────────────────────────────────────────────────────────────────────
# LAYER 3: LOAD + DECODE + ENRICH
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Load data lengkap dengan:
    1. Decode semua kolom kategorikal dari metadata → kolom *_label
    2. Kolom tambahan: cabang_label, nps_xyz_class, nps_kompetitor_class
    3. Kolom shorthand untuk kolom yang sering dipakai di dashboard

    Fungsi ini dipanggil sekali oleh app.py dan hasilnya dibagikan ke setiap page.
    """
    df           = load_raw_data().copy()
    mapping_dict = build_metadata_mapping()

    # ── Decode semua kolom yang ada di metadata ──────────────────────────────
    for col_name, decoder in mapping_dict.items():
        if col_name in df.columns:
            # Nama kolom label: snake_case dari nama kolom asli
            label_col = (
                col_name.lower()
                .replace(" ", "_")
                .replace("-", "_")
            )
            df[f"{label_col}_label"] = df[col_name].map(decoder)

    # ── Kolom shorthand (untuk kemudahan akses di page) ──────────────────────
    df["provinsi_label"] = (
        df["provinsi_label"] if "provinsi_label" in df.columns else None
    )

    df["gender_label"] = (
        df["jenis_kelamin_label"]
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

    df["usia_label"] = (
        df["range_usia_label"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({
            "17 - 19 tahun": "17–19 Years",
            "17-19 tahun": "17–19 Years",
            "17 -19 tahun": "17–19 Years",
            "20 - 25 tahun": "20–25 Years",
            "20-25 tahun": "20–25 Years",
            "26 - 30 tahun": "26–30 Years",
            "26-30 tahun": "26–30 Years",
            "31 - 35 tahun": "31–35 Years",
            "31-35 tahun": "31–35 Years",
            "36 - 40 tahun": "36–40 Years",
            "36-40 tahun": "36–40 Years",
            "41 - 45 tahun": "41–45 Years",
            "41-45 tahun": "41–45 Years",
            "46 - 50 tahun": "46–50 Years",
            "46-50 tahun": "46–50 Years",
            "50 tahun dan ke atas": "Above 50 Years",
            "50 tahun ke atas": "Above 50 Years",
            "di atas 50 tahun": "Above 50 Years",
        })
    )

    df["tenure_label"] = (
        df["sudah_berapa_lamakah_menjadi_nasabah_bank_xyz_label"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({
            "kurang dari 1 tahun": "Less than 1 year",
            "di bawah 1 tahun": "Less than 1 year",
            "dibawah 1 tahun": "Less than 1 year",
            "< 1 tahun": "Less than 1 year",
            "1 tahun": "1 year",
            "1 - 2 tahun": "1–2 years",
            "1-2 tahun": "1–2 years",
            "2 - 3 tahun": "2–3 years",
            "2-3 tahun": "2–3 years",
            "3 - 5 tahun": "3–5 years",
            "3-5 tahun": "3–5 years",
            "4 - 5 tahun": "4–5 years",
            "4-5 tahun": "4–5 years",
            "5 - 10 tahun": "5–10 years",
            "5-10 tahun": "5–10 years",
            "5 tahun atau lebih": "5 years or more",
            "5 tahun atau lebih ": "5 years or more",
            "5 tahun ke atas": "5 years or more",
            "lebih dari 5 tahun": "More than 5 years",
            "> 5 tahun": "More than 5 years",
            "lebih dari 10 tahun": "More than 10 years",
            "10 tahun ke atas": "More than 10 years",
            "> 10 tahun": "More than 10 years",
            "less than 1 year": "Less than 1 year",
            "1 year": "1 year",
            "1–2 years": "1–2 years",
            "2–3 years": "2–3 years",
            "3–5 years": "3–5 years",
            "4–5 years": "4–5 years",
            "5–10 years": "5–10 years",
            "5 years or more": "5 years or more",
            "more than 5 years": "More than 5 years",
            "more than 10 years": "More than 10 years",
        })
    )
    df["panel_label"] = df["panel_transaksi_label"]
    df["pekerjaan_label"] = (
        df["pekerjaan_label"] if "pekerjaan_label" in df.columns else None
    )
    df["pendidikan_label"] = (
        df["pendidikan_label"] if "pendidikan_label" in df.columns else None
    )
    df["ses_pengeluaran_label"] = df[
        "rata_rata_pengeluaran_rutin_per_bulannya_label"
    ]
    df["ses_penghasilan_label"] = df[
        "rata_rata_penghasilan_rumah_tangga_per_bulannya_label"
    ]

    if "kategori_nasabah_label" in df.columns:
        df["kategori_nasabah_label"] = (
            df["kategori_nasabah_label"]
            .astype("string")
            .str.strip()
            .str.lower()
            .replace({
                "nasabah prioritas": "Priority Customer",
                "nasabah reguler": "Regular Customer",
                "nasabah tabungan xyz reguler": "Regular Bank XYZ Savings Customer",
                "nasabah tabungan bank xyz reguler": "Regular Bank XYZ Savings Customer",
                "priority customer": "Priority Customer",
                "regular customer": "Regular Customer",
            })
        )

    # ── Cabang: title case dari kolom string ─────────────────────────────────
    df["cabang_label"] = df["Nama Kantor Cabang"].str.title()

    # ── NPS Classification ───────────────────────────────────────────────────
    def classify_nps(score):
        if score >= 9:
            return "Promoter"
        elif score >= 7:
            return "Passive"
        else:
            return "Detractor"

    df["nps_xyz_class"]        = df["Nps Bank Xyz"].apply(classify_nps)
    df["nps_kompetitor_class"] = df["Nps Bank Kompetitor"].apply(classify_nps)

    return df


# ──────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

def compute_nps(df: pd.DataFrame, col_class: str) -> float:
    """
    Hitung Net Promoter Score dari kolom klasifikasi
    (nps_xyz_class atau nps_kompetitor_class).
    """
    if df is None or df.empty:
        return 0.0
    total      = len(df)
    promoters  = (df[col_class] == "Promoter").sum()
    detractors = (df[col_class] == "Detractor").sum()
    return round(((promoters - detractors) / total) * 100, 1)


def compute_nps_from_scores(df: pd.DataFrame, col: str) -> float:
    """Hitung NPS langsung dari kolom skor 0–10."""
    if df is None or df.empty:
        return 0.0
    total      = len(df)
    promoters  = (df[col] >= 9).sum()
    detractors = (df[col] <= 6).sum()
    return round(((promoters - detractors) / total) * 100, 1)


def calculate_bank_xyz_usage(df: pd.DataFrame) -> dict:
    """
    Hitung % nasabah yang menjadikan Bank XYZ sebagai:
    - Rekening utama simpanan (kode 10)
    - Rekening utama transaksi (kode 7)
    """
    if df is None or df.empty:
        return {"deposit_pct": 0, "transaction_pct": 0}

    deposit_col     = "Bank Manakah Yang Merupakan Rekening Utama Untuk Bapak Ibu Menyimpan Dana"
    transaction_col = "Bank Manakah Yang Merupakan Rekening Utama Untuk Bapak Ibu Bertransaksi Belanja Transfer Dsb"

    total = len(df)

    deposit_pct     = round((df[deposit_col]     == 10).sum() / total * 100, 1)
    transaction_pct = round((df[transaction_col] ==  7).sum() / total * 100, 1)

    return {
        "deposit_pct":     deposit_pct,
        "transaction_pct": transaction_pct,
    }


def calculate_avg_saving_rate(df: pd.DataFrame) -> float:
    """
    Menghitung rata-rata Saving Rate = (Surplus / Penghasilan) * 100%
    Mengekstrak angka numerik dari teks kategori rentang penghasilan/pengeluaran.
    """
    if df is None or df.empty:
        return 0.0

    def extract_median(text):
        if pd.isna(text) or not isinstance(text, str):
            return 0
        # Bersihkan titik, temukan semua deretan angka
        numbers = re.findall(r'\d+', text.replace('.', ''))
        # Hanya ambil angka yang memiliki panjang > 5 digit (mengabaikan kode seperti 'A1', 'A1.1')
        valid_nums = [int(n) for n in numbers if len(n) >= 5]
        
        if len(valid_nums) >= 2:
            return (valid_nums[0] + valid_nums[1]) / 2 # Ambil rata-rata batas bawah & batas atas
        elif len(valid_nums) == 1:
            return valid_nums[0]
        return 0

    df_calc = df.dropna(subset=['ses_pengeluaran_label', 'ses_penghasilan_label']).copy()
    
    # Konversi string ke angka
    df_calc['pengeluaran_num'] = df_calc['ses_pengeluaran_label'].apply(extract_median)
    df_calc['penghasilan_num'] = df_calc['ses_penghasilan_label'].apply(extract_median)

    # Filter hanya yang memiliki penghasilan dan pengeluaran valid (>0)
    df_calc = df_calc[(df_calc['penghasilan_num'] > 0) & (df_calc['pengeluaran_num'] > 0)]

    if df_calc.empty:
        return 0.0

    # Hitung Saving Rate
    df_calc['surplus'] = df_calc['penghasilan_num'] - df_calc['pengeluaran_num']
    # Jika surplus negatif (lebih besar pasak dari tiang), rate-nya akan negatif. Ini valid untuk bisnis.
    df_calc['saving_rate'] = (df_calc['surplus'] / df_calc['penghasilan_num']) * 100

    return round(df_calc['saving_rate'].mean(), 1)