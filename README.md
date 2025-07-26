
# 🧭 MyTCAS Dashboard

**MyTCAS Dashboard** is a project designed to present course information from [mytcas.com](https://course.mytcas.com) in an interactive dashboard. The data is collected via **web scraping** and visualized using tools such as **Streamlit**, **Pandas**, and **Matplotlib/Seaborn**. This helps users better understand computer engineering programs across universities in Thailand.

---

## 🛠️ Technologies Used

| Tech | Description |
|------|-------------|
| `Python 3.10+` | Main programming language |
| `Streamlit` | Interactive web dashboard framework |
| `Pandas` | Data manipulation and transformation |
| `Matplotlib` + `Seaborn` | Visualization libraries |
| `BeautifulSoup` + `Playwright` | Used for scraping from mytcas.com (optional) |

---

## 📈 Dashboard Features

- Filter data by **university** and **program type**
- Visualizations include:
  - Average tuition fees per university
  - Boxplot and histogram of tuition fees
  - Scatter plot of total admission vs. tuition
  - Pie chart of program types
  - Bar chart showing admission volume by round (Round 1–4)
- Viewable **data table with filters**
- Fully supports Thai text with LeelawUI font

---

## 📂 Project Structure

```
MyTCAS-Dashboard/
│
├── data/
│   └── rearranged_courses_tuition_numeric.json   ← Scraped and cleaned course data
│
├── app.py         ← Main Streamlit dashboard
├── scraper.py     ← (optional) scraping script for collecting data
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Prepare data**
   - Run `scraper.py` (if available)
   - Or use existing `data/rearranged_courses_tuition_numeric.json`

3. **Launch the dashboard**
```bash
streamlit run app.py
```

---

## 📌 Notes

- All course data shown is publicly scraped and not altered from its original source.
- This project is intended for educational and analytical purposes only.

---

## 🙋‍♂️ Developer

**[17Saberz](https://github.com/17Saberz)**

Feel free to fork, clone, or contribute to this repository!
