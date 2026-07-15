import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

/* Main global text formatting - Dark text style for clean visibility */
html, body, p, span, li, label {
    font-family: 'Inter', sans-serif;
    color: #1E293B !important;
}

/* Base App background */
.stApp {
    background: linear-gradient(180deg, #F4FBFA 0%, #EAF7F5 100%);
}

/* Sidebar styling keeping white text inside dark background */
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

/* Fixed Hero Section with custom light styling for proper visibility */
.app-hero {
    background: linear-gradient(120deg, #E0F2FE 0%, #CFFAFE 45%, #BAE6FD 100%) !important;
    padding: 34px 40px;
    border-radius: 22px;
    box-shadow: 0 12px 30px rgba(15, 157, 140, 0.1);
    margin-bottom: 26px;
    border-left: 8px solid #0F9D8C;
}

.app-hero h1 {
    font-family: 'Poppins', sans-serif;
    font-size: 2.1rem;
    margin-bottom: 6px;
    font-weight: 700;
    color: #0B4F4A !important;
}

.app-hero p {
    font-size: 1.02rem;
    color: #334155 !important;
    margin: 0;
}

/* Content Headings & Markdown Fix */
.section-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    color: #0B4F4A !important;
    font-size: 1.5rem;
    border-left: 6px solid #0F9D8C;
    padding-left: 14px;
    margin: 18px 0 14px 0;
}

/* Table and column headers fix to keep it black */
h1, h2, h3, h4, h5, h6 {
    color: #0B4F4A !important;
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
    color: #0F9D8C !important;
}

.metric-label {
    font-size: 0.85rem;
    color: #4B6B68 !important;
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
    color: #0B2E33 !important;
}

div.stButton > button {
    background-color: #0F9D8C;
    color: white !important;
    border-radius: 10px;
    border: none;
}

div.stButton > button:hover {
    background-color: #0B4F4A;
    color: white !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #E4F5F2;
    border-radius: 10px 10px 0 0;
    padding: 8px 16px;
    color: #0B4F4A !important;
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
