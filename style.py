import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

/* Main global text formatting */
html, body, p, span, li, label {
    font-family: 'Inter', sans-serif;
    color: #1E293B !important;
}

/* Base App background */
.stApp {
    background: linear-gradient(180deg, #F4FBFA 0%, #EAF7F5 100%);
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B4F4A 0%, #0F9D8C 100%);
}

section[data-testid="stSidebar"] * {
    color: #F4FBFA !important;
}

/* Expander background fix */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border-radius: 12px;
    border: 1px solid #DFF3F0;
}

[data-testid="stExpander"] [data-testid="stText"] {
    color: #0B4F4A !important;
    font-weight: 600;
}

/* Hero Section */
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
    font-weight: 700;
    color: #0B4F4A !important;
}

/* Section Titles */
.section-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    color: #0B4F4A !important;
    font-size: 1.5rem;
    border-left: 6px solid #0F9D8C;
    padding-left: 14px;
    margin: 18px 0 14px 0;
}

/* Metric Cards */
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

.insight-box {
    background: #FFFFFF;
    border-left: 5px solid #38BDF8;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 10px 0;
    color: #0B2E33 !important;
}

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>
"""

def inject_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)
