import glob
import os
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

# ----------------------------------
# PAGE SETTINGS
# ----------------------------------
st.set_page_config(
    page_title="Online Retail Sales Dashboard", page_icon="📊", layout="wide"
)


# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Auto-detect Excel or CSV file in project folder or 'data' folder
    search_patterns = [
        os.path.join(BASE_DIR, "*.xlsx"),
        os.path.join(BASE_DIR, "data", "*.xlsx"),
        os.path.join(BASE_DIR, "*.csv"),
        os.path.join(BASE_DIR, "data", "*.csv"),
        os.path.join(BASE_DIR, "*.csv.gz")
    ]

    found_files = []
    for pattern in search_patterns:
        found_files.extend(glob.glob(pattern))

    if not found_files:
        st.error(f"❌ No dataset found in folder: `{BASE_DIR}`")
        st.write("📁 **Files found in folder:**", os.listdir(BASE_DIR))
        st.stop()

    file_path = found_files[0]

    if file_path.endswith((".csv", ".csv.gz")):
        df = pd.read_csv(file_path, encoding="utf-8")
    else:
        df = pd.read_excel(file_path, engine="openpyxl")

    # Data cleaning & preprocessing
    df = df.dropna(subset=["InvoiceNo", "Quantity", "UnitPrice"])
    df = df.drop_duplicates()
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df = df[~df["InvoiceNo"].str.startswith("C")]
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    df = df[df["Quantity"] < 50000]
    df = df[df["StockCode"].astype(str).str.match(r"^\d{5}")]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Sales"] = df["Quantity"] * df["UnitPrice"]

    return df


df = load_data()

# ----------------------------------
# SIDEBAR FILTERS
# ----------------------------------
st.sidebar.header("Dashboard Filters")

all_countries = sorted(df["Country"].dropna().unique().tolist())

selected_countries = st.sidebar.multiselect(
    "Select Country", options=all_countries, default=all_countries
)

# Filter dataset dynamically based on multiselect choices
if selected_countries:
    filtered_df = df[df["Country"].isin(selected_countries)]
else:
    filtered_df = df.copy()

# ----------------------------------
# HEADER
# ----------------------------------
st.title("📊 Online Retail Sales Dashboard")
st.write(
    "This dashboard communicates the main sales findings from the Online Retail dataset."
)

st.markdown("---")

# ----------------------------------
# KEY PERFORMANCE INDICATORS (KPIs)
# ----------------------------------
st.subheader("Key Performance Indicators")

total_sales = filtered_df["Sales"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
units_sold = int(filtered_df["Quantity"].sum())
avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"£{total_sales:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Units Sold", f"{units_sold:,}")
col4.metric("Average Order Value", f"£{avg_order_value:,.2f}")

st.markdown("---")

# ----------------------------------
# SALES BY COUNTRY CHART
# ----------------------------------
st.subheader("Sales by Country")

country_sales = (
    filtered_df.groupby("Country")["Sales"]
    .sum()
    .reset_index()
    .sort_values(by="Sales", ascending=True)
    .tail(10)
)

fig = px.bar(
    country_sales,
    x="Sales",
    y="Country",
    orientation="h",
    title="Top 10 Countries by Sales",
    text_auto=".2s",
)

fig.update_layout(
    xaxis_title="Sales",
    yaxis_title="Country",
    height=450,
    margin=dict(l=20, r=20, t=40, b=20),
)

st.plotly_chart(fig, use_container_width=True)


# -----------------------------------
# MONTHLY SALES
# -----------------------------------
st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .dropna(subset=["InvoiceDate"])
    .set_index("InvoiceDate")
    .resample("ME")["Sales"]
    .sum()
)


fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)

ax.set_title("Monthly Sales Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Sales (£)")

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig)


# -----------------------------------
# TOP PRODUCTS
# -----------------------------------
st.subheader("Top 10 Products by Sales")

product_sales = (
    filtered_df
    .groupby("Description")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


st.dataframe(
    product_sales.reset_index(),
    use_container_width=True
)


# -----------------------------------
# TOP CUSTOMERS
# -----------------------------------
st.subheader("Top 10 Customers by Sales")

customer_sales = (
    filtered_df
    .dropna(subset=["CustomerID"])
    .groupby("CustomerID")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)


st.dataframe(
    customer_sales.reset_index(),
    use_container_width=True
)

# ----------------------------------
# KEY FINDINGS
# ----------------------------------
st.subheader("Key Findings")

if not filtered_df.empty:
    # Group sales by country
    country_totals = filtered_df.groupby("Country")["Sales"].sum()
    
    # Get top country name and sales amount as a float scalar
    best_country_name = country_totals.idxmax()
    best_country_sales = float(country_totals.max())  # Convert to single float number

    st.markdown(
        f"**Top Performing Country:** {best_country_name} with total sales of **£{best_country_sales:,.2f}**."
    )


# Finding 2
best_month = monthly_sales.idxmax()
best_month_sales = monthly_sales.max()

st.write(
    f"**2. The highest-sales month is {best_month.strftime('%B %Y')}, "
    f"with sales of £{best_month_sales:,.2f}.**"
)


# Finding 3
best_product = product_sales.index[0]
best_product_sales = product_sales.iloc[0]

st.write(
    f"**3. The top-selling product by revenue is "
    f"{best_product}, generating £{best_product_sales:,.2f}.**"
)

# ----------------------------------
# TOP 10 BEST-SELLING PRODUCTS
# ----------------------------------
st.subheader("Top 10 Best-Selling Products")

# Group data by product description and sum the quantities sold
top_products = (
    filtered_df.groupby("Description")["Quantity"]
    .sum()
    .reset_index()
    .sort_values(by="Quantity", ascending=True)
    .tail(10)  # Top 10 items
)

fig_products = px.bar(
    top_products,
    x="Quantity",
    y="Description",
    orientation="h",
    title="Top 10 Products by Quantity Sold",
    text_auto=".2s",
    color="Quantity",
    color_continuous_scale="Blues",
)

fig_products.update_layout(
    xaxis_title="Quantity Sold",
    yaxis_title="Product Description",
    height=450,
    margin=dict(l=20, r=20, t=40, b=20),
    showlegend=False,
)

st.plotly_chart(fig_products, use_container_width=True)
# -----------------------------------
# RECOMMENDED ACTION
# -----------------------------------
st.subheader("💡 Recommended Action")

st.write(
    f"Focus marketing and inventory planning on the strongest "
    f"market, **{best_country_name}**, and prioritize high-performing "
    f"products such as **{best_product}**. "
    f"Sales campaigns and inventory availability can also be "
    f"planned around the strongest sales periods."
)


# -----------------------------------
# DATA SOURCE
# -----------------------------------
st.divider()

st.caption(
    "Source: Online Retail.xlsx | "
    "All calculations are generated directly from the raw dataset."
)
st.caption("Cleaning: removed duplicates, cancellations, non-positive quantity or price, and two cancelled bulk orders (74k and 81k units). Limits: one year of data, one UK retailer, wholesale buyers, 25% of rows without CustomerID, December 2011 is partial.")