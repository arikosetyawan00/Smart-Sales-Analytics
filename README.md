<div align="center">

# 📊 Smart Sales Analytics Dashboard

**End-to-end Business Intelligence project** — from raw data to an interactive
decision-support dashboard — built with Python, Pandas, Plotly, and
Streamlit.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.59-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-3.0-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-6.9-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](#license)

**[🔴 Live Demo](https://your-app-name.streamlit.app)** · [Notebooks](#notebooks) · [Business Questions](#-business-questions--answers)

</div>

---

## 📌 Overview

Retail companies generate large volumes of transactional data, but raw data
alone rarely drives decisions — it needs to be cleaned, explored, and turned
into something stakeholders can actually act on.

This project simulates that full workflow for a fictional superstore chain:
**9,994 transactions across 4 years, 3 product categories, and 4 US regions.**
Instead of only producing static charts, the end deliverable is a **filterable,
interactive dashboard** that lets a stakeholder slice the data by year,
region, segment, or category and get consistent answers across every view.

> 💡 The goal of this project isn't just to visualize data — it's to
> demonstrate the complete Data Analyst workflow: data cleaning → exploratory
> analysis → business-question-driven reporting → interactive dashboarding.

---

## 🖼️ Preview

<div align="center">

*(add a screenshot or screen recording GIF of the dashboard here)*

`assets/preview.png`

</div>

---

## ❓ Business Questions & Answers

The dashboard is organized around five themes, each mapped directly to a
tab and answering real business questions:

| Theme | Business Questions | Dashboard Tab |
|---|---|---|
| **Sales** | How is the sales trend over time? Which month performed best? Is growth increasing or slowing down? | 📈 Sales Performance |
| **Profit** | Does high sales always mean high profit? Which products are losing money? Are heavy discounts hurting margins? | 💰 Profit Analysis |
| **Customer** | Who are the best customers? Which segment is the most profitable? | 👥 Customer |
| **Product** | Which products sell the most? Which category drives the most profit? | 📦 Product |
| **Regional** | Which region performs best? Which cities need attention? | 🌍 Regional |

### Key Insights Found

- Sales and Profit are only moderately correlated (**r ≈ 0.48**) — high
  revenue products don't automatically mean high profitability.
- Discount and Profit show a **negative correlation (r ≈ -0.22)**; discounts
  above ~20–30% frequently push transactions into a loss.
- Over **300 products** in the dataset have a net-negative profit despite
  positive sales — a clear candidate list for pricing/discount policy review.
- Q4 consistently shows the strongest sales performance across all years.

---

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| Data cleaning & analysis | Python, Pandas, NumPy |
| Visualization | Plotly |
| Dashboard / App | Streamlit |
| Notebooks | Jupyter |

---

## 🗂️ Project Structure

```
Smart Sales Analytics/
├── app.py                        # Main Streamlit application
├── helpers/
│   ├── load_data.py               # Data loading, filtering, KPI calculations
│   └── style.py                   # Custom CSS & reusable UI components
├── data/
│   ├── raw/superstore.csv          # Original raw dataset
│   └── final/Superstore_Clean.csv  # Cleaned dataset (powers the live app)
├── processed/                     # Pre-aggregated reference tables from notebooks
│   └── dashboard_filters.json
├── notebooks/
│   ├── 01_EDA.ipynb                # Data cleaning + exploratory data analysis
│   └── 02_Dashboard_Data.ipynb     # Data preparation pipeline for the dashboard
├── assets/logo.png
├── .streamlit/config.toml         # Dashboard color theme
└── requirements.txt
```

---

## 🚀 Getting Started

### Run locally

```bash
git clone https://github.com/<your-username>/smart-sales-analytics.git
cd smart-sales-analytics
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
streamlit run app.py
```

The app will open at `http://localhost:8501`.

### Deployed version

The dashboard is deployed on **Streamlit Community Cloud**:
👉 **[your-app-name.streamlit.app](https://your-app-name.streamlit.app)**

---

## 📓 Notebooks

| Notebook | Purpose |
|---|---|
| `01_EDA.ipynb` | Data understanding, cleaning, exploratory data analysis (distributions, correlations, time series, customer/product/regional analysis), and business recommendations |
| `02_Dashboard_Data.ipynb` | Aggregation pipeline that prepares reference datasets and filter options consumed by the dashboard |

---

## 📈 Dataset

[Superstore Sales Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
— 9,994 retail transactions (2014–2017), covering orders, customers,
products, and regional/shipping information across the United States.

---

## 👨‍💻 Author

**Ariko Yahya Setyawan**

[LinkedIn](#) · [GitHub](#) · [Portfolio](#)

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
