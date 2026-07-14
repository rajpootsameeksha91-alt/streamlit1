import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from mappings import (
    ADMISSION_TYPE, DISCHARGE_DISPOSITION, ADMISSION_SOURCE,
    AGE_ORDER, MEDICATION_COLUMNS, READMIT_ORDER, READMIT_LABELS,
)
from style import (
    inject_css, hero, kpi_card, section_title, insight,
    PLOTLY_TEMPLATE, COLOR_SEQUENCE, READMIT_COLOR_MAP, GENDER_COLOR_MAP,
)

st.set_page_config(
    page_title="Diabetic Patient Healthcare Analysis",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
px.defaults.template = PLOTLY_TEMPLATE
px.defaults.color_discrete_sequence = COLOR_SEQUENCE
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

    tab1, tab2, tab3 = st.tabs(["Age & Gender", "Race", "Combined Views"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            age_counts = df["age"].value_counts().sort_index().reset_index()
            age_counts.columns = ["age", "count"]
            fig = px.bar(age_counts, x="age", y="count", color="count",
                         color_continuous_scale="Teal", title="Patient Count by Age Group")
            fig.update_layout(showlegend=False, xaxis_title="Age Group", yaxis_title="Number of Encounters")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            gender_counts = df["gender"].value_counts().reset_index()
            gender_counts.columns = ["gender", "count"]
            fig = px.pie(gender_counts, names="gender", values="count", hole=0.45,
                         color="gender", color_discrete_map=GENDER_COLOR_MAP,
                         title="Gender Distribution")
            st.plotly_chart(fig, use_container_width=True)

        age_gender = df.groupby(["age", "gender"], observed=True).size().reset_index(name="count")
        fig = px.bar(age_gender, x="age", y="count", color="gender", barmode="group",
                     color_discrete_map=GENDER_COLOR_MAP, title="Age Distribution Split by Gender")
        fig.update_layout(xaxis_title="Age Group", yaxis_title="Number of Encounters")
        st.plotly_chart(fig, use_container_width=True)

        insight("Most encounters come from patients aged 50–80, indicating diabetes-related "
                "hospital visits are concentrated in middle-aged to elderly populations.")

    with tab2:
        col1, col2 = st.columns([1.3, 1])
        with col1:
            race_counts = df["race"].value_counts().reset_index()
            race_counts.columns = ["race", "count"]
            fig = px.bar(race_counts, x="count", y="race", orientation="h", color="race",
                         title="Patient Count by Race")
            fig.update_layout(showlegend=False, yaxis_title="", xaxis_title="Number of Encounters")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.barplot(y=race_counts["race"], x=race_counts["count"], palette="crest", ax=ax)
            ax.set_xlabel("Number of Encounters")
            ax.set_ylabel("")
            ax.set_title("Race Distribution (Seaborn)")
            st.pyplot(fig)

        race_gender = df.groupby(["race", "gender"], observed=True).size().reset_index(name="count")
        fig = px.bar(race_gender, x="race", y="count", color="gender", barmode="stack",
                     color_discrete_map=GENDER_COLOR_MAP, title="Race Distribution Split by Gender")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        sunburst_df = df.groupby(["race", "gender", "age"], observed=True).size().reset_index(name="count")
        sunburst_df = sunburst_df[sunburst_df["count"] > 0]
        fig = px.sunburst(sunburst_df, path=["race", "gender", "age"], values="count",
                          color="race", title="Patient Composition: Race → Gender → Age")
        fig.update_layout(height=650)
        st.plotly_chart(fig, use_container_width=True)

        treemap_df = df.groupby(["race", "gender"], observed=True).size().reset_index(name="count")
        fig = px.treemap(treemap_df, path=["race", "gender"], values="count",
                         color="count", color_continuous_scale="Teal",
                         title="Treemap: Race and Gender Composition")
        st.plotly_chart(fig, use_container_width=True)


elif page == "🏥 Hospital & Clinical Insights":
    hero("🏥 Hospital & Clinical Insights", "Admissions, hospital stay duration, procedures, and diagnoses patterns.")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Admission Patterns", "Hospital Stay & Procedures", "Diagnoses", "Correlations"]
    )

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            admission_type_counts = df["admission_type"].value_counts().reset_index()
            admission_type_counts.columns = ["type", "count"]
            fig = px.bar(admission_type_counts, x="count", y="type", orientation="h", color="type",
                         title="Admission Type Distribution")
            fig.update_layout(showlegend=False, yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            source_counts = df["admission_source"].value_counts().head(10).reset_index()
            source_counts.columns = ["source", "count"]
            fig = px.bar(source_counts, x="count", y="source", orientation="h", color="source",
                         title="Top 10 Admission Sources")
            fig.update_layout(showlegend=False, yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)

        discharge_counts = df["discharge_disposition"].value_counts().head(10).reset_index()
        discharge_counts.columns = ["disposition", "count"]
        fig = px.bar(discharge_counts, x="disposition", y="count", color="disposition",
                     title="Top 10 Discharge Dispositions")
        fig.update_layout(showlegend=False, xaxis_title="", xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(df, x="Hospital_Stay", nbins=15, color_discrete_sequence=["#0F9D8C"],
                               title="Hospital Stay Duration Distribution")
            fig.update_layout(xaxis_title="Days in Hospital", yaxis_title="Number of Encounters")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(df, x="age", y="Hospital_Stay", color="age",
                        title="Hospital Stay by Age Group")
            fig.update_layout(showlegend=False, xaxis_title="Age Group", yaxis_title="Days in Hospital")
            st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            fig = px.histogram(df, x="Lab_Procedures", nbins=30, color_discrete_sequence=["#38BDF8"],
                               title="Lab Procedures Distribution")
            st.plotly_chart(fig, use_container_width=True)
        with col4:
            fig = px.histogram(df, x="Medications", nbins=30, color_discrete_sequence=["#A855F7"],
                               title="Number of Medications Distribution")
            st.plotly_chart(fig, use_container_width=True)

        visits_df = df[["Outpatient_Visits", "Emergency_Visits", "Inpatient_Visits"]].melt(
            var_name="Visit Type", value_name="Count"
        )
        visits_summary = visits_df.groupby("Visit Type")["Count"].mean().reset_index()
        fig = px.bar(visits_summary, x="Visit Type", y="Count", color="Visit Type",
                     title="Average Prior Visits by Type")
        fig.update_layout(showlegend=False, yaxis_title="Average Count per Encounter")
        st.plotly_chart(fig, use_container_width=True)

        insight("A large majority of patients have zero prior outpatient/emergency/inpatient visits, "
                "so average counts stay low even though a small subset of patients drive frequent visits.")

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            top_diag = df["diag_1"].value_counts().head(10).reset_index()
            top_diag.columns = ["diagnosis_code", "count"]
            fig = px.bar(top_diag, x="count", y="diagnosis_code", orientation="h",
                        color="count", color_continuous_scale="Tealgrn",
                        title="Top 10 Primary Diagnosis Codes (diag_1)")
            fig.update_layout(yaxis_title="ICD-9 Code", yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.histogram(df, x="Diagnoses", nbins=16, color_discrete_sequence=["#F97316"],
                               title="Number of Diagnoses per Encounter")
            fig.update_layout(xaxis_title="Total Diagnoses Entered", yaxis_title="Number of Encounters")
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        numeric_cols = ["Hospital_Stay", "Lab_Procedures", "Procedures", "Medications",
                        "Outpatient_Visits", "Emergency_Visits", "Inpatient_Visits", "Diagnoses"]
        corr = df[numeric_cols].corr()

        col1, col2 = st.columns([1.1, 1])
        with col1:
            fig, ax = plt.subplots(figsize=(7, 6))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="crest", ax=ax, linewidths=0.5)
            ax.set_title("Correlation Heatmap of Clinical Numeric Features")
            st.pyplot(fig)
        with col2:
            fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="Teal",
                            title="Interactive Correlation Matrix")
            st.plotly_chart(fig, use_container_width=True)

        insight("Lab Procedures, Medications, and Hospital Stay show the strongest positive "
                "relationships, suggesting longer admissions involve more tests and prescriptions.")


elif page == "💊 Medication Analysis":
    hero("💊 Medication Analysis", "How diabetes medications are prescribed, adjusted, and used across patients.")

    col1, col2 = st.columns(2)
    with col1:
        med_counts = df["diabetesMed"].value_counts().reset_index()
        med_counts.columns = ["status", "count"]
        fig = px.pie(med_counts, names="status", values="count", hole=0.45,
                     title="Patients Prescribed Diabetes Medication")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        change_counts = df["change"].value_counts().reset_index()
        change_counts.columns = ["status", "count"]
        fig = px.pie(change_counts, names="status", values="count", hole=0.45,
                     title="Medication Change During Encounter")
        st.plotly_chart(fig, use_container_width=True)

    section_title("Prescription Status by Drug")
    prevalence = {}
    for drug in MEDICATION_COLUMNS:
        prevalence[drug] = (df[drug] != "No").mean() * 100
    prevalence_df = pd.DataFrame({"drug": prevalence.keys(), "prescribed_pct": prevalence.values()})
    prevalence_df = prevalence_df.sort_values("prescribed_pct", ascending=False)
    top_drugs = prevalence_df.head(8)["drug"].tolist()

    fig = px.bar(prevalence_df.head(12), x="prescribed_pct", y="drug", orientation="h",
                color="prescribed_pct", color_continuous_scale="Teal",
                title="Top 12 Most Prescribed Diabetes Medications")
    fig.update_layout(xaxis_title="% of Patients Prescribed", yaxis_title="",
                      yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

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
        fig = px.bar(status_df, x="drug", y="count", color="status", barmode="stack",
                     title="Dosage Status per Selected Medication",
                     category_orders={"status": ["No", "Down", "Steady", "Up"]})
        fig.update_layout(xaxis_title="", yaxis_title="Number of Encounters")
        st.plotly_chart(fig, use_container_width=True)

    section_title("Insulin Usage Across Age Groups")
    insulin_age = df.groupby(["age", "insulin"], observed=True).size().reset_index(name="count")
    fig = px.bar(insulin_age, x="age", y="count", color="insulin", barmode="stack",
                category_orders={"insulin": ["No", "Down", "Steady", "Up"]},
                title="Insulin Dosage Status by Age Group")
    fig.update_layout(xaxis_title="Age Group", yaxis_title="Number of Encounters")
    st.plotly_chart(fig, use_container_width=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    insulin_pivot = pd.crosstab(df["age"], df["insulin"])
    insulin_pivot = insulin_pivot[["No", "Down", "Steady", "Up"]]
    insulin_pivot.plot(kind="bar", stacked=True, ax=ax, colormap="crest")
    ax.set_title("Insulin Status by Age Group (Matplotlib/Seaborn Style)")
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
        readmit_counts = df["readmitted_label"].value_counts().reset_index()
        readmit_counts.columns = ["status", "count"]
        color_map_label = {READMIT_LABELS[k]: v for k, v in READMIT_COLOR_MAP.items()}
        fig = px.pie(readmit_counts, names="status", values="count", hole=0.45,
                     color="status", color_discrete_map=color_map_label,
                     title="Overall Readmission Distribution")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        readmit_age = df.groupby(["age", "readmitted"], observed=True).size().reset_index(name="count")
        readmit_age["pct"] = readmit_age.groupby("age", observed=True)["count"].transform(lambda x: x / x.sum() * 100)
        fig = px.bar(readmit_age, x="age", y="pct", color="readmitted", barmode="stack",
                     category_orders={"readmitted": READMIT_ORDER},
                     color_discrete_map=READMIT_COLOR_MAP,
                     title="Readmission Rate (%) by Age Group")
        fig.update_layout(xaxis_title="Age Group", yaxis_title="Percentage of Encounters")
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        readmit_gender = df.groupby(["gender", "readmitted"], observed=True).size().reset_index(name="count")
        fig = px.bar(readmit_gender, x="gender", y="count", color="readmitted", barmode="group",
                     category_orders={"readmitted": READMIT_ORDER},
                     color_discrete_map=READMIT_COLOR_MAP, title="Readmission by Gender")
        st.plotly_chart(fig, use_container_width=True)
    with col4:
        readmit_race = df.groupby(["race", "readmitted"], observed=True).size().reset_index(name="count")
        fig = px.bar(readmit_race, x="race", y="count", color="readmitted", barmode="stack",
                     category_orders={"readmitted": READMIT_ORDER},
                     color_discrete_map=READMIT_COLOR_MAP, title="Readmission by Race")
        fig.update_layout(xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)

    section_title("Readmission vs Clinical Utilization")
    col5, col6 = st.columns(2)
    with col5:
        fig = px.box(df, x="readmitted", y="Hospital_Stay", color="readmitted",
                    category_orders={"readmitted": READMIT_ORDER},
                    color_discrete_map=READMIT_COLOR_MAP, title="Hospital Stay vs Readmission")
        st.plotly_chart(fig, use_container_width=True)
    with col6:
        fig = px.violin(df, x="readmitted", y="Medications", color="readmitted", box=True,
                        category_orders={"readmitted": READMIT_ORDER},
                        color_discrete_map=READMIT_COLOR_MAP, title="Medications Count vs Readmission")
        st.plotly_chart(fig, use_container_width=True)

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    sns.boxplot(data=df, x="readmitted", y="Lab_Procedures", order=READMIT_ORDER, palette="crest", ax=ax[0])
    ax[0].set_title("Lab Procedures vs Readmission")
    sns.countplot(data=df, x="diabetesMed", hue="readmitted", hue_order=READMIT_ORDER, palette="crest", ax=ax[1])
    ax[1].set_title("Diabetes Medication vs Readmission")
    st.pyplot(fig)

    section_title("Lab Procedures vs Hospital Stay (Sampled)")
    sample_df = df.sample(n=5000, random_state=42)
    fig = px.scatter(sample_df, x="Lab_Procedures", y="Hospital_Stay", color="readmitted",
                     category_orders={"readmitted": READMIT_ORDER},
                     color_discrete_map=READMIT_COLOR_MAP, opacity=0.6,
                     title="Lab Procedures vs Hospital Stay by Readmission Status (5,000 Sample)")
    st.plotly_chart(fig, use_container_width=True)

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
            readmit_counts = filtered["readmitted_label"].value_counts().reset_index()
            readmit_counts.columns = ["status", "count"]
            color_map_label = {READMIT_LABELS[k]: v for k, v in READMIT_COLOR_MAP.items()}
            fig = px.pie(readmit_counts, names="status", values="count", hole=0.45,
                        color="status", color_discrete_map=color_map_label,
                        title="Readmission Breakdown (Filtered)")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            age_counts = filtered["age"].value_counts().sort_index().reset_index()
            age_counts.columns = ["age", "count"]
            fig = px.bar(age_counts, x="age", y="count", color="count",
                        color_continuous_scale="Teal", title="Age Distribution (Filtered)")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            fig = px.histogram(filtered, x="Hospital_Stay", nbins=15,
                               color_discrete_sequence=["#0F9D8C"],
                               title="Hospital Stay Distribution (Filtered)")
            st.plotly_chart(fig, use_container_width=True)


        section_title("Filtered Data Table")
        display_df = filtered.drop(columns=["age"]).assign(age=filtered["age"].astype(str))
        st.dataframe(display_df.head(500), use_container_width=True, height=350)

        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Filtered Data as CSV", data=csv,
                          file_name="filtered_diabetic_data.csv", mime="text/csv")


