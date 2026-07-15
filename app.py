import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from mappings import (
    ADMISSION_TYPE, DISCHARGE_DISPOSITION, ADMISSION_SOURCE,
    AGE_ORDER, MEDICATION_COLUMNS, READMIT_ORDER, READMIT_LABELS,
)
from style import (
    inject_css, hero, kpi_card, section_title, insight,
    COLOR_SEQUENCE, READMIT_COLOR_MAP, GENDER_COLOR_MAP,
)

st.set_page_config(
    page_title="Diabetic Patient Healthcare Analysis",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
sns.set_theme(style="whitegrid", palette="crest")


@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_diabetic_data.csv")
    df["age"] = pd.Categorical(df["age"], categories=AGE_ORDER, ordered=True)
    df["admission_type"] = df["admission_type_id"].map(ADMISSION_TYPE).fillna("Unknown")
    df["discharge_disposition"] = df["discharge_disposition_id"].map(DISCHARGE_DISPOSITION).fillna("Unknown")
    df["admission_source"] = df["admission_source_id"].map(ADMISSION_SOURCE).fillna("Unknown")
    df["readmitted_label"] = df["readmitted"].map(READMIT_LABELS)
    return df


df = load_data()

st.sidebar.markdown("## 🩺 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "🔍 Exploratory Data Analysis",
        "🏥 Hospital & Clinical Insights",
        "💊 Medication Analysis",
        "🔄 Readmission Analysis",
        "📊 Interactive Dashboard",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This project analyzes 100,000+ diabetic patient hospital encounters "
    "to uncover patterns in demographics, treatment, and readmission."
)


if page == "🏠 Home":
    hero(
        "🩺 Diabetic Patient Healthcare Analysis",
        "An end-to-end exploratory analysis of diabetic patient hospital encounters — "
        "demographics, clinical utilization, medications, and readmission patterns.",
    )

    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card("Total Encounters", f"{len(df):,}", c1)
    kpi_card("Unique Patients", f"{df['Patient_ID'].nunique():,}", c2)
    kpi_card("Avg Hospital Stay", f"{df['Hospital_Stay'].mean():.1f} days", c3)
    kpi_card("Readmitted <30 Days", f"{(df['readmitted'] == '<30').mean() * 100:.1f}%", c4)
    kpi_card("On Diabetes Medication", f"{(df['diabetesMed'] == 'Yes').mean() * 100:.1f}%", c5)

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
        section_title("Dataset Snapshot")
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
    hero("🔍 Exploratory Data Analysis", "Understanding the patient population — age, gender, and race distribution.")

    tab1, tab2, tab3 = st.tabs(["Age & Gender", "Race", "Combined View"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            age_counts = df["age"].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.barplot(x=age_counts.index.astype(str), y=age_counts.values, palette="crest", ax=ax)
            ax.set_xlabel("Age Group")
            ax.set_ylabel("Number of Encounters")
            ax.set_title("Patient Count by Age Group")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        with col2:
            gender_counts = df["gender"].value_counts()
            fig, ax = plt.subplots(figsize=(6, 4.5))
            colors = [GENDER_COLOR_MAP.get(g, "#0F9D8C") for g in gender_counts.index]
            ax.pie(gender_counts.values, labels=gender_counts.index, autopct="%1.1f%%",
                   colors=colors, startangle=90)
            ax.set_title("Gender Distribution")
            st.pyplot(fig)

        age_gender = df.groupby(["age", "gender"], observed=True).size().reset_index(name="count")
        fig, ax = plt.subplots(figsize=(10, 4.5))
        sns.barplot(data=age_gender, x="age", y="count", hue="gender",
                    palette=GENDER_COLOR_MAP, ax=ax)
        ax.set_xlabel("Age Group")
        ax.set_ylabel("Number of Encounters")
        ax.set_title("Age Distribution Split by Gender")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        insight("Most encounters come from patients aged 50–80, indicating diabetes-related "
                "hospital visits are concentrated in middle-aged to elderly populations.")

    with tab2:
        col1, col2 = st.columns([1.3, 1])
        with col1:
            race_counts = df["race"].value_counts().reset_index()
            race_counts.columns = ["race", "count"]
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.barplot(y=race_counts["race"], x=race_counts["count"], palette="crest", ax=ax)
            ax.set_xlabel("Number of Encounters")
            ax.set_ylabel("")
            ax.set_title("Patient Count by Race")
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.pie(race_counts["count"], labels=race_counts["race"], autopct="%1.0f%%",
                   colors=COLOR_SEQUENCE, startangle=90)
            ax.set_title("Race Share")
            st.pyplot(fig)

        race_gender = df.groupby(["race", "gender"], observed=True).size().reset_index(name="count")
        race_gender_pivot = race_gender.pivot(index="race", columns="gender", values="count").fillna(0)
        fig, ax = plt.subplots(figsize=(10, 4.5))
        race_gender_pivot.plot(kind="bar", stacked=True, ax=ax,
                               color=[GENDER_COLOR_MAP.get(c, "#999") for c in race_gender_pivot.columns])
        ax.set_xlabel("")
        ax.set_ylabel("Number of Encounters")
        ax.set_title("Race Distribution Split by Gender")
        plt.xticks(rotation=20)
        st.pyplot(fig)

    with tab3:
        st.write("Heatmap showing how patient counts break down across race and age group together.")
        combo = pd.crosstab(df["race"], df["age"])
        fig, ax = plt.subplots(figsize=(11, 5))
        sns.heatmap(combo, annot=True, fmt="d", cmap="crest", ax=ax)
        ax.set_title("Patient Count: Race vs Age Group")
        ax.set_xlabel("Age Group")
        ax.set_ylabel("Race")
        st.pyplot(fig)


elif page == "🏥 Hospital & Clinical Insights":
    hero("🏥 Hospital & Clinical Insights", "Admissions, hospital stay duration, procedures, and diagnoses patterns.")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Admission Patterns", "Hospital Stay & Procedures", "Diagnoses", "Correlations"]
    )

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            admission_type_counts = df["admission_type"].value_counts()
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.barplot(x=admission_type_counts.values, y=admission_type_counts.index, palette="crest", ax=ax)
            ax.set_xlabel("Number of Encounters")
            ax.set_ylabel("")
            ax.set_title("Admission Type Distribution")
            st.pyplot(fig)
        with col2:
            source_counts = df["admission_source"].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.barplot(x=source_counts.values, y=source_counts.index, palette="crest", ax=ax)
            ax.set_xlabel("Number of Encounters")
            ax.set_ylabel("")
            ax.set_title("Top 10 Admission Sources")
            st.pyplot(fig)

        discharge_counts = df["discharge_disposition"].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(11, 4.5))
        sns.barplot(x=discharge_counts.index, y=discharge_counts.values, palette="crest", ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Number of Encounters")
        ax.set_title("Top 10 Discharge Dispositions")
        plt.xticks(rotation=35, ha="right")
        st.pyplot(fig)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.histplot(df["Hospital_Stay"], bins=15, color="#0F9D8C", ax=ax)
            ax.set_xlabel("Days in Hospital")
            ax.set_ylabel("Number of Encounters")
            ax.set_title("Hospital Stay Duration Distribution")
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.boxplot(data=df, x="age", y="Hospital_Stay", palette="crest", ax=ax)
            ax.set_xlabel("Age Group")
            ax.set_ylabel("Days in Hospital")
            ax.set_title("Hospital Stay by Age Group")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        col3, col4 = st.columns(2)
        with col3:
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.histplot(df["Lab_Procedures"], bins=30, color="#38BDF8", ax=ax)
            ax.set_title("Lab Procedures Distribution")
            st.pyplot(fig)
        with col4:
            fig, ax = plt.subplots(figsize=(6, 4.5))
            sns.histplot(df["Medications"], bins=30, color="#A855F7", ax=ax)
            ax.set_title("Number of Medications Distribution")
            st.pyplot(fig)

        visits_df = df[["Outpatient_Visits", "Emergency_Visits", "Inpatient_Visits"]].melt(
            var_name="Visit Type", value_name="Count"
        )
        visits_summary = visits_df.groupby("Visit Type")["Count"].mean().reset_index()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(data=visits_summary, x="Visit Type", y="Count", palette="crest", ax=ax)
        ax.set_ylabel("Average Count per Encounter")
        ax.set_title("Average Prior Visits by Type")
        st.pyplot(fig)

        insight("A large majority of patients have zero prior outpatient/emergency/inpatient visits, "
                "so average counts stay low even though a small subset of patients drive frequent visits.")

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            top_diag = df["diag_1"].value_counts().head(10)
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.barplot(x=top_diag.values, y=top_diag.index.astype(str), palette="crest", ax=ax)
            ax.set_xlabel("Number of Encounters")
            ax.set_ylabel("ICD-9 Code")
            ax.set_title("Top 10 Primary Diagnosis Codes (diag_1)")
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.histplot(df["Diagnoses"], bins=16, color="#F97316", ax=ax)
            ax.set_xlabel("Total Diagnoses Entered")
            ax.set_ylabel("Number of Encounters")
            ax.set_title("Number of Diagnoses per Encounter")
            st.pyplot(fig)

    with tab4:
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
    hero("💊 Medication Analysis", "How diabetes medications are prescribed, adjusted, and used across patients.")

    col1, col2 = st.columns(2)
    with col1:
        med_counts = df["diabetesMed"].value_counts()
        fig, ax = plt.subplots(figsize=(5.5, 4.5))
        ax.pie(med_counts.values, labels=med_counts.index, autopct="%1.1f%%",
               colors=["#0F9D8C", "#EF4444"], startangle=90)
        ax.set_title("Patients Prescribed Diabetes Medication")
        st.pyplot(fig)
    with col2:
        change_counts = df["change"].value_counts()
        fig, ax = plt.subplots(figsize=(5.5, 4.5))
        ax.pie(change_counts.values, labels=change_counts.index, autopct="%1.1f%%",
               colors=["#38BDF8", "#FACC15"], startangle=90)
        ax.set_title("Medication Change During Encounter")
        st.pyplot(fig)

    section_title("Prescription Status by Drug")
    prevalence = {}
    for drug in MEDICATION_COLUMNS:
        prevalence[drug] = (df[drug] != "No").mean() * 100
    prevalence_df = pd.DataFrame({"drug": prevalence.keys(), "prescribed_pct": prevalence.values()})
    prevalence_df = prevalence_df.sort_values("prescribed_pct", ascending=False)
    top_drugs = prevalence_df.head(8)["drug"].tolist()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=prevalence_df.head(12), x="prescribed_pct", y="drug", palette="crest", ax=ax)
    ax.set_xlabel("% of Patients Prescribed")
    ax.set_ylabel("")
    ax.set_title("Top 12 Most Prescribed Diabetes Medications")
    st.pyplot(fig)

    selected_drugs = st.multiselect(
        "Select medications to compare dosage change patterns",
        options=MEDICATION_COLUMNS, default=top_drugs[:5],
    )

    if selected_drugs:
        rows = []
        for drug in selected_drugs:
            counts = df[drug].value_counts()
            for status, cnt in counts.items():
                rows.append({"drug": drug, "status": status, "count": cnt})
        status_df = pd.DataFrame(rows)
        status_pivot = status_df.pivot(index="drug", columns="status", values="count").fillna(0)
        status_pivot = status_pivot.reindex(columns=["No", "Down", "Steady", "Up"], fill_value=0)
        fig, ax = plt.subplots(figsize=(9, 5))
        status_pivot.plot(kind="bar", stacked=True, ax=ax, colormap="crest")
        ax.set_xlabel("")
        ax.set_ylabel("Number of Encounters")
        ax.set_title("Dosage Status per Selected Medication")
        plt.xticks(rotation=30)
        st.pyplot(fig)

    section_title("Insulin Usage Across Age Groups")
    fig, ax = plt.subplots(figsize=(10, 5))
    insulin_pivot = pd.crosstab(df["age"], df["insulin"])
    insulin_pivot = insulin_pivot[["No", "Down", "Steady", "Up"]]
    insulin_pivot.plot(kind="bar", stacked=True, ax=ax, colormap="crest")
    ax.set_title("Insulin Dosage Status by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Number of Encounters")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    insight("Insulin is the most frequently adjusted medication, with usage rising sharply "
            "after age 40 and remaining high through the elderly population.")


elif page == "🔄 Readmission Analysis":
    hero("🔄 Readmission Analysis", "Examining which factors relate to patients returning to the hospital.")

    col1, col2 = st.columns([1, 1.3])
    with col1:
        readmit_counts = df["readmitted_label"].value_counts()
        colors = [READMIT_COLOR_MAP[k] for k in READMIT_ORDER if READMIT_LABELS[k] in readmit_counts.index]
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.pie(readmit_counts.values, labels=readmit_counts.index, autopct="%1.1f%%",
               colors=colors, startangle=90)
        ax.set_title("Overall Readmission Distribution")
        st.pyplot(fig)
    with col2:
        readmit_age = df.groupby(["age", "readmitted"], observed=True).size().reset_index(name="count")
        readmit_age["pct"] = readmit_age.groupby("age", observed=True)["count"].transform(lambda x: x / x.sum() * 100)
        pivot = readmit_age.pivot(index="age", columns="readmitted", values="pct").fillna(0)
        pivot = pivot[READMIT_ORDER]
        fig, ax = plt.subplots(figsize=(8, 5))
        pivot.plot(kind="bar", stacked=True, ax=ax,
                  color=[READMIT_COLOR_MAP[c] for c in pivot.columns])
        ax.set_xlabel("Age Group")
        ax.set_ylabel("Percentage of Encounters")
        ax.set_title("Readmission Rate (%) by Age Group")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    col3, col4 = st.columns(2)
    with col3:
        fig, ax = plt.subplots(figsize=(6, 4.5))
        sns.countplot(data=df, x="gender", hue="readmitted", hue_order=READMIT_ORDER,
                      palette=READMIT_COLOR_MAP, ax=ax)
        ax.set_title("Readmission by Gender")
        st.pyplot(fig)
    with col4:
        fig, ax = plt.subplots(figsize=(6, 4.5))
        sns.boxplot(data=df, x="readmitted", y="Hospital_Stay", order=READMIT_ORDER,
                   palette=READMIT_COLOR_MAP, ax=ax)
        ax.set_title("Hospital Stay vs Readmission")
        st.pyplot(fig)

    section_title("Readmission vs Clinical Utilization")
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    sns.boxplot(data=df, x="readmitted", y="Lab_Procedures", order=READMIT_ORDER, palette="crest", ax=ax[0])
    ax[0].set_title("Lab Procedures vs Readmission")
    sns.violinplot(data=df, x="readmitted", y="Medications", order=READMIT_ORDER, palette="crest", ax=ax[1])
    ax[1].set_title("Medications Count vs Readmission")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.countplot(data=df, x="diabetesMed", hue="readmitted", hue_order=READMIT_ORDER, palette="crest", ax=ax)
    ax.set_title("Diabetes Medication vs Readmission")
    st.pyplot(fig)

    section_title("Lab Procedures vs Hospital Stay (Sampled)")
    sample_df = df.sample(n=5000, random_state=42)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(data=sample_df, x="Lab_Procedures", y="Hospital_Stay", hue="readmitted",
                    hue_order=READMIT_ORDER, palette=READMIT_COLOR_MAP, alpha=0.5, ax=ax)
    ax.set_title("Lab Procedures vs Hospital Stay by Readmission Status (5,000 Sample)")
    st.pyplot(fig)

    insight("Patients readmitted within 30 days tend to have longer hospital stays and more "
            "medications on average, hinting these encounters involve more complex cases.")


elif page == "📊 Interactive Dashboard":
    hero("📊 Interactive Dashboard", "Filter the dataset live and explore patterns dynamically.")

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

    filtered = df[
        df["gender"].isin(genders)
        & df["race"].isin(races)
        & df["age"].astype(str).isin(age_groups)
        & df["admission_type"].isin(admission_types)
    ]

    if filtered.empty:
        st.warning("No records match the selected filters. Please adjust your selection.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        kpi_card("Filtered Encounters", f"{len(filtered):,}", c1)
        kpi_card("Avg Hospital Stay", f"{filtered['Hospital_Stay'].mean():.1f} days", c2)
        kpi_card("Readmitted <30 Days", f"{(filtered['readmitted'] == '<30').mean() * 100:.1f}%", c3)
        kpi_card("Avg Medications", f"{filtered['Medications'].mean():.1f}", c4)

        col1, col2 = st.columns(2)
        with col1:
            readmit_counts = filtered["readmitted_label"].value_counts()
            colors = [READMIT_COLOR_MAP[k] for k in READMIT_ORDER if READMIT_LABELS[k] in readmit_counts.index]
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.pie(readmit_counts.values, labels=readmit_counts.index, autopct="%1.1f%%",
                  colors=colors, startangle=90)
            ax.set_title("Readmission Breakdown (Filtered)")
            st.pyplot(fig)
        with col2:
            age_counts = filtered["age"].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.barplot(x=age_counts.index.astype(str), y=age_counts.values, palette="crest", ax=ax)
            ax.set_xlabel("Age Group")
            ax.set_ylabel("Number of Encounters")
            ax.set_title("Age Distribution (Filtered)")
            plt.xticks(rotation=45)
            st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(10, 4.5))
        sns.histplot(filtered["Hospital_Stay"], bins=15, color="#0F9D8C", ax=ax)
        ax.set_title("Hospital Stay Distribution (Filtered)")
        st.pyplot(fig)

        section_title("Filtered Data Table")
        display_df = filtered.drop(columns=["age"]).assign(age=filtered["age"].astype(str))
        st.dataframe(display_df.head(500), use_container_width=True, height=350)

        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Filtered Data as CSV", data=csv,
                          file_name="filtered_diabetic_data.csv", mime="text/csv")


