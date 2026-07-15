import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from mappings import ( ADMISSION_TYPE, DISCHARGE_DISPOSITION, ADMISSION_SOURCE, AGE_ORDER, MEDICATION_COLUMNS, READMIT_ORDER, READMIT_LABELS,)
from style import ( inject_css, section_title, insight, COLOR_SEQUENCE, GENDER_COLOR_MAP,)

st.set_page_config(  page_title="Diabetic Patient Healthcare Analysis", page_icon="🩺", layout="wide",)

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
page = st.sidebar.radio(
    "Go to",  [ "🏠 Home", "🔍 Exploratory Data Analysis", "🏥 Hospital & Clinical Insights","💊 Medication Analysis", "🔄 Readmission Analysis", "📊 Interactive Dashboard", ], )

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This project analyzes 100,000+ diabetic patient hospital encounters "
    "to uncover patterns in demographics, treatment, and readmission.")

if page == "🏠 Home":
    st.title("🩺 Diabetic Patient Healthcare Analysis")
    st.caption("An end-to-end exploratory analysis of diabetic patient hospital encounters — demographics, clinical utilization, medications, and readmission patterns.")
    st.markdown("---")

    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
    with metric_col1:
        st.metric(label="Total Encounters", value=f"{len(df):,}")
    with metric_col2:
        st.metric(label="Unique Patients", value=f"{df['Patient_ID'].nunique():,}")
    with metric_col3:
        st.metric(label="Avg Hospital Stay", value=f"{df['Hospital_Stay'].mean():.1f} days")
    with metric_col4:
        st.metric(label="Readmitted <30 Days", value=f"{(df['readmitted'] == '<30').mean() * 100:.1f}%")
    with metric_col5:
        st.metric(label="On Diabetes Medication", value=f"{(df['diabetesMed'] == 'Yes').mean() * 100:.1f}%")

    st.write("")
    section_title("Project Overview")
    st.write(
        "This dashboard explores a real-world clinical dataset of diabetic patient encounters "
        "across 130 US hospitals. The goal is purely analytical — understanding who the patients "
        "are, how they are treated, and how often they return to the hospital, without building "
        "any predictive model."
    )

    left, right = st.columns([1.3, 1])
    with left:
        section_title("Dataset")
        st.dataframe(df.drop(columns=["age"]).assign(age=df["age"].astype(str)).head(12), use_container_width=True)
    with right:
        section_title("Column Groups")
        st.markdown(
            """
            - **Identifiers**: Encounter_ID, Patient_ID
            - **Demographics**: race, gender, age
            - **Admission Details**: admission_type, discharge_disposition, admission_source
            - **Clinical Utilization**: Hospital_Stay, Lab_Procedures, Procedures, Medications,
              Outpatient/Emergency/Inpatient Visits
            - **Diagnoses**: diag_1, diag_2, diag_3, Diagnoses
            - **Medications (23 drugs)**: metformin, insulin, glipizide, etc.
            - **Outcome**: readmitted
            """
        )

    section_title("Column Data Types & Missing Values")
    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": [df[c].nunique() for c in df.columns],
    })
    st.dataframe(info_df, use_container_width=True, height=300)


elif page == "🔍 Exploratory Data Analysis":
    st.title("🔍 Exploratory Data Analysis")
    st.caption("Understanding the patient population — age, gender, and race distribution.")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Age & Gender", "Race Distribution"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Patient Count by Age Group")
            age_counts = df["age"].value_counts().sort_index()
            st.bar_chart(age_counts)
            
        with col2:
            st.markdown("#### Gender Distribution")
            fig, ax = plt.subplots(figsize=(6, 5))
            gender_counts = df["gender"].value_counts()
            ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90, colors=['#0F9D8C', '#38BDF8'])
            ax.axis('equal')
            st.pyplot(fig)

        st.markdown("#### Age Distribution Split by Gender")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.countplot(data=df, x="age", hue="gender", palette="crest", ax=ax)
        ax.set_xlabel("Age Group")
        ax.set_ylabel("Number of Encounters")
        st.pyplot(fig)

        insight("Most encounters come from patients aged 50–80, indicating diabetes-related "
                "hospital visits are concentrated in middle-aged to elderly populations.")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Patient Count by Race")
            race_counts = df["race"].value_counts()
            st.bar_chart(race_counts)
            
        with col2:
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.barplot(y=df["race"].value_counts().index, x=df["race"].value_counts().values, palette="crest", ax=ax)
            ax.set_xlabel("Number of Encounters")
            ax.set_ylabel("")
            ax.set_title("Race Distribution")
            st.pyplot(fig)


elif page == "🏥 Hospital & Clinical Insights":
    st.title("🏥 Hospital & Clinical Insights")
    st.caption("Admissions, hospital stay duration, procedures, and diagnoses patterns.")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Admission Patterns", "Hospital Stay & Details", "Correlations"])

    with tab1:
        st.markdown("#### Admission Type Distribution")
        st.bar_chart(df["admission_type"].value_counts())

        st.markdown("#### Top 10 Admission Sources")
        st.bar_chart(df["admission_source"].value_counts().head(10))

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(df, x="Hospital_Stay", bins=15, color="#0F9D8C", kde=True, ax=ax)
            ax.set_title("Hospital Stay Duration Distribution")
            ax.set_xlabel("Days in Hospital")
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.boxplot(data=df, x="age", y="Hospital_Stay", palette="crest", ax=ax)
            ax.set_title("Hospital Stay by Age Group")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.markdown("#### Average Prior Visits by Type")
        visits_summary = df[["Outpatient_Visits", "Emergency_Visits", "Inpatient_Visits"]].mean()
        st.bar_chart(visits_summary)

        insight("A large majority of patients have zero prior outpatient/emergency/inpatient visits, "
                "so average counts stay low even though a small subset of patients drive frequent visits.")

    with tab3:
        numeric_cols = ["Hospital_Stay", "Lab_Procedures", "Procedures", "Medications",
                        "Outpatient_Visits", "Emergency_Visits", "Inpatient_Visits", "Diagnoses"]
        corr = df[numeric_cols].corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="crest", ax=ax, linewidths=0.5)
        ax.set_title("Correlation Heatmap of Clinical Numeric Features")
        st.pyplot(fig)

        insight("Lab Procedures, Medications, and Hospital Stay show the strongest positive "
                "relationships, suggesting longer admissions involve more tests and prescriptions.")


elif page == "💊 Medication Analysis":
    st.title("💊 Medication Analysis")
    st.caption("How diabetes medications are prescribed, adjusted, and used across patients.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Patients Prescribed Diabetes Medication")
        fig, ax = plt.subplots(figsize=(6, 5))
        med_counts = df["diabetesMed"].value_counts()
        ax.pie(med_counts, labels=med_counts.index, autopct='%1.1f%%', startangle=90, colors=['#0F9D8C', '#A855F7'])
        st.pyplot(fig)
    with col2:
        st.markdown("#### Medication Change During Encounter")
        fig, ax = plt.subplots(figsize=(6, 5))
        change_counts = df["change"].value_counts()
        ax.pie(change_counts, labels=change_counts.index, autopct='%1.1f%%', startangle=90, colors=['#38BDF8', '#F97316'])
        st.pyplot(fig)

    st.markdown("#### Top 12 Most Prescribed Diabetes Medications (%)")
    prevalence = {}
    for drug in MEDICATION_COLUMNS:
        prevalence[drug] = (df[drug] != "No").mean() * 100
    prevalence_df = pd.Series(prevalence).sort_values(ascending=False).head(12)
    st.bar_chart(prevalence_df)

    st.markdown("#### Insulin Usage Across Age Groups")
    fig, ax = plt.subplots(figsize=(10, 5))
    insulin_pivot = pd.crosstab(df["age"], df["insulin"])
    insulin_pivot.plot(kind="bar", stacked=True, ax=ax, colormap="crest")
    ax.set_title("Insulin Status by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Number of Encounters")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    insight("Insulin is the most frequently adjusted medication, with usage rising sharply "
            "after age 40 and remaining high through the elderly population.")


elif page == "🔄 Readmission Analysis":
    st.title("🔄 Readmission Analysis")
    st.caption("Examining which factors relate to patients returning to the hospital.")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Overall Readmission Distribution")
        fig, ax = plt.subplots(figsize=(6, 5))
        rcounts = df["readmitted_label"].value_counts()
        ax.pie(rcounts, labels=rcounts.index, autopct='%1.1f%%', startangle=90, colors=['#0F9D8C', '#38BDF8', '#F97316'])
        st.pyplot(fig)
    with col2:
        st.markdown("#### Readmission Count by Age Group")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x="age", hue="readmitted", order=AGE_ORDER, palette="crest", ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    st.markdown("#### Clinical Utilization Metrics vs Readmission Status")
    
    # ✅ Fixed: Subplots dimensions and alignment are completely fixed now
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    sns.boxplot(data=df, x="readmitted", y="Hospital_Stay", order=READMIT_ORDER, palette="crest", ax=ax[0])
    ax[0].set_title("Hospital Stay vs Readmission")
    
    sns.boxplot(data=df, x="readmitted", y="Lab_Procedures", order=READMIT_ORDER, palette="crest", ax=ax[1])
    ax[1].set_title("Lab Procedures vs Readmission")
    st.pyplot(fig)

    insight("Patients readmitted within 30 days tend to have longer hospital stays and more "
            "medications on average, hinting these encounters involve more complex cases.")


elif page == "📊 Interactive Dashboard":
    st.title("📊 Interactive Dashboard")
    st.caption("Filter the dataset live and explore patterns dynamically.")
    st.markdown("---")

    with st.expander("🔧 Filters", expanded=True):
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            genders = st.multiselect("Gender", sorted(df["gender"].unique()), default=list(df["gender"].unique()))
        with f2:
            races = st.multiselect("Race", sorted(df["race"].unique()), default=list(df["race"].unique()))
        with f3:
            age_groups = st.multiselect("Age Group", AGE_ORDER, default=AGE_ORDER)
        with f4:
            admission_types = st.multiselect(
                "Admission Type", sorted(df["admission_type"].unique()),
                default=list(df["admission_type"].unique())
            )

    selected_ages = [str(a) for a in age_groups]
    filtered = df[
        df["gender"].isin(genders)
        & df["race"].isin(races)
        & df["age"].isin(selected_ages)
        & df["admission_type"].isin(admission_types)
    ]

    if filtered.empty:
        st.warning("No records match the selected filters. Please adjust your selection.")
    else:
        dash_col1, dash_col2, dash_col3, dash_col4 = st.columns(4)
        with dash_col1:
            st.metric(label="Filtered Encounters", value=f"{len(filtered):,}")
        with dash_col2:
            st.metric(label="Avg Hospital Stay", value=f"{filtered['Hospital_Stay'].mean():.1f} days")
        with dash_col3:
            st.metric(label="Readmitted <30 Days", value=f"{(filtered['readmitted'] == '<30').mean() * 100:.1f}%")
        with dash_col4:
            st.metric(label="Avg Medications", value=f"{filtered['Medications'].mean():.1f}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Age Group Breakdown(Filtered)")
            st.bar_chart(filtered["age"].value_counts())
        with col2:
            st.markdown("#### Hospital Stay Distribution(Filtered)")
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(filtered, x="Hospital_Stay", bins=15, color="#0F9D8C", ax=ax)
            st.pyplot(fig)

        section_title("Data Table")
        display_df = filtered.drop(columns=["age"]).assign(age=filtered["age"].astype(str))
        st.dataframe(display_df.head(500), use_container_width=True, height=350)

        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Filtered Data as CSV", data=csv,
                           file_name="filtered_diabetic_data.csv", mime="text/csv")
