
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

#===================================
#Stage 1: PAGE CONFIGURATION
#===================================
st.set_page_config(
    page_title="Pharmacy Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

#===================================
#Stage 2: LOAD DATASET
#===================================
df = pd.read_csv("pharmacy_full_data.csv")

#===================================
# Convert Date Columns
#===================================
df["Transaction_Date"] = pd.to_datetime(df["Transaction_Date"])

# Create Year Column
df["Year"] = df["Transaction_Date"].dt.year

# Create Month Column
df["Month"] = df["Transaction_Date"].dt.month_name()

#===================================
#Stage 3: SIDEBAR FILTERS
#===================================
st.sidebar.header("🔍 Dashboard Filters")

# Province Sidebar
province = st.sidebar.multiselect(
    "Select Province",
    options=sorted(df["Province"].unique()),
    default=sorted(df["Province"].unique())
)

# Branch Name
branch_name = st.sidebar.multiselect(
    "Select Branch",
    options=sorted(df["Branch_Name"].unique()),
    default=sorted(df["Branch_Name"].unique())
)

# Medicine Category
medicine_category = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Medicine_Category"].unique()),
    default=sorted(df["Medicine_Category"].unique())
)

# Prescription Required
prescription_required = st.sidebar.multiselect(
    "Select Prescription Required",
    options=sorted(df["Prescription_Required"].unique()),
    default=sorted(df["Prescription_Required"].unique())
)

# Medicine Name
medicine_name = st.sidebar.multiselect(
    "Select Medicine Name",
    options=sorted(df["Medicine_Name"].unique()),
    default=sorted(df["Medicine_Name"].unique())
)

# Payment Method
payment_method = st.sidebar.multiselect(
    "Select Payment Method",
    options=sorted(df["Payment_Method"].unique()),
    default=sorted(df["Payment_Method"].unique())
)

# Customer Gender
customer_gender = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["Customer_Gender"].unique()),
    default=sorted(df["Customer_Gender"].unique())
)

#===================================
# Age Group
#===================================
df["Age_Group"] = pd.cut(
    df["Customer_Age"],
    bins=[17, 29, 39, 49, 59, 100],
    labels=[
        "Young Adults",
        "Adults",
        "Middle_aged Adults",
        "Older Adults",
        "Senior Citizens"
    ]
)

age_group = st.sidebar.multiselect(
    "Select Age Group",
    options=sorted(df["Age_Group"].dropna().unique()),
    default=sorted(df["Age_Group"].dropna().unique())
)

#===================================
# Year Filter
#===================================
year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

#==================================
# Stage 4 : APPLY FILTERS
#==================================
df = df[
    (df["Province"].isin(province)) &
    (df["Branch_Name"].isin(branch_name)) &
    (df["Medicine_Category"].isin(medicine_category)) &
    (df["Prescription_Required"].isin(prescription_required)) &
    (df["Medicine_Name"].isin(medicine_name)) &
    (df["Payment_Method"].isin(payment_method)) &
    (df["Customer_Gender"].isin(customer_gender)) &
    (df["Age_Group"].isin(age_group)) &
    (df["Year"].isin(year))
]


#===================================
#Stage 5 : DASHBOARD TITLE
#===================================
st.title("📊 Pharmacy Sales Dashboard")

st.markdown("""
This interactive dashboard provides a comprehensive analysis of the Pharmacy sales dataset.

Use the filters on the left to explore sales performance across province, branch, categories,
prescription required, medicine name, payment method, gender, age group, and years.
""")

#==================================
# Stage 6 : KPI CARDS
#==================================
total_orders = len(df)
total_sales = df["Line_Total_LKR"].sum()
total_quantity_sold = df["Quantity"].sum()
average_discount = df["Discount_Rate"].mean() * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Orders", total_orders)

with col2:
    st.metric("Total Revenue", f"₦ {total_sales:,.2f}")

with col3:
    st.metric("Total Quantity Sold", f"{total_quantity_sold:,}")

with col4:
    st.metric("Average Discount Margin", f"{average_discount:.2f}%")
    

#===================================
#Stage 7 : DASHBOARD SUMMARY
#===================================
st.markdown("---")

st.subheader("📌 Dashboard Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"Filtered Records: {len(df)}")

with col2:
    st.success(f"Categories: {df['Medicine_Category'].nunique()}")

with col3:
    st.warning(f"Branches: {df['Branch_Name'].nunique()}")

st.markdown("### 📈 Business Insights")

col1, col2, col3 = st.columns(3)

best_province = df.groupby("Province")["Line_Total_LKR"].sum().idxmax()

best_category = df.groupby("Medicine_Category")["Line_Total_LKR"].sum().idxmax()

best_medicine = df.groupby("Medicine_Name")["Line_Total_LKR"].sum().idxmax()

with col1:
    st.success(f"🏆 Best Province\n\n{best_province}")

with col2:
    st.info(f"📦 Best Category\n\n{best_category}")

with col3:
    st.warning(f"⭐ Best Medicine\n\n{best_medicine}")

st.markdown("### 📊 Dataset Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Suppliers", df["Supplier_Name"].nunique())

with col2:
    st.metric("Payment Methods", df["Payment_Method"].nunique())

with col3:
    st.metric("Transactions", df["Transaction_ID"].nunique())

#===================================
#Stage 8: DATASET PREVIEW
#===================================

st.subheader("📄 Dataset Preview")

with st.expander("View Filtered Dataset"):
    st.dataframe(df, use_container_width=True)
    
    
#===================================
#Stage 9: CHARTS ANALYSIS
#===================================

# Chart 1 and Chart 2
# Revenue by Medicine Category & Monthly Sales Trend

category_revenue = (
    df.groupby("Medicine_Category")["Line_Total_LKR"]
    .sum()
    .sort_values(ascending=False)
)

monthly_revenue = (
    df.groupby("Month")["Line_Total_LKR"]
    .sum()
)

col1, col2 = st.columns(2)

#===================================
# Chart 1
#===================================
with col1:

    st.subheader("📊 Revenue by Medicine Category")

    fig = px.bar(
        x=category_revenue.index,
        y=category_revenue.values,
        labels={
            "x": "Medicine Category",
            "y": "Revenue"
        },
        color=category_revenue.values,
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig, use_container_width=True)

#===================================
# Chart 2
#===================================
with col2:

    st.subheader("📈 Monthly Revenue Trend")

    fig = px.line(
        x=monthly_revenue.index,
        y=monthly_revenue.values,
        labels={
            "x": "Month",
            "y": "Revenue"
        },
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

#===================================
# Chart 3 and Chart 4
#===================================

branch_revenue = (
    df.groupby("Branch_Name")["Line_Total_LKR"]
    .sum()
    .sort_values(ascending=False)
)

payment_revenue = (
    df.groupby("Payment_Method")["Line_Total_LKR"]
    .sum()
    .sort_values(ascending=False)
)

col1, col2 = st.columns(2)

#===================================
# Chart 3
#===================================
with col1:

    st.subheader("🏥 Revenue by Branch")

    fig = px.bar(
        x=branch_revenue.values,
        y=branch_revenue.index,
        orientation="h",
        color=branch_revenue.values,
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        xaxis_title="Revenue",
        yaxis_title="Branch Name"
    )

    st.plotly_chart(fig, use_container_width=True)

#===================================
# Chart 4
#===================================
with col2:

    st.subheader("💳 Revenue by Payment Method")

    fig = px.pie(
        names=payment_revenue.index,
        values=payment_revenue.values,
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)
    

#===================================
#DOWNLOAD FILTERED DATASET
#===================================

st.markdown("---")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_pharmacy_full_data.csv",
    mime="text/csv"
)

#===================================
#FOOTER
#===================================

st.markdown("---")

st.markdown(
"""
<div style='text-align:center;'>

### 📊 Pharmacy Sales Dashboard

Developed by **Okpanachi Ogwu**

Python • Pandas • Plotly • Streamlit

© 2026

</div>
""",
unsafe_allow_html=True
)

#===================================
#MAKE IT LOOK PREMIUM
#===================================

hide_st_style = """
<style>

/* Hide Streamlit default menu */
#MainMenu {
    visibility: hidden;
}

/* Hide Footer */
footer {
    visibility: hidden;
}

/* Hide Header */
header {
    visibility: hidden;
}

/* Reduce top padding */
.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
}

</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)
