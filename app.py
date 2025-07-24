import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# ---------- Load Data ----------
with open("data/rearranged_courses_tuition_numeric.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# ---------- Rename columns for English display ----------
df = df.rename(columns={
    'รอบ 1 Portfolio': 'Round 1: Portfolio',
    'รอบ 2 Quota': 'Round 2: Quota',
    'รอบ 3 Admission': 'Round 3: Admission',
    'รอบ 4 Direct Admission': 'Round 4: Direct Admission'
})

# ---------- Cleaning ----------
df['total_admission'] = df[[
    'Round 1: Portfolio', 'Round 2: Quota', 'Round 3: Admission', 'Round 4: Direct Admission'
]].sum(axis=1, skipna=True)
df['tuition'] = pd.to_numeric(df['tuition'], errors='coerce')

# ---------- Sidebar ----------
st.sidebar.title("📊 Dashboard Options")
chart_type = st.sidebar.selectbox("Select Chart", [
    "Bar Chart: Total Admission per Round",
    "Histogram: Tuition Distribution",
    "Box Plot: Tuition by University",
    "Scatter Plot: Admission vs Tuition",
    "Heatmap: Admission Correlation"
])

st.title("🎓 Thai University Programs Dashboard")

# ---------- Chart 1 ----------
if chart_type == "Bar Chart: Total Admission per Round":
    st.subheader("Total Admissions per Round")
    round_sum = df[[
        'Round 1: Portfolio', 'Round 2: Quota', 'Round 3: Admission', 'Round 4: Direct Admission'
    ]].sum()
    fig, ax = plt.subplots()
    round_sum.plot(kind='bar', ax=ax)
    ax.set_ylabel("Total Admissions")
    ax.set_xlabel("Admission Rounds")
    st.pyplot(fig)

# ---------- Chart 2 ----------
elif chart_type == "Histogram: Tuition Distribution":
    st.subheader("Distribution of Program Tuition")
    fig, ax = plt.subplots()
    sns.histplot(df['tuition'].dropna(), kde=True, ax=ax, bins=30)
    ax.set_xlabel("Tuition (Baht)")
    st.pyplot(fig)

# ---------- Chart 3 ----------
elif chart_type == "Box Plot: Tuition by University":
    st.subheader("Box Plot: Tuition by University")
    
    uni_counts = df['university'].value_counts()
    top_universities = uni_counts[uni_counts > 3].index

    df_box = df[df['university'].isin(top_universities) & df['tuition'].notnull()]

    if df_box.empty:
        st.warning("⚠️ Not enough data to generate Box Plot (ensure university and tuition data exists)")
    else:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df_box, x='tuition', y='university', ax=ax)
        ax.set_xlabel("Tuition (Baht)")
        ax.set_ylabel("University")
        ax.set_title("Tuition per Program by University")
        st.pyplot(fig)

# ---------- Chart 4 ----------
elif chart_type == "Scatter Plot: Admission vs Tuition":
    st.subheader("Relationship between Total Admission and Tuition")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='total_admission', y='tuition', hue='program_type', ax=ax)
    ax.set_xlabel("Total Admission")
    ax.set_ylabel("Tuition (Baht)")
    st.pyplot(fig)

# ---------- Chart 5 ----------
elif chart_type == "Heatmap: Admission Correlation":
    st.subheader("Correlation of Admission Rounds")
    corr = df[[
        'Round 1: Portfolio', 'Round 2: Quota', 'Round 3: Admission', 'Round 4: Direct Admission'
    ]].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="YlGnBu", ax=ax)
    st.pyplot(fig)

# ---------- Data Table ----------
with st.expander("📋 View Full Data Table"):
    st.dataframe(df)
