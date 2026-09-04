import pandas as pd
df = pd.read_csv("IDS_ALLcountries_Data.csv", encoding="latin-1")
print(df.head())
df.info()
print(df.shape)
print(df.columns)
print(df.isnull().sum())
null_counts = df.isnull().sum().sort_values(ascending=False)

print(null_counts.head(15).to_string())
print((df.isnull().sum() / len(df) * 100).sort_values(ascending=False).head(15))
print("Duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicate rows after cleaning:", df.duplicated().sum())
print(df.dtypes)
print(df.select_dtypes(include="object").columns)
print(df.select_dtypes(include="number").columns)
print(df["2020"].head())
print(df["2020"].dtype)
df.to_csv("International_Debt_Cleaned.csv", index=False)
print(df.columns.tolist())
print(df.describe())
print(df["Country Name"].nunique())
print(df["Country Name"].unique())
print(df[df["Country Name"].str.contains("Data from database|Last Updated", na=False)])
df = df[~df["Country Name"].str.contains(
    "Data from database|Last Updated",
    na=False
)]
print(df.shape)
df.to_csv("International_Debt_Cleaned.csv", index=False)
print(df["Country Name"].value_counts().head(15))
print(df[["Country Name", "Country Code"]].drop_duplicates().head(30))
print(df["Country Code"].isnull().sum())
print(df[df["Country Code"].isnull()][["Country Name", "Country Code"]])
df = df.dropna(subset=["Country Name", "Country Code"])
print(df[["Country Name", "Country Code"]].isnull().sum())
print(df.describe())
print(df.mean(numeric_only=True))
print(df.median(numeric_only=True))
print(df.groupby("Country Name").sum(numeric_only=True).head(10))

print(df[["Country Name", "Country Code"]].drop_duplicates().tail(30))
print(df["Country Code"].unique()[:50])
print(df[["Country Name", "Country Code"]].drop_duplicates().head(20))
country_meta = pd.read_csv("IDS_CountryMetaData.csv", encoding="cp1252")
print(country_meta.columns.tolist())
print("COUNTRY META COLUMNS:", country_meta.columns.tolist())
#df = df[df["Country Name"].isin(country_meta["Table Name"])]
print(df["Country Name"].isin(country_meta["Table Name"]).sum())


country_debt = df.groupby("Country Name").sum(numeric_only=True).sum(axis=1)

print(country_debt.sort_values(ascending=False).head(10))
# Actual countries only
country_list = country_meta.loc[
    country_meta["Region"].notna(), "Table Name"
].dropna().unique()

country_df = df[df["Country Name"].isin(country_list)]


print(country_df["Country Name"].nunique())
print(country_df["Country Name"].drop_duplicates().head(20))
country_debt_actual = (
    country_df.groupby("Country Name")
    .sum(numeric_only=True)
    .sum(axis=1)
)

print(country_debt_actual.sort_values(ascending=False).head(10))
print(
    df[df["Series Name"].str.contains(
        "External debt stocks, total",
        case=False,
        na=False
    )]["Series Name"].drop_duplicates().to_list()
)
print("Test successful")
# Total External Debt
debt_df = country_df[
    country_df["Series Name"] == "External debt stocks, total (DOD, current US$)"
].copy()

# Find year columns
year_cols = [col for col in debt_df.columns if str(col).isdigit()]

# Latest available year
valid_years = [
    col for col in year_cols
    if debt_df[col].notna().any()
]

latest_year = max(valid_years, key=int)


print("Latest Year:", latest_year)

# Top 10 countries by latest year external debt
top_10_debt = (
    debt_df[["Country Name", latest_year]]
    .dropna()
    .sort_values(by=latest_year, ascending=False)
    .head(10)
)

print(top_10_debt)



# EDA 3 - Debt Indicator Analysis

indicator_debt = (
    country_df[["Series Name", latest_year]]
    .dropna()
    .groupby("Series Name")[latest_year]
    .sum()
    .sort_values(ascending=False)
)

print("Top 10 Debt Indicators by Total Debt:")
print(indicator_debt.head(10))

print("Total Indicators:", country_df["Series Name"].nunique())
# EDA 4 - Debt Trends Over Years

year_totals = country_df[year_cols].sum()

print("Total Debt by Year:")
print(year_totals)
print("Highest Debt Year:", year_totals.idxmax())
print("Highest Debt Value:", year_totals.max())

print("Lowest Debt Year:", year_totals.idxmin())
print("Lowest Debt Value:", year_totals.min())
# EDA 5 - Statistical Summary

debt_values = country_df[year_cols].stack()

print("Statistical Summary of Debt:")
print(debt_values.describe())

print("Mean Debt:", debt_values.mean())
print("Median Debt:", debt_values.median())
print("Maximum Debt:", debt_values.max())
print("Minimum Debt:", debt_values.min())
# VISUALIZATION 1 - Total Debt Trend Over Years

import plotly.express as px

fig = px.line(
    x=year_totals.index,
    y=year_totals.values,
    markers=True,
    title="Total Debt Trend Over Years",
    labels={
        "x": "Year",
        "y": "Total Debt"
    }
)

fig.show()
# VISUALIZATION 2 - Top 10 Countries by Total Debt

country_totals = country_df[year_cols].sum(axis=1)

top_10 = pd.DataFrame({
    "Country": country_df["Country Name"],
    "Total Debt": country_totals
})

# Combine duplicate countries
top_10 = (
    top_10.groupby("Country", as_index=False)["Total Debt"]
    .sum()
    .sort_values("Total Debt", ascending=False)
    .head(10)
)

print("Top 10 Countries by Total Debt:")
print(top_10)

fig2 = px.bar(
    top_10,
    x="Country",
    y="Total Debt",
    title="Top 10 Countries by Total Debt",
    labels={
        "Country": "Country",
        "Total Debt": "Total Debt"
    },
    text="Total Debt"
)    
#Show actual value directly above each bar
fig2.update_traces(
    texttemplate="%{y:.3s}",
    textposition="outside"
)

fig2.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode="hide"
)

fig2.show()
# Visualization 3: Top 10 Indicators by Total Debt
print(df.columns.tolist())
year_cols = df.select_dtypes(include="number").columns
indicator_totals = df.groupby("Series Name")[year_cols].sum().sum(axis=1)

top_10_indicators = indicator_totals.sort_values(ascending=False).head(10)

print("Top 10 Indicators by Total Debt:")
print(top_10_indicators)

fig3 = px.bar(
    x=top_10_indicators.index,
    y=top_10_indicators.values,
    title="Top 10 Indicators by Total Debt",
    labels={
        "x": "Indicator Name",
        "y": "Total Debt"
    },
    text=[f"{x/1_000_000_000_000:.2f}T" for x in top_10_indicators.values]
)

fig3.update_traces(textposition="outside")

fig3.update_layout(
    yaxis_title="Total Debt (Trillion)",
    showlegend=False
)

fig3.update_xaxes(showgrid=False)
fig3.update_yaxes(showgrid=False)

fig3.show()
# Visualization 4: Debt Distribution Across Different Indicators
indicator_totals = df.groupby("Series Name")[year_cols].sum().sum(axis=1)

# Sort indicators by total debt
indicator_totals = indicator_totals.sort_values(ascending=False)

# Select top 10 indicators
top_indicators = indicator_totals.head(10)

# Convert values to trillion for display
top_indicator_trillion = top_indicators / 1_000_000_000_000

# Create vertical bar chart
fig4 = px.bar(
    x=top_indicators.index,
    y=top_indicators.values,
    title="Debt Distribution Across Different Indicators",
    labels={
        "x": "Indicators",
        "y": "Total Debt (Trillion)"
    },
    text=[
        f"{x:.2f}T"
        for x in top_indicator_trillion.values
    ]
)

# Display value labels above bars
fig4.update_traces(
    textposition="outside"
)

# Layout settings - remove grid lines
fig4.update_layout(
    showlegend=False
)

fig4.update_xaxes(showgrid=False)
fig4.update_yaxes(showgrid=False)

# Display chart
fig4.show()
# Visualization 5: Country-wise and Indicator-wise Debt Comparison

# Calculate total debt for each country
country_totals = df.groupby("Country Name")[year_cols].sum().sum(axis=1)

# Select top 5 countries
top_countries = country_totals.sort_values(ascending=False).head(5).index

# Calculate total debt for each indicator
indicator_totals = df.groupby("Series Name")[year_cols].sum().sum(axis=1)

# Select top 5 indicators
top_indicators = indicator_totals.sort_values(ascending=False).head(5).index
# Filter data for top countries and top indicators
comparison_data = df[
    df["Country Name"].isin(top_countries) &
    df["Series Name"].isin(top_indicators)
]

# Calculate total values
comparison_data = comparison_data.groupby(
    ["Country Name", "Series Name"]
)[year_cols].sum().sum(axis=1).reset_index(name="Total Debt")    

# Convert values to  trillion
comparison_data["Total Debt (Trillion)"] = (
   comparison_data["Total Debt"] / 1_000_000_000_000
)   

# Create grouped bar chart
fig5 = px.bar(
    comparison_data,
    x="Country Name",
    y="Total Debt (Trillion)",
    color="Series Name",
    barmode="group",
    title="Country-wise and Indicator-wise Debt Comparison",
    labels={
        "Country Name": "Country",
        "Total Debt (Trillion)": "Total Debt (Trillion)",

        "Series Name": "Indicatore"
    }
    
)

# Display chart
fig5.update_traces(textposition="outside")
fig5.show()

# --------------------------------------------------
# INSIGHTS AND REPORTING

# --------------------------------------------------
year_cols = [str(col) for col in df.columns if str(col).isdigit()]
print("Year columns:", year_cols)
print("\nColumn Names:")
print(df.columns.tolist())
# Debt-related indicators
debt_indicators = df[
    df["Series Name"].str.contains("External debt", case=False, na=False)
]["Series Name"].unique()

print("\nDebt-related Indicators:")
for indicator in debt_indicators:
    print(indicator)
# Insight 1: Which year had the highest principal repayment?

repayment_data = df[
    df["Series Name"].str.contains(
        "Principal repayments on external debt",
        case=False,
        na=False
    )
]

repayment_total = (
    repayment_data[year_cols]
    .apply(pd.to_numeric, errors="coerce")
    .sum()
)

highest_repayment_year = repayment_total.idxmax()
highest_repayment_value = repayment_total.max()

print("\nInsight 1:")
print("Year with highest principal repayment:", highest_repayment_year)
print("Highest principal repayment:", highest_repayment_value)
# Insight 2: Which year had the lowest principal repayment?

lowest_repayment_year = repayment_total.idxmin()
lowest_repayment_value = repayment_total.min()

print("\nInsight 2:")
print("Year with lowest principal repayment:", lowest_repayment_year)
print("Lowest principal repayment:", lowest_repayment_value)
# Insight 3: Which year had the highest external debt?

external_debt_data = df[
    df["Series Name"].str.contains(
        "External debt stocks, total",
        case=False,
        na=False
    )
]

external_debt_total = (
    external_debt_data[year_cols]
    .apply(pd.to_numeric, errors="coerce")
    .sum()
)

highest_debt_year = external_debt_total.idxmax()
highest_debt_value = external_debt_total.max()

print("\nInsight 3:")
print("Year with highest external debt:", highest_debt_year)
print("Highest external debt:", highest_debt_value)
# Insight 4: Which region has the most debt records?

country_record_count = (
    df["Country Name"]
    .value_counts()
    .sort_values(ascending=False)
)

top_country = country_record_count.idxmax()
top_count = country_record_count.max()

print("\nInsight 4:")
print("Country with most debt records:", top_country)
print("Number of debt records:", top_count)
# Insight 5: Which year had the highest number of debt records?

year_record_count = (
    df[year_cols]
    .notna()
    .sum()
)

highest_record_year = year_record_count.idxmax()
highest_record_count = year_record_count.max()

print("\nInsight 5:")
print("Year with highest number of debt records:", highest_record_year)
print("Number of debt records:", highest_record_count)






