import pandas as pd

def process_rekening_pillars(df, target_col):
    """
    Fungsi untuk melakukan parsing dan explode pada kolom Tujuan Buka Rekening.
    Junior: Gunakan fungsi ini setelah memuat dataset utama!
    """
    if target_col not in df.columns:
        return df
        
    def map_to_pillars(text):
        if pd.isna(text): return ["Other"]
        text_lower = str(text).lower()
        pillars = []
        
        if "menabung" in text_lower: pillars.append("Saving")
        if "gaji" in text_lower: pillars.append("Salary Receipt")
        if "transaksi" in text_lower or "sehari-hari" in text_lower: pillars.append("Daily Transactions")
        if "bisnis" in text_lower: pillars.append("Business Needs")
        if "kredit" in text_lower or "pinjaman" in text_lower: pillars.append("Loan Requirement")
        if "lainnya" in text_lower: pillars.append("Other")
            
        return pillars if len(pillars) > 0 else ["Other"]

    # Mapping dan Explode
    df['Pilar_Motif'] = df[target_col].apply(map_to_pillars)
    df_exploded = df.explode('Pilar_Motif')
    
    return df_exploded