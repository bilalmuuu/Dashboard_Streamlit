import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# --- FUNCTION 1: CALCULATE PERSONA DATA ---
def calculate_dynamic_persona(df_filtered, pillar_name):

    pillar_name_str = str(pillar_name).strip()
    pillar_df = df_filtered[
        df_filtered['Pilar_Motif'].astype(str).str.strip() == pillar_name_str
    ]

    if pillar_df.empty:
        return None

    # ==========================================================
    # FUNCTION DOMINANT CATEGORY
    # ==========================================================
    def get_dominant_category(col_name):

        if col_name not in pillar_df.columns:
            return None, 0, 0

        series = pillar_df[col_name].dropna()

        if series.empty:
            return None, 0, 0

        vc = series.value_counts()

        max_count = vc.max()

        candidates = vc[vc == max_count].index.tolist()

        # If there is a tie, use the highest code.
        dominant_value = max(candidates)

        dominant_count = max_count

        dominant_pct = round(
            dominant_count / len(pillar_df) * 100,
            1
        )

        return dominant_value, dominant_count, dominant_pct

    # ==========================================================
    # MAPPING
    # ==========================================================
    gender_map = {
        1: "Male",
        2: "Female"
    }

    usia_map = {
        1: "17–19 years",
        2: "20–25 years",
        3: "26–30 years",
        4: "31–35 years",
        5: "36–40 years",
        6: "41–45 years",
        7: "46–50 years",
        8: "Above 50 years"
    }

    pendidikan_map = {
        1: "Diploma / Associate Degree",
        2: "Doctorate (PhD)",
        3: "Master's Degree",
        4: "Bachelor's Degree",
        5: "Primary School",
        6: "Senior High School",
        7: "Junior High School"
    }

    pekerjaan_map = {
        1: "Doctor",
        2: "Private-Sector Teacher",
        3: "Homemaker",
        4: "Student",
        5: "Civil Servant (Non-Teacher)",
        6: "Civil Servant (Teacher)",
        7: "Private-Sector Employee",
        8: "Lawyer / Advocate / Notary",
        9: "Retiree",
        10: "Village Official",
        11: "Police / Military",
        12: "Currently Unemployed",
        13: "Contract / Honorary Worker",
        14: "Entrepreneur / Business Owner / Trader"
    }

    pengeluaran_map = {
        1: "Rp 4,500,000–Rp 6,000,000",
        2: "Rp 6,000,001–Rp 7,500,000",
        3: "Rp 7,500,001–Rp 9,000,000",
        4: "Rp 9,000,001–Rp 10,500,000",
        5: "Rp 10,500,001–Rp 15,000,000",
        6: "Rp 15,000,001–Rp 20,000,000",
        7: "Rp 20,000,001–Rp 25,000,000",
        8: "Above Rp 25,000,000",
        9: "Rp 3,000,001–Rp 4,500,000",
        10: "Rp 2,000,001–Rp 3,000,000",
        11: "Rp 1,500,001–Rp 2,000,000",
        12: "Rp 1,000,001–Rp 1,500,000"
    }

    pendapatan_map = {
        1: "Above Rp 25,000,000",
        2: "Prefer not to answer",
        3: "Rp 10,500,001–Rp 15,000,000",
        4: "Rp 15,000,001–Rp 20,000,000",
        5: "Rp 20,000,001–Rp 25,000,000",
        6: "Rp 6,000,001–Rp 7,500,000",
        7: "Rp 7,500,001–Rp 9,000,000",
        8: "Rp 9,000,001–Rp 10,500,000",
        9: "Rp 1,000,001–Rp 1,500,000",
        10: "Rp 1,500,001–Rp 2,000,000",
        11: "Rp 2,000,001–Rp 3,000,000",
        12: "Rp 3,000,001–Rp 4,500,000",
        13: "Rp 4,500,000–Rp 6,000,000"
    }

    # ==========================================================
    # GET DOMINANT VALUES
    # ==========================================================
    gender_val, gender_count, gender_pct = get_dominant_category(
        'Jenis Kelamin'
    )

    usia_val, usia_count, usia_pct = get_dominant_category(
        'Range Usia'
    )

    pendidikan_val, pendidikan_count, pendidikan_pct = get_dominant_category(
        'Pendidikan'
    )

    pekerjaan_val, pekerjaan_count, pekerjaan_pct = get_dominant_category(
        'Pekerjaan'
    )

    pendapatan_val, pendapatan_count, pendapatan_pct = get_dominant_category(
        'Rata Rata Penghasilan Rumah Tangga Per Bulannya'
    )

    pengeluaran_val, pengeluaran_count, pengeluaran_pct = get_dominant_category(
        'Rata Rata Pengeluaran Rutin Per Bulannya'
    )

    return {

        "volume": len(pillar_df),

        "gender_text": gender_map.get(
            gender_val,
            "Unknown"
        ),
        "gender_pct": gender_pct,

        "usia": usia_map.get(
            usia_val,
            "Unknown"
        ),
        "usia_pct": usia_pct,

        "pendidikan": pendidikan_map.get(
            pendidikan_val,
            "Unknown"
        ),
        "pendidikan_pct": pendidikan_pct,

        "pekerjaan": pekerjaan_map.get(
            pekerjaan_val,
            "Unknown"
        ),
        "pekerjaan_pct": pekerjaan_pct,

        "pendapatan": pendapatan_map.get(
            pendapatan_val,
            "Unknown"
        ),
        "pendapatan_pct": pendapatan_pct,

        "pengeluaran": pengeluaran_map.get(
            pengeluaran_val,
            "Unknown"
        ),
        "pengeluaran_pct": pengeluaran_pct
    }


# --- FUNCTION 2: RENDER PERSONA DASHBOARD ---
def render_persona_dashboard(df_exploded):
    st.markdown("""
    <div style="font-size:20px; font-weight:800; color:#1D2433; margin-bottom:5px;">
        Interactive Persona Mapping
    </div>
    <div style="font-size:14px; color:#6a738b; margin-bottom:20px;">
        <b>Select a motivation bubble</b> below to view the dominant customer socio-demographic profile.
    </div>
    """, unsafe_allow_html=True)

    pillar_volumes = df_exploded['Pilar_Motif'].value_counts().reset_index()
    pillar_volumes.columns = ['Pilar', 'Volume']

    default_pillar = pillar_volumes['Pilar'].iloc[0] if not pillar_volumes.empty else "Saving"
    selected_pillar = default_pillar

    # CRITICAL FIX: robust session-state handling for chart selections
    if "bubble_click" in st.session_state:
        event = st.session_state.bubble_click
        try:
            # Validate the returned event structure before reading the selected point.
            if hasattr(event, "__contains__") and "selection" in event:
                sel = event["selection"]
                if hasattr(sel, "__contains__") and "points" in sel:
                    points = sel["points"]
                    if isinstance(points, list) and len(points) > 0:
                        cd = points[0].get("customdata")
                        if cd is not None:
                            # Plotly may return customdata as a list; use its first value.
                            selected_pillar = cd[0] if isinstance(cd, list) else cd
        except Exception:
            pass  # Ignore malformed browser events and retain the default pillar.

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        with st.container(key="p1_card_bubble"):
            st.markdown("<div style='font-weight:800; font-size:16px; color:#1D2433; margin-bottom:10px;'>Motivation Pillar Clusters (Clickable)</div>", unsafe_allow_html=True)

            N = len(pillar_volumes)
            angles = np.linspace(0, 2*np.pi, N, endpoint=False)
            fig = go.Figure()

            RADIUS = 1.5

            for i, row in pillar_volumes.iterrows():
                # Spread the bubbles evenly around the center.
                x_pos = np.cos(angles[i]) * RADIUS
                y_pos = np.sin(angles[i]) * RADIUS

                marker_size = (row['Volume'] / pillar_volumes['Volume'].max()) * 90
                marker_size = max(40, marker_size)

                is_selected = (str(row['Pilar']).strip() == str(selected_pillar).strip())

                bubble_color = "#bb2649" if is_selected else "#e2e8f0"
                bubble_opacity = 1.0 if is_selected else 0.6
                font_color = "#ffffff" if is_selected else "#64748b"

                fig.add_trace(go.Scatter(
                    x=[x_pos], y=[y_pos],
                    mode="markers+text",
                    text=[f"<b>{row['Pilar']}</b><br>N={row['Volume']}"],
                    textposition="top center",
                    textfont=dict(color=font_color),
                    customdata=[row['Pilar']],
                    marker=dict(size=marker_size, color=bubble_color, line=dict(width=3 if is_selected else 1, color="#ffffff"), opacity=bubble_opacity),
                    name=row['Pilar'],
                    hovertemplate=f"<b>{row['Pilar']}</b><br>Click to view persona details<extra></extra>"
                ))

            # Expand the axis range so outer bubbles are not clipped.
            fig.update_layout(
                height=263,
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2.5, 2.5]),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-2.5, 2.5]),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=0, b=0),
                clickmode='event+select'
            )

            try:
                st.plotly_chart(fig, width="stretch", config={"displayModeBar": False}, on_select="rerun", key="bubble_click")
            except TypeError:
                st.warning("Interactive chart selection is not supported by this Streamlit version. Run `pip install --upgrade streamlit` in the terminal.")
                st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    with col_right:
        with st.container(key="p1_card_persona"):
            persona_data = calculate_dynamic_persona(df_exploded, selected_pillar)

            if persona_data:
                is_female = persona_data['gender_text'].lower() == 'female'
                icon = "👩‍💼" if is_female else "👨‍💼"
                theme_color = "#bb2649"

                # Header and primary identity
                html_header = (
                    '<div style="display:flex;align-items:center;justify-content:space-between;'
                    'border-bottom:2px solid #f0f0f0;padding-bottom:10px;margin-bottom:15px;">'
                    '<div style="font-size:16px;font-weight:800;color:#1D2433;">Dominant Persona Profile</div>'
                    f'<div style="background-color:#ffeef0;color:#bb2649;padding:4px 10px;'
                    f'border-radius:12px;font-size:12px;font-weight:700;">{selected_pillar}</div>'
                    '</div>'
                )

                html_identity = (
                    '<div style="display:flex;gap:15px;align-items:flex-start;">'
                    f'<div style="font-size:60px;line-height:1;">{icon}</div>'
                    '<div>'
                    f'<div style="font-size:20px;font-weight:800;color:{theme_color};">'
                    f'{persona_data["gender_text"]} ({persona_data["gender_pct"]}%)'
                    f'</div>'
                    f'<div style="font-size:14px;color:#1D2433;font-weight:600;">'
                    f'Age: <span style="color:#6a738b;">{persona_data["usia"]} ({persona_data["usia_pct"]}%)</span>'
                    f'</div>'
                    f'<div style="font-size:13px;color:#6a738b;">Volume: <b>{persona_data["volume"]} customers</b></div>'
                    '</div>'
                    '</div>'
                )

                # Socio-demographic details
                html_socio = (
                    '<div style="margin-top:16px;padding-top:15px;">'
                    '<div style="font-size:12px;font-weight:700;color:#98A1B3;'
                    'text-transform:uppercase;margin-bottom:8px;">Dominant Socio-Demographics</div>'
                    '<div style="background-color:#fcfdff;border:1px solid #e9ecef;'
                    'border-radius:8px;padding:15px;font-size:13px;color:#4b4f5d;line-height:1.8;">'
                    f'🎓 <b>Education:</b> {persona_data["pendidikan"]} ({persona_data["pendidikan_pct"]}%)<br>'
                    f'💼 <b>Occupation:</b> {persona_data["pekerjaan"]} ({persona_data["pekerjaan_pct"]}%)<br>'
                    f'💰 <b>Income:</b> {persona_data["pendapatan"]} ({persona_data["pendapatan_pct"]}%)<br>'
                    f'🛒 <b>Monthly Expenditure:</b> {persona_data["pengeluaran"]} ({persona_data["pengeluaran_pct"]}%)'
                    '</div>'
                    '</div>'
                )

                # Main card wrapper and render
                html_card = (
                    '<div style="display:flex;flex-direction:column;min-height:300px;">'
                    + html_header
                    + html_identity
                    + html_socio
                    + '</div>'
                )
                st.markdown(html_card, unsafe_allow_html=True)

            else:
                html_empty = (
                    '<div style="display:flex;flex-direction:column;align-items:center;'
                    'justify-content:center;min-height:300px;text-align:center;">'
                    '<span style="font-size:50px;color:#cccccc;">👤</span>'
                    '<div style="color:#98A1B3;font-weight:600;margin-top:10px;">Persona data is unavailable.</div>'
                    '</div>'
                )
                st.markdown(html_empty, unsafe_allow_html=True)