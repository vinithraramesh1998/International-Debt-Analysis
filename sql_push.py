import pandas as pd
import mysql.connector

# Load cleaned data
df = pd.read_csv("International_Debt_Cleaned.csv", encoding="latin-1")

# Load country metadata
country_meta = pd.read_csv("IDS_CountryMetaData.csv", encoding="cp1252")

print("Data loaded successfully")
print("Rows:", len(df))


# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="international_debt_db"
)

cursor = conn.cursor()

print("MySQL Connected Successfully")


# Prepare country data
country_list = country_meta.loc[
    country_meta["Region"].notna(), "Table Name"
].dropna().unique()

countries = (
    df[df["Country Name"].isin(country_list)]
    [["Country Code", "Country Name"]]
    .drop_duplicates()
    .dropna()
)

print("Countries to insert:", len(countries))


# Insert countries into MySQL
country_query = """
INSERT IGNORE INTO countries (country_code, country_name)
VALUES (%s, %s)
"""

country_data = list(
    countries.itertuples(index=False, name=None)
)

cursor.executemany(country_query, country_data)
conn.commit()

print("Countries inserted successfully:", cursor.rowcount)


# Prepare indicator data
indicators = (
    df[["Series Code", "Series Name"]]
    .drop_duplicates()
    .dropna()
)

print("Indicators to insert:", len(indicators))


# Insert indicators into MySQL
indicator_query = """
INSERT IGNORE INTO indicators (series_code, series_name)
VALUES (%s, %s)
"""

indicator_data = list(
    indicators.itertuples(index=False, name=None)
)

cursor.executemany(indicator_query, indicator_data)
conn.commit()

print("Indicators inserted successfully:", cursor.rowcount)


# Match codes with existing MySQL values

cursor.execute("SELECT country_code FROM countries")
country_codes_db = {
    code.strip(): code
    for (code,) in cursor.fetchall()
}

cursor.execute("SELECT series_code FROM indicators")
series_codes_db = {
    code.strip(): code
    for (code,) in cursor.fetchall()
}

df["Country Code"] = (
    df["Country Code"]
    .astype(str)
    .str.strip()
    .map(country_codes_db)
)

df["Series Code"] = (
    df["Series Code"]
    .astype(str)
    .str.strip()
    .map(series_codes_db)
)


# Verify code mapping
print("Missing Country Codes:", df["Country Code"].isna().sum())
print("Missing Series Codes:", df["Series Code"].isna().sum())

print("\nSample mapped Series Codes:")
print(df["Series Code"].dropna().head(10))


# Prepare debt data
year_cols = [
    col for col in df.columns
    if str(col).isdigit()
]

debt_data = df[
    ["Country Code", "Series Code"] + year_cols
].melt(
    id_vars=["Country Code", "Series Code"],
    var_name="year",
    value_name="debt_value"
)

debt_data = debt_data.dropna(
    subset=["Country Code", "Series Code", "debt_value"]
)

debt_data["year"] = debt_data["year"].astype(int)

print("Debt data rows to insert:", len(debt_data))
print(debt_data.head())


# Get existing debt-data keys from MySQL
cursor.execute("""
    SELECT country_code, series_code, year
    FROM debt_data
""")

existing_keys = set(cursor.fetchall())

print("Existing debt keys:", len(existing_keys))


# Keep only new records
new_records = []

for row in debt_data.itertuples(index=False, name=None):
    if row[:3] not in existing_keys:
        new_records.append(row)

print("New debt rows to insert:", len(new_records))


# Insert new debt data in batches
debt_query = """
INSERT INTO debt_data
(country_code, series_code, year, debt_value)
VALUES (%s, %s, %s, %s)
"""

batch_size = 5000

for i in range(0, len(new_records), batch_size):

    batch = new_records[i:i + batch_size]

    cursor.executemany(debt_query, batch)
    conn.commit()

    print(
        f"Inserted {min(i + batch_size, len(new_records))} "
        f"/ {len(new_records)} new rows"
    )

print("Debt data insertion completed successfully!")


cursor.close()
conn.close()

print("Database connection closed.")