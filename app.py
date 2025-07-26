import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import matplotlib.font_manager as fm

# ---------- ตั้งค่าหน้า ----------
st.set_page_config(page_title="MyTCAS Dashboard", layout="wide")

# ---------- ฟอนต์ภาษาไทย ----------
font_path = "C:/Windows/Fonts/LeelawUI.ttf"
font_prop = fm.FontProperties(fname=font_path)
matplotlib.rcParams['font.family'] = font_prop.get_name()

# ---------- โหลดข้อมูล ----------
df = pd.read_json("data/rearranged_courses_tuition_numeric.json")
df['total_admission'] = df[['รอบ 1 Portfolio', 'รอบ 2 Quota', 'รอบ 3 Admission', 'รอบ 4 Direct Admission']].sum(axis=1, skipna=True)

# ---------- เมนูเลือกหน้า ----------
st.sidebar.title("🔎 เมนู")
page = st.sidebar.radio("ไปยังหน้า", ["📊 Dashboard", "📋 ตารางข้อมูล"])

# ---------- หน้า Dashboard ----------
if page == "📊 Dashboard":
    st.title("🎓 Dashboard หลักสูตรวิศวกรรมคอมพิวเตอร์ (MyTCAS)")

    # Filter
    selected_university = st.sidebar.multiselect("เลือกมหาวิทยาลัย", sorted(df['university'].unique()))
    selected_program_type = st.sidebar.multiselect("เลือกประเภทหลักสูตร", df['program_type'].unique())

    df_filtered = df.copy()
    if selected_university:
        df_filtered = df_filtered[df_filtered['university'].isin(selected_university)]
    if selected_program_type:
        df_filtered = df_filtered[df_filtered['program_type'].isin(selected_program_type)]

    # Chart 1
    st.header("1️⃣ ค่าเทอมเฉลี่ยต่อมหาวิทยาลัย")
    avg_tuition = df_filtered.groupby('university')['tuition'].mean().sort_values(ascending=False)
    st.bar_chart(avg_tuition)

    # Chart 2
    st.header("2️⃣ Boxplot ค่าเทอมตามประเภทหลักสูตร")
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=df_filtered, x="program_type", y="tuition", ax=ax1)
    st.pyplot(fig1)

    # Chart 3
    st.header("3️⃣ Histogram: การกระจายของค่าเทอม")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    ax2.hist(df_filtered['tuition'], bins=20, edgecolor='black')
    ax2.set_xlabel("ค่าเทอม (บาท)")
    ax2.set_ylabel("จำนวนหลักสูตร")
    st.pyplot(fig2)

    # Chart 4
    st.header("4️⃣ Scatter: จำนวนรับรวมกับค่าเทอม")
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.scatter(df_filtered['total_admission'], df_filtered['tuition'])
    ax3.set_xlabel("จำนวนรับรวม (ทุกรอบ)")
    ax3.set_ylabel("ค่าเทอม (บาท)")
    st.pyplot(fig3)

    # Chart 5
    st.header("5️⃣ สัดส่วนประเภทหลักสูตร")
    pie_data = df_filtered['program_type'].value_counts()
    fig4, ax4 = plt.subplots()
    ax4.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
    ax4.axis("equal")
    st.pyplot(fig4)

    # Chart 6 - Bar Chart จำนวนรับแต่ละรอบ
    st.header("6️⃣ Bar Chart: จำนวนรับรวมของแต่ละรอบ")
    round_columns = ['รอบ 1 Portfolio', 'รอบ 2 Quota', 'รอบ 3 Admission', 'รอบ 4 Direct Admission']
    round_sums = df_filtered[round_columns].sum(skipna=True)
    colors = ['#4F81BD', '#9BBB59', '#8064A2', '#A5A5A5']  # ฟ้า เขียว ม่วง เทา

    fig5, ax5 = plt.subplots(figsize=(8, 5))
    bars = ax5.bar(round_sums.index, round_sums.values, color=colors)

    for bar in bars:
        height = bar.get_height()
        ax5.annotate(f'{int(height):,}', xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=10)

    ax5.set_ylabel("จำนวนรับรวม", fontsize=12)
    ax5.set_xlabel("รอบการรับสมัคร", fontsize=12)
    ax5.set_title("จำนวนรับรวมของแต่ละรอบการสมัคร", fontsize=14)
    ax5.set_ylim(0, round_sums.max() * 1.15)
    ax5.legend(bars, round_sums.index, title="รอบ", loc="upper right")

    st.pyplot(fig5)

# ---------- หน้า ตารางข้อมูล ----------
elif page == "📋 ตารางข้อมูล":
    st.title("📋 ตารางข้อมูลหลักสูตรทั้งหมด")

    col1, col2 = st.columns(2)
    with col1:
        selected_uni = st.multiselect("เลือกมหาวิทยาลัย", sorted(df['university'].unique()))
    with col2:
        selected_field = st.multiselect("เลือกสาขาวิชา", sorted(df['field'].unique()))

    df_table = df.copy()
    if selected_uni:
        df_table = df_table[df_table['university'].isin(selected_uni)]
    if selected_field:
        df_table = df_table[df_table['field'].isin(selected_field)]

    if 'url' in df_table.columns:
        df_table = df_table.drop(columns=['url'])

    st.dataframe(df_table.reset_index(drop=True), use_container_width=True)
