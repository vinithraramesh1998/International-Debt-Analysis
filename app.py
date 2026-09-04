import streamlit as st

import mysql.connector
import pandas as pd
import plotly.express as px

st.title("International Debt Analysis")

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="international_debt_db"
    )

 

except mysql.connector.Error as e:
    st.error(f"Database connection failed: {e}")
    # Fetch sample data from SQL

query = """
SELECT country_code, series_code, year, debt_value
FROM debt_data
LIMIT 10
"""
# Execute SQL query and display data
df_sql = pd.read_sql(query, conn)

st.subheader("Debt Data")
st.dataframe(df_sql)
# Country-wise Debt Analysis
st.subheader("Country-wise Debt Analysis")

series_list = pd.read_sql(
    "SELECT DISTINCT series_code FROM debt_data ORDER BY series_code",
    conn
)["series_code"].tolist()

selected_series = st.selectbox(
    "Select Debt Indicator",
    series_list
)

year_list = pd.read_sql(
    "SELECT DISTINCT year FROM debt_data ORDER BY year",
    conn
)["year"].tolist()

selected_year = st.selectbox(
    "Select Year",
    year_list
)

country_data = pd.read_sql(
    """
    SELECT country_code, debt_value
    FROM debt_data
    WHERE series_code = %s
      AND year = %s
    ORDER BY debt_value DESC
    LIMIT 10
    """,
    conn,
    params=(selected_series, selected_year)
)

fig = px.bar(
    country_data,
    x="country_code",
    y="debt_value",
    title=f"Top 10 Countries - {selected_series} ({selected_year})",
    labels={
        "country_code": "Country",
        "debt_value": "Debt Value"
    }
)

st.plotly_chart(fig, use_container_width=True)
# Year-wise Debt Trend
st.subheader("Year-wise Debt Trend")

trend_data = pd.read_sql(
    """
    SELECT year, debt_value
    FROM debt_data
    WHERE series_code = %s
    ORDER BY year
    """,
    conn,
    params=(selected_series,)
)

fig_trend = px.line(
    trend_data,
    x="year",
    y="debt_value",
    title=f"Debt Trend - {selected_series}",
    labels={
        "year": "Year",
        "debt_value": "Debt Value"
    }
)

st.plotly_chart(fig_trend, use_container_width=True)
# Country-wise External Debt Comparison
st.subheader("Country-wise External Debt Comparison")

selected_year = st.selectbox(
    "Select Year",
    sorted(df_sql["year"].unique(), reverse=True)
)

country_data = pd.read_sql(f"""
    SELECT country_code, debt_value
    FROM debt_data
    WHERE series_code = 'BM.GSR.TOTL.CD'
      AND year = {selected_year}
      AND debt_value > 0
    ORDER BY debt_value DESC
    LIMIT 10
""", conn)

fig_country = px.bar(
    country_data,
    x="country_code",
    y="debt_value",
    title=f"Top 10 Countries by External Debt - {selected_year}",
    labels={
        "country_code": "Country",
        "debt_value": "External Debt Value"
    },
    color="debt_value",
    color_continuous_scale="Turbo"
)

fig_country.update_layout(
    xaxis_title="Country",
    yaxis_title="External Debt",
    height=500
)

st.plotly_chart(fig_country, use_container_width=True)


