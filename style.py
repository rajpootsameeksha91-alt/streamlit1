import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #F4FBFA 0%, #EAF7F5 100%);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B4F4A 0%, #0F9D8C 100%);
}

section[data-testid="stSidebar"] * {
    color: #F4FBFA !important;
}

div[data-baseweb="radio"] label {
    background-color: rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 8px 10px;
    margin-bottom: 4px;
    transition: all 0.2s ease-in-out;
}

div[data-baseweb="radio"] label:hover {
    background-color: rgba(255,255,255,0.20);
}

.app-hero {
    background: linear-gradient(120deg, #0F9D8C 0%, #14B8A6 45%, #38BDF8 100%);
    padding: 34px 40px;
    border-radius: 22px;
    color: white;
    box-shadow: 0 12px 30px rgba(15, 157, 140, 0.25);
    margin-bottom: 26px;
}

.app-hero h1 {
    font-family: 'Poppins', sans-serif;
    font-size: 2.1rem;
    margin-bottom: 6px;
    font-weight: 700;
}

.app-hero p {
    font-size: 1.02rem;
    opacity: 0.95;
    margin: 0;
}

.section-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    color: #0B4F4A;
    font-size: 1.5rem;
    border-left: 6px solid #0F9D8C;
    padding-left: 14px;
    margin: 18px 0 14px 0;
}

.metric-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 6px 18px rgba(11, 79, 74, 0.08);
    border: 1px solid #DFF3F0;
    text-align: center;
}

.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #0F9D8C;
}

.metric-label {
    font-size: 0.85rem;
    color: #4B6B68;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 4px;
}

.insight-box {
    background: #FFFFFF;
    border-left: 5px solid #38BDF8;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(11, 79, 74, 0.06);
    color: #0B2E33;
}

div.stButton > button {
    background-color: #0F9D8C;
    color: white;
    border-radius: 10px;
    border: none;
}

div.stButton > button:hover {
    background-color: #0B4F4A;
    color: white;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #E4F5F2;
    border-radius: 10px 10px 0 0;
    padding: 8px 16px;
    color: #0B4F4A;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background-color: #0F9D8C !important;
    color: white !important;
}

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>
"""

PLOTLY_TEMPLATE = "plotly_white"

COLOR_SEQUENCE = [
    "#0F9D8C", "#38BDF8", "#F97316", "#A855F7", "#EF4444",
    "#14B8A6", "#FACC15", "#6366F1", "#EC4899", "#22C55E",
]

READMIT_COLOR_MAP = {
    "NO": "#0F9D8C",
    ">30": "#FACC15",
    "<30": "#EF4444",
}

GENDER_COLOR_MAP = {
    "Female": "#EC4899",
    "Male": "#38BDF8",
}


def inject_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def hero(title, subtitle):
    st.markdown(
        f'<div class="app-hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )


def kpi_card(label, value, col):
    col.markdown(
        f'<div class="metric-card"><div class="metric-value">{value}</div>'
        f'<div class="metric-label">{label}</div></div>',
        unsafe_allow_html=True,
    )


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)
