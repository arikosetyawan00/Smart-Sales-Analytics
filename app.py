import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from helpers.load_data import (
    apply_filters,
    compute_kpis,
    load_filters,
    load_raw_data,
)
from helpers.style import insight_box, load_css

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Smart Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# ==========================================
# Load Data
# ==========================================

df = load_raw_data()
filter_options = load_filters()

# ==========================================
# Sidebar — Branding & Filters
# ==========================================

with st.sidebar:
    st.image("assets/logo.png", width=90)
    st.title("Smart Sales Analytics")
    st.caption("Version 2.0 · Business Intelligence Dashboard")
    st.markdown("---")

    st.markdown("### 🔎 Filters")

    selected_years = st.multiselect(
        "Year",
        options=filter_options["Year"],
        default=filter_options["Year"],
    )

    selected_regions = st.multiselect(
        "Region",
        options=filter_options["Region"],
        default=filter_options["Region"],
    )

    selected_segments = st.multiselect(
        "Segment",
        options=filter_options["Segment"],
        default=filter_options["Segment"],
    )

    selected_categories = st.multiselect(
        "Category",
        options=filter_options["Category"],
        default=filter_options["Category"],
    )

    if st.button("↺ Reset Filters", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.write("Ariko Yahya Setyawan")

    st.markdown("---")
    st.markdown("### 🛠 Tech Stack")
    st.markdown(
        """
    - Python & Pandas
    - Plotly
    - Streamlit
    """
    )

    st.markdown("---")
    st.info("Business Intelligence Portfolio Project")

# ==========================================
# Apply Filters
# ==========================================

filtered_df = apply_filters(
    df,
    years=selected_years,
    regions=selected_regions,
    segments=selected_segments,
    categories=selected_categories,
)

if filtered_df.empty:
    st.warning(
        "⚠️ Tidak ada data yang cocok dengan kombinasi filter yang dipilih. "
        "Silakan ubah filter di sidebar."
    )
    st.stop()

kpis = compute_kpis(filtered_df)

# ==========================================
# Header
# ==========================================

col1, col2 = st.columns([5, 1])

with col1:
    st.title("📊 Smart Sales Analytics Dashboard")
    st.markdown(
        """
A Business Intelligence Dashboard to monitor sales performance, profits, customers, products, and regions interactively 

"""
    )

with col2:
    st.image("assets/logo.png", width=120)

st.caption(
    f"Menampilkan **{len(filtered_df):,} transaksi** dari total {len(df):,} "
    f"transaksi berdasarkan filter yang dipilih."
)

st.divider()

# ==========================================
# Executive Summary (KPIs)
# ==========================================

st.subheader("📈 Executive Summary")

kpi_cols = st.columns(6)

kpi_cols[0].metric("💰 Total Sales", f"${kpis['Total Sales']:,.0f}")
kpi_cols[1].metric("📈 Total Profit", f"${kpis['Total Profit']:,.0f}")
kpi_cols[2].metric("📊 Profit Margin", f"{kpis['Profit Margin (%)']:.1f}%")
kpi_cols[3].metric("🛒 Total Orders", f"{kpis['Total Orders']:,}")
kpi_cols[4].metric("👥 Customers", f"{kpis['Total Customers']:,}")
kpi_cols[5].metric("🧾 Avg Order Value", f"${kpis['Average Order Value']:,.0f}")

st.download_button(
    "⬇️ Download Filtered Data (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="smart_sales_analytics_filtered.csv",
    mime="text/csv",
)

st.divider()

# ==========================================
# Tabs — one per business question theme
# ==========================================

tab_sales, tab_profit, tab_customer, tab_product, tab_region = st.tabs(
    [
        "📈 Sales Performance",
        "💰 Profit Analysis",
        "👥 Customer",
        "📦 Product",
        "🌍 Regional",
    ]
)

# ------------------------------------------
# TAB 1 — Sales Performance
# ------------------------------------------
with tab_sales:
    st.markdown("#### Bagaimana tren penjualan dari waktu ke waktu?")

    monthly = (
        filtered_df.groupby(["Year", "Month", "Month Name"])
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
        .sort_values(["Year", "Month"])
    )
    monthly["Period"] = pd.to_datetime(
        monthly["Year"].astype(str) + "-" + monthly["Month"].astype(str) + "-01"
    )

    fig_trend = go.Figure()
    fig_trend.add_trace(
        go.Scatter(
            x=monthly["Period"],
            y=monthly["Sales"],
            name="Sales",
            mode="lines+markers",
            line=dict(color="#2563EB", width=3),
        )
    )
    fig_trend.add_trace(
        go.Scatter(
            x=monthly["Period"],
            y=monthly["Profit"],
            name="Profit",
            mode="lines+markers",
            line=dict(color="#10B981", width=3),
            yaxis="y2",
        )
    )
    fig_trend.update_layout(
        title="Monthly Sales vs Profit Trend",
        xaxis_title="Period",
        yaxis=dict(title="Sales ($)"),
        yaxis2=dict(title="Profit ($)", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        height=450,
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    if not monthly.empty:
        best_month = monthly.loc[monthly["Sales"].idxmax()]
        first_sales = monthly["Sales"].iloc[0]
        last_sales = monthly["Sales"].iloc[-1]
        growth = ((last_sales - first_sales) / first_sales * 100) if first_sales else 0
        trend_word = "meningkat 📈" if growth >= 0 else "menurun 📉"

        insight_box(
            f"Penjualan tertinggi terjadi pada <b>{best_month['Month Name']} "
            f"{int(best_month['Year'])}</b> senilai <b>${best_month['Sales']:,.0f}</b>. "
            f"Dibandingkan periode awal terhadap periode terakhir pada data yang "
            f"terfilter, penjualan {trend_word} sebesar <b>{abs(growth):.1f}%</b>."
        )

    st.markdown("#### Performa penjualan per kuartal")
    quarter_sales = (
        filtered_df.groupby(["Year", "Quarter"])["Sales"].sum().reset_index()
    )
    fig_quarter = px.bar(
        quarter_sales,
        x="Quarter",
        y="Sales",
        color="Year",
        barmode="group",
        title="Quarterly Sales by Year",
        labels={"Sales": "Sales ($)"},
    )
    fig_quarter.update_layout(height=400)
    st.plotly_chart(fig_quarter, use_container_width=True)

# ------------------------------------------
# TAB 2 — Profit Analysis
# ------------------------------------------
with tab_profit:
    st.markdown("#### Apakah penjualan tinggi menghasilkan profit tinggi?")

    col_a, col_b = st.columns(2)

    with col_a:
        fig_sales_profit = px.scatter(
            filtered_df,
            x="Sales",
            y="Profit",
            color="Category",
            opacity=0.6,
            title="Sales vs Profit",
        )
        fig_sales_profit.update_layout(height=420)
        st.plotly_chart(fig_sales_profit, use_container_width=True)

    with col_b:
        fig_discount_profit = px.scatter(
            filtered_df,
            x="Discount",
            y="Profit",
            color="Category",
            opacity=0.6,
            title="Discount vs Profit",
        )
        fig_discount_profit.update_layout(height=420)
        st.plotly_chart(fig_discount_profit, use_container_width=True)

    corr = filtered_df["Sales"].corr(filtered_df["Profit"])
    corr_discount = filtered_df["Discount"].corr(filtered_df["Profit"])

    insight_box(
        f"Korelasi antara <b>Sales dan Profit</b> sebesar <b>{corr:.2f}</b> — "
        f"artinya penjualan tinggi tidak selalu menjamin profit tinggi. "
        f"Sementara korelasi antara <b>Discount dan Profit</b> sebesar "
        f"<b>{corr_discount:.2f}</b>, menunjukkan diskon yang terlalu besar "
        f"cenderung <b>menekan profit</b>."
    )

    st.markdown("#### Produk mana yang merugi?")
    loss_products = (
        filtered_df.groupby("Product Name")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Avg_Discount=("Discount", "mean"),
            Orders=("Order ID", "nunique"),
        )
        .reset_index()
        .query("Profit < 0")
        .sort_values("Profit")
    )

    st.dataframe(
        loss_products.head(15).style.format(
            {
                "Sales": "${:,.0f}",
                "Profit": "${:,.0f}",
                "Avg_Discount": "{:.0%}",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    if not loss_products.empty:
        insight_box(
            f"Ditemukan <b>{len(loss_products)} produk</b> yang merugi pada data "
            f"terfilter, dengan rata-rata diskon <b>"
            f"{loss_products['Avg_Discount'].mean():.0%}</b> — mengindikasikan "
            f"diskon berlebih sebagai salah satu penyebab utama kerugian."
        )
    else:
        st.success("Tidak ada produk yang merugi pada kombinasi filter ini. ✅")

# ------------------------------------------
# TAB 3 — Customer
# ------------------------------------------
with tab_customer:
    st.markdown("#### Siapa pelanggan terbaik?")

    top_customers = (
        filtered_df.groupby("Customer Name")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order ID", "nunique"),
        )
        .reset_index()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    fig_top_customer = px.bar(
        top_customers.sort_values("Sales"),
        x="Sales",
        y="Customer Name",
        orientation="h",
        color="Sales",
        color_continuous_scale="Blues",
        title="Top 10 Customers by Sales",
    )
    fig_top_customer.update_layout(height=450, coloraxis_showscale=False)
    st.plotly_chart(fig_top_customer, use_container_width=True)

    st.dataframe(
        top_customers.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}"}),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### Segment mana yang paling menguntungkan?")
    col_c, col_d = st.columns(2)

    segment_sales = filtered_df.groupby("Segment")["Sales"].sum().reset_index()
    segment_profit = filtered_df.groupby("Segment")["Profit"].sum().reset_index()

    with col_c:
        fig_seg_sales = px.pie(
            segment_sales,
            values="Sales",
            names="Segment",
            title="Sales Contribution by Segment",
            hole=0.45,
        )
        fig_seg_sales.update_layout(height=380)
        st.plotly_chart(fig_seg_sales, use_container_width=True)

    with col_d:
        fig_seg_profit = px.bar(
            segment_profit,
            x="Segment",
            y="Profit",
            color="Segment",
            title="Profit by Segment",
        )
        fig_seg_profit.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_seg_profit, use_container_width=True)

    if not segment_profit.empty:
        best_segment = segment_profit.loc[segment_profit["Profit"].idxmax()]
        insight_box(
            f"Segment <b>{best_segment['Segment']}</b> menghasilkan profit "
            f"terbesar senilai <b>${best_segment['Profit']:,.0f}</b> pada data "
            f"terfilter."
        )

# ------------------------------------------
# TAB 4 — Product
# ------------------------------------------
with tab_product:
    st.markdown("#### Produk apa yang paling laku & kategori mana paling profit?")

    category_perf = (
        filtered_df.groupby("Category")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
    )

    fig_category = px.bar(
        category_perf.melt(
            id_vars="Category", value_vars=["Sales", "Profit"], var_name="Metric"
        ),
        x="Category",
        y="value",
        color="Metric",
        barmode="group",
        title="Sales & Profit by Category",
        labels={"value": "Amount ($)"},
    )
    fig_category.update_layout(height=420)
    st.plotly_chart(fig_category, use_container_width=True)

    if not category_perf.empty:
        best_cat = category_perf.loc[category_perf["Profit"].idxmax()]
        insight_box(
            f"Kategori <b>{best_cat['Category']}</b> menghasilkan profit "
            f"terbesar senilai <b>${best_cat['Profit']:,.0f}</b>."
        )

    col_e, col_f = st.columns(2)

    with col_e:
        subcat_sales = (
            filtered_df.groupby("Sub-Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        fig_subcat = px.bar(
            subcat_sales.sort_values("Sales"),
            x="Sales",
            y="Sub-Category",
            orientation="h",
            title="Sales by Sub-Category",
        )
        fig_subcat.update_layout(height=550)
        st.plotly_chart(fig_subcat, use_container_width=True)

    with col_f:
        top_products = (
            filtered_df.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig_top_product = px.bar(
            top_products.sort_values("Sales"),
            x="Sales",
            y="Product Name",
            orientation="h",
            title="Top 10 Products by Sales",
            color="Sales",
            color_continuous_scale="Teal",
        )
        fig_top_product.update_layout(height=550, coloraxis_showscale=False)
        st.plotly_chart(fig_top_product, use_container_width=True)

# ------------------------------------------
# TAB 5 — Regional
# ------------------------------------------
with tab_region:
    st.markdown("#### Wilayah mana yang performanya paling baik?")

    region_perf = (
        filtered_df.groupby("Region")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
    )

    fig_region = px.bar(
        region_perf.melt(
            id_vars="Region", value_vars=["Sales", "Profit"], var_name="Metric"
        ),
        x="Region",
        y="value",
        color="Metric",
        barmode="group",
        title="Sales & Profit by Region",
        labels={"value": "Amount ($)"},
    )
    fig_region.update_layout(height=420)
    st.plotly_chart(fig_region, use_container_width=True)

    if not region_perf.empty:
        best_region = region_perf.loc[region_perf["Profit"].idxmax()]
        insight_box(
            f"Region <b>{best_region['Region']}</b> memberikan kontribusi "
            f"profit terbesar senilai <b>${best_region['Profit']:,.0f}</b>."
        )

    st.markdown("#### Top wilayah berdasarkan State")
    state_sales = (
        filtered_df.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )
    fig_state = px.bar(
        state_sales.sort_values("Sales"),
        x="Sales",
        y="State",
        orientation="h",
        title="Top 15 States by Sales",
    )
    fig_state.update_layout(height=550)
    st.plotly_chart(fig_state, use_container_width=True)

    st.markdown("#### Kota mana yang perlu perhatian?")
    city_perf = (
        filtered_df.groupby("City")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
        .sort_values("Profit")
        .head(10)
    )
    st.dataframe(
        city_perf.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}"}),
        use_container_width=True,
        hide_index=True,
    )
    insight_box(
        "Kota-kota di atas memiliki profit terendah (atau merugi) pada data "
        "terfilter dan perlu dievaluasi lebih lanjut — misalnya terkait "
        "kebijakan diskon, biaya pengiriman, atau bauran produk yang dijual."
    )

st.divider()
st.caption(
    "Smart Sales Analytics Dashboard · Built with Python, Pandas, Plotly & "
    "Streamlit · by Ariko Yahya Setyawan"
)
