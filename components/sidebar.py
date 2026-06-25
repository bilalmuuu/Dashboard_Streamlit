

"""
Shared navigation and persistent global filters for the Bank XYZ CX Dashboard.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st


FILTER_PREFIX = "cx_sidebar_"
APPLIED_FILTER_KEY = f"{FILTER_PREFIX}applied_filters"
INITIALIZED_KEY = f"{FILTER_PREFIX}initialized"
CURRENT_PAGE_KEY = "cx_current_page"
DEFAULT_PAGE = "respondent_profile"

COLUMN_CANDIDATES = {
    "province": ["provinsi_label", "Provinsi"],
    "branch": ["cabang_label", "Nama Kantor Cabang"],
    "gender": ["gender_label", "jenis_kelamin_label", "Jenis Kelamin"],
    "age": ["usia_label", "range_usia_label", "Range Usia"],
    "customer_type": ["kategori_nasabah_label", "Kategori Nasabah"],
}

FILTER_LABELS = {
    "province": "Province",
    "branch": "Branch Office",
    "gender": "Gender",
    "age": "Age Group",
    "customer_type": "Customer Type",
}

SIDEBAR_CSS = """
<style>
[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 0% 0%, rgba(187,38,73,.09), transparent 30%),
        linear-gradient(180deg, #FFFFFF 0%, #FFF7FA 100%) !important;
    border-right: 1px solid rgba(29,36,51,.06) !important;
    min-width: 17.25rem !important;
    max-width: 17.25rem !important;
    box-shadow: 8px 0 30px rgba(29,36,51,.035) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: .4rem !important;
}

[data-testid="stSidebarContent"] {
    padding-left: .85rem !important;
    padding-right: .85rem !important;
}

[data-testid="stSidebarUserContent"] {
    padding-bottom: .75rem !important;
    overflow-x: hidden !important;
}

.cx-brand-card {
    position: relative;
    overflow: hidden;
    padding: 13px 13px 12px 13px;
    margin: 0 0 9px 0;
    border-radius: 15px;
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF1F5 100%);
    border: 1px solid rgba(187,38,73,.12);
    box-shadow: 0 8px 20px rgba(29,36,51,.05);
}

.cx-brand-card::after {
    content: "";
    position: absolute;
    width: 76px;
    height: 76px;
    border-radius: 50%;
    right: -30px;
    top: -32px;
    background: linear-gradient(135deg, rgba(243,93,116,.20), rgba(187,38,73,.14));
}

.cx-brand-row {
    display: flex;
    align-items: center;
    gap: 10px;
    position: relative;
    z-index: 1;
}

.cx-brand-icon {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 11px;
    color: #FFFFFF;
    font-size: 19px;
    background: linear-gradient(145deg, #F35D74 0%, #BB2649 100%);
    box-shadow: 0 7px 15px rgba(187,38,73,.22);
}

.cx-brand-title {
    color: #1D2433;
    font-size: 16px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -.3px;
}

.cx-brand-subtitle {
    margin-top: 2px;
    color: #6A738B;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: .01em;
}

.cx-sidebar-section {
    display: flex;
    align-items: center;
    gap: 7px;
    margin: 10px 2px 6px 2px;
    color: #1D2433;
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .09em;
}

.cx-sidebar-section::after {
    content: "";
    height: 1px;
    flex: 1;
    background: linear-gradient(90deg, rgba(29,36,51,.10), transparent);
}

[data-testid="stSidebar"] details {
    background: rgba(255,255,255,.86) !important;
    border: 1px solid rgba(29,36,51,.07) !important;
    border-radius: 13px !important;
    box-shadow: 0 7px 18px rgba(29,36,51,.04) !important;
}

[data-testid="stSidebar"] details summary {
    padding: 8px 10px !important;
    font-size: 11px !important;
    font-weight: 800 !important;
    color: #1D2433 !important;
}

[data-testid="stSidebar"] [data-testid="stForm"] {
    background: transparent !important;
    border: 0 !important;
    padding: 4px 1px 2px 1px !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] .stMultiSelect label {
    color: #4B4F5D !important;
    font-size: 9px !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: .06em !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    min-height: 35px !important;
    border-radius: 9px !important;
    border-color: rgba(29,36,51,.10) !important;
    background: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
    border-color: #BB2649 !important;
    box-shadow: 0 0 0 2px rgba(187,38,73,.12) !important;
}

[data-testid="stSidebar"] .stButton button,
[data-testid="stSidebar"] .stFormSubmitButton button {
    width: 100% !important;
    min-height: 36px !important;
    border-radius: 9px !important;
    font-weight: 800 !important;
    font-size: 11px !important;
}

[data-testid="stSidebar"] .stFormSubmitButton button {
    border: 1px solid #FFC3D4 !important;
    color: #BB2649 !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF0F4 100%) !important;
    box-shadow: 0 5px 12px rgba(187,38,73,.11) !important;
}

[data-testid="stSidebar"] .stFormSubmitButton button:hover {
    color: #FFFFFF !important;
    background: linear-gradient(135deg, #F35D74 0%, #BB2649 100%) !important;
    border-color: #BB2649 !important;
    box-shadow: 0 7px 16px rgba(187,38,73,.20) !important;
    transform: translateY(-1px);
}

[data-testid="stSidebar"] .stButton button {
    color: #5E6677 !important;
    background: #FFFFFF !important;
    border: 1px solid rgba(29,36,51,.11) !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    color: #BB2649 !important;
    border-color: #FFC3D4 !important;
    background: #FFF0F4 !important;
}

.cx-filter-summary {
    margin-top: 7px;
    padding: 8px 9px;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(187,38,73,.08), rgba(243,93,116,.05));
    border: 1px solid rgba(187,38,73,.10);
}

.cx-filter-summary-title {
    color: #1D2433;
    font-size: 10px;
    font-weight: 800;
}

.cx-filter-summary-text {
    margin-top: 2px;
    color: #6A738B;
    font-size: 9px;
    line-height: 1.35;
}

.cx-sidebar-footer {
    margin-top: 9px;
    padding: 8px 4px 0 4px;
    border-top: 1px solid rgba(29,36,51,.07);
    color: #98A1B3;
    font-size: 9px;
    line-height: 1.35;
    text-align: center;
}

.cx-status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 5px;
    background: #2FBF71;
    box-shadow: 0 0 0 3px rgba(47,191,113,.12);
}

/* --- Session-state navigation buttons --- */
[data-testid="stSidebar"] div[data-testid="stButton"] {
    margin-bottom: 4px;
}
[data-testid="stSidebar"] div[data-testid="stButton"]:has(button[kind="primary"]) button {
    color: #FFFFFF !important;
    background: linear-gradient(135deg, #F35D74 0%, #BB2649 100%) !important;
    border-color: #BB2649 !important;
    box-shadow: 0 7px 16px rgba(187,38,73,.20) !important;
    transform: none !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"]:has(button[kind="secondary"]) button {
    color: #5E6677 !important;
    background: transparent !important;
    border-color: rgba(187,38,73,.14) !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"]:has(button[kind="secondary"]) button:hover {
    color: #BB2649 !important;
    background: #FFF0F4 !important;
    border-color: #FFC3D4 !important;
    transform: translateX(2px);
}

[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"],
[data-testid="stSidebarResizer"] {
    display: none !important;
    width: 0 !important;
}
</style>
"""


def _first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for column in candidates:
        if column in df.columns:
            return column
    return None


def _clean_options(series: pd.Series) -> list[str]:
    values = series.dropna().astype(str).str.strip()
    values = values[values.ne("") & values.str.lower().ne("nan")]
    return sorted(values.unique().tolist(), key=str.casefold)


def _filter_definitions(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    definitions: dict[str, dict[str, Any]] = {}

    for filter_name, candidates in COLUMN_CANDIDATES.items():
        column = _first_existing_column(df, candidates)
        if column is None:
            continue

        options = _clean_options(df[column])
        if not options:
            continue

        definitions[filter_name] = {
            "label": FILTER_LABELS[filter_name],
            "column": column,
            "options": options,
        }

    return definitions


def _default_filters() -> dict[str, list[str]]:
    return {name: [] for name in COLUMN_CANDIDATES}


def _initialize_state() -> None:
    if INITIALIZED_KEY not in st.session_state:
        st.session_state[INITIALIZED_KEY] = True

    if APPLIED_FILTER_KEY not in st.session_state:
        st.session_state[APPLIED_FILTER_KEY] = _default_filters()

    if CURRENT_PAGE_KEY not in st.session_state:
        st.session_state[CURRENT_PAGE_KEY] = DEFAULT_PAGE


def _reset_filters() -> None:
    st.session_state[APPLIED_FILTER_KEY] = _default_filters()

    for filter_name in COLUMN_CANDIDATES:
        widget_key = f"{FILTER_PREFIX}widget_{filter_name}"
        if widget_key in st.session_state:
            st.session_state[widget_key] = []


def _navigate_to(page_name: str) -> None:
    st.session_state[CURRENT_PAGE_KEY] = page_name


def render_sidebar(df: pd.DataFrame | None = None) -> dict[str, list[str]]:
    """Render compact navigation and persistent filters."""
    _initialize_state()
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(
            """
            <div class="cx-brand-card">
                <div class="cx-brand-row">
                    <div class="cx-brand-icon">🏦</div>
                    <div>
                        <div class="cx-brand-title">Bank XYZ</div>
                        <div class="cx-brand-subtitle">Customer Experience Dashboard</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="cx-sidebar-section">Dashboard Navigation</div>',
            unsafe_allow_html=True,
        )

        current_page = st.session_state.get(CURRENT_PAGE_KEY, DEFAULT_PAGE)

        if st.button(
            "Respondent Profile",
            key="cx_nav_respondent_profile",
            icon=":material/groups:",
            type="primary" if current_page == "respondent_profile" else "secondary",
            width="stretch",
        ):
            _navigate_to("respondent_profile")
            st.rerun()

        if st.button(
            "Branch & Touchpoint Experience",
            key="cx_nav_bank_performance",
            icon=":material/account_balance:",
            type="primary" if current_page == "bank_performance" else "secondary",
            width="stretch",
        ):
            _navigate_to("bank_performance")
            st.rerun()

        if st.button(
            "Competitor Performance",
            key="cx_nav_competitor_performance",
            icon=":material/compare_arrows:",
            type="primary" if current_page == "competitor_performance" else "secondary",
            width="stretch",
        ):
            _navigate_to("competitor_performance")
            st.rerun()

        st.markdown(
            '<div class="cx-sidebar-section">Dashboard Filters</div>',
            unsafe_allow_html=True,
        )

        with st.expander("Configure Filters", expanded=False):
            if df is None or not isinstance(df, pd.DataFrame) or df.empty:
                st.info("Filters are unavailable because the dataset could not be loaded.")
            else:
                definitions = _filter_definitions(df)
                current_filters = st.session_state[APPLIED_FILTER_KEY]

                with st.form("cx_global_filter_form", clear_on_submit=False):
                    pending_filters: dict[str, list[str]] = {}

                    for filter_name, definition in definitions.items():
                        widget_key = f"{FILTER_PREFIX}widget_{filter_name}"
                        existing = current_filters.get(filter_name, [])
                        safe_existing = [
                            value
                            for value in existing
                            if value in definition["options"]
                        ]

                        if widget_key not in st.session_state:
                            st.session_state[widget_key] = safe_existing

                        pending_filters[filter_name] = st.multiselect(
                            definition["label"],
                            options=definition["options"],
                            key=widget_key,
                            placeholder=f"All {definition['label'].lower()}",
                        )

                    submitted = st.form_submit_button(
                        "Apply Filters",
                        width="stretch",
                    )

                    if submitted:
                        merged = _default_filters()
                        merged.update(pending_filters)
                        st.session_state[APPLIED_FILTER_KEY] = merged
                        st.rerun()

                st.button(
                    "Reset Filters",
                    key=f"{FILTER_PREFIX}reset_button",
                    on_click=_reset_filters,
                    width="stretch",
                )

        applied = st.session_state[APPLIED_FILTER_KEY]
        active = {
            name: values
            for name, values in applied.items()
            if values
        }

        if active:
            active_count = sum(len(values) for values in active.values())
            readable = []

            for name, values in active.items():
                label = FILTER_LABELS.get(name, name.replace("_", " ").title())
                shown = ", ".join(values[:2])
                if len(values) > 2:
                    shown += f" +{len(values) - 2}"
                readable.append(f"<b>{label}:</b> {shown}")

            st.markdown(
                f"""
                <div class="cx-filter-summary">
                    <div class="cx-filter-summary-title">
                        {active_count} filter selection(s) active
                    </div>
                    <div class="cx-filter-summary-text">
                        {'<br>'.join(readable)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="cx-filter-summary">
                    <div class="cx-filter-summary-title">All respondents included</div>
                    <div class="cx-filter-summary-text">
                        No global filter is currently restricting the dataset.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="cx-sidebar-footer">
                <span class="cx-status-dot"></span>
                Dataset connected<br>
                Bank XYZ CX Analytics
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state[APPLIED_FILTER_KEY]


def apply_global_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the persistent sidebar filters to a DataFrame."""
    if df is None:
        return pd.DataFrame()

    if not isinstance(df, pd.DataFrame):
        raise TypeError("apply_global_filters() expects a pandas DataFrame.")

    if df.empty:
        return df.copy()

    _initialize_state()
    filtered = df.copy()
    definitions = _filter_definitions(filtered)
    applied = st.session_state.get(APPLIED_FILTER_KEY, {})

    for filter_name, selected_values in applied.items():
        if not selected_values:
            continue

        definition = definitions.get(filter_name)
        if definition is None:
            continue

        column = definition["column"]
        if column not in filtered.columns:
            continue

        filtered = filtered[
            filtered[column]
            .astype(str)
            .str.strip()
            .isin(selected_values)
        ]

    return filtered.copy()


def get_active_filter_count() -> int:
    """Return the total number of selected filter values."""
    _initialize_state()
    applied = st.session_state.get(APPLIED_FILTER_KEY, {})
    return sum(len(values) for values in applied.values() if values)