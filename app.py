import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from mappings import (ADMISSION_TYPE, DISCHARGE_DISPOSITION, ADMISSION_SOURCE, AGE_ORDER, MEDICATION_COLUMNS, READMIT_ORDER, READMIT_LABELS)
from style import (inject_css, section_title, insight, COLOR_SEQUENCE, GENDER_COLOR_MAP)

st.set_page_config(page_title="Diabetic Patient Healthcare Analysis", page_icon="🩺", layout="wide")

inject_css()
sns.set_theme(style="whitegrid", palette="crest")

def load_data():
    df = pd.read_csv("cleaned_diabetic_data.csv")
    df["age"] = pd.Categorical(df["age"], categories=AGE_ORDER, ordered=True)
    df["admission_type"] = df["admission_type_id"].map(ADMISSION_TYPE).fillna("Unknown")
    df["discharge_disposition"] = df["discharge_disposition_id"].map(DISCHARGE_DISPOSITION).fillna("Unknown")
    df["admission_source"] = df["admission_source_id"].map(ADMISSION_SOURCE).fillna("Unknown")
    df["readmitted_label"] = df["readmitted"].map(READMIT_LABELS)
    return df

df = load_data()

st.sidebar.markdown("## 🩺 Sidebar")
page = st.sidebar.radio("Go to", ["🏠 Home", "🔍 Exploratory Data Analysis", "🏥 Hospital & Clinical Insights", "💊 Medication Analysis", "🔄 Readmission Analysis", "📊 Interactive Dashboard"])

if page == "🏠 Home":
    st.title("🩺 Diabetic Patient Healthcare Analysis")
    st.markdown("---")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Encounters", f"{len(df):,}")
    m2.metric("Unique Patients", f"{df['Patient_ID'].nunique():,}")
    m3.metric("Avg Hospital Stay", f"{df['Hospital_Stay'].mean():.1f} days")
    m4.metric("Readmitted <30 Days", f"{(df['readmitted'] == '<30').mean() * 100:.1f}%")
    m5.metric("On Diabetes Medication", f"{(df['diabetesMed'] == 'Yes').mean() * 100:.1f}%")

elif page == "🔍 Exploratory Data Analysis":
    st.title("🔍 Exploratory Data Analysis")
    tab1, tab2 = st.tabs(["Age & Gender", "Race Distribution"])
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Patient Count by Age Group")
            st.bar_chart(df["age"].value_counts().sort_index())
        with c2:
            st.markdown("#### Gender Distribution")
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(df["gender"].value_counts(), labels=df["gender"].value_counts().index, autopct='%1.1f%%', colors=['#0F9D8C', '#38BDF8'])
            st.pyplot(fig)
            plt.close()
        st.markdown("#### Age Distribution Split by Gender")
        fig, ax = plt.subplots(figsize=(7, 3.5))
        sns.countplot(data=df, x="age", hue="gender", palette="crest", ax=ax)
        st.pyplot(fig)
        plt.close()
        insight("Most encounters come from patients aged 50–80.")
    with tab2:
        st.markdown("#### Patient Count by Race")
        st.bar_chart(df["race"].value_counts())

elif page == "🏥 Hospital & Clinical Insights":
    st.title("🏥 Hospital & Clinical Insights")
    st.markdown("#### Hospital Stay Duration")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df, x="Hospital_Stay", bins=15, color="#0F9D8C", kde=True, ax=ax)
    st.pyplot(fig)
    plt.close()

elif page == "💊 Medication Analysis":
    st.title("💊 Medication Analysis")
    st.write("Medication prescribing patterns across the dataset.")

elif page == "🔄 Readmission Analysis":
    st.title("🔄 Readmission Analysis")
    st.write("Analyzing factors contributing to hospital readmission.")

elif page == "📊 Interactive Dashboard":
    st.title("📊 Interactive Dashboard")
    with st.expander("🔧 Filters", expanded=True):
        f1, f2 = st.columns(2)
        genders = f1.multiselect("Gender", df["gender"].unique(), default=df["gender"].unique())
        races = f2.multiselect("Race", df["race"].unique(), default=df["race"].unique())
    filtered = df[df["gender"].isin(genders) & df["race"].isin(races)]
    st.dataframe(filtered.head(500), use_container_width=True)
