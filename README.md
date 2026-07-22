# 📊 Smart Sales Analytics Dashboard

Business Intelligence dashboard end-to-end — mulai dari **data cleaning, EDA,
data preparation, hingga dashboard interaktif** — dibangun menggunakan
**Python, Pandas, Plotly, dan Streamlit**.

Dataset yang digunakan: [Superstore Sales Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
(9.994 transaksi, 2014–2017).

---

## 🎯 Tujuan Proyek

Menunjukkan kemampuan end-to-end seorang **Data Analyst / BI Analyst**:
mengambil data mentah → membersihkannya → melakukan eksplorasi & analisis →
menyusun data untuk pelaporan → membangun dashboard interaktif yang menjawab
pertanyaan bisnis nyata.

## ❓ Pertanyaan Bisnis yang Dijawab

| Tema | Pertanyaan | Ada di Tab |
|---|---|---|
| **Sales** | Bagaimana tren penjualan dari waktu ke waktu? Bulan mana tertinggi? Meningkat/menurun? | 📈 Sales Performance |
| **Profit** | Apakah sales tinggi = profit tinggi? Produk mana yang merugi? Apakah diskon terlalu besar menekan profit? | 💰 Profit Analysis |
| **Customer** | Siapa pelanggan terbaik? Segment mana paling menguntungkan? | 👥 Customer |
| **Product** | Produk apa paling laku? Kategori mana profit terbesar? | 📦 Product |
| **Regional** | Wilayah mana performanya terbaik? Kota mana perlu perhatian? | 🌍 Regional |

Semua tab merespons **filter interaktif** di sidebar (Year, Region, Segment,
Category), sehingga setiap angka dan grafik selalu konsisten dengan slice
data yang sedang dilihat pengguna.

---

## 🗂️ Struktur Proyek

```
Smart Sales Analytics/
├── app.py                       # Aplikasi utama Streamlit
├── helpers/
│   ├── load_data.py              # Load data, filter, & perhitungan KPI
│   └── style.py                  # Custom CSS & komponen insight box
├── data/
│   ├── raw/superstore.csv        # Data mentah
│   └── final/Superstore_Clean.csv# Data hasil cleaning (dipakai app.py)
├── processed/                    # Tabel agregasi hasil notebook (referensi)
├── notebooks/
│   ├── 01_EDA.ipynb               # Data cleaning + exploratory data analysis
│   └── 02_Dashboard_Data.ipynb    # Persiapan data untuk dashboard
├── assets/logo.png
├── .streamlit/config.toml        # Tema warna dashboard
└── requirements.txt
```

## 🚀 Cara Menjalankan

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🛠 Tech Stack

- **Python & Pandas** — data cleaning & aggregation
- **Plotly** — visualisasi interaktif
- **Streamlit** — dashboard web app

## 👨‍💻 Developer

Ariko Yahya Setyawan
