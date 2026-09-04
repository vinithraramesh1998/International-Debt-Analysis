import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="international_debt_db"
)

query = """
SELECT country_code, series_code, debt_value
FROM debt_data
"""

chunks = []

for chunk in pd.read_sql(query, conn, chunksize=100000):
    grouped = (
        chunk.groupby(["country_code", "series_code"], as_index=False)["debt_value"]
        .sum()
    )
    chunks.append(grouped)

q7_result = pd.concat(chunks)

q7_result = (
    q7_result
    .groupby(["country_code", "series_code"], as_index=False)["debt_value"]
    .sum()
    .rename(columns={"debt_value": "total_debt"})
    .sort_values("total_debt", ascending=False)
)

print(q7_result.head(20))

q7_result.to_csv("q7_result.csv", index=False)



print("Q7 result saved successfully!")
# =========================
# Q8 - Number of indicators for each country
# =========================

query_q8 = """
SELECT country_code, series_code
FROM debt_data
"""

chunks = []

for chunk in pd.read_sql(query_q8, conn, chunksize=100000):
    chunks.append(chunk.drop_duplicates())

df_q8 = pd.concat(chunks)

q8_result = (
    df_q8.groupby("country_code")["series_code"]
    .nunique()
    .reset_index(name="indicator_count")
    .sort_values("indicator_count", ascending=False)
)

print(q8_result)

q8_result.to_csv("q8_result.csv", index=False)

print("Q8 result saved successfully!")

# Q9 - Total debt for each country and year

query_q9 = """
SELECT country_code, year, debt_value
FROM debt_data
"""

chunks_q9 = []

for chunk in pd.read_sql(query_q9, conn, chunksize=100000):
    chunks_q9.append(chunk)

df_q9 = pd.concat(chunks_q9)

q9_result = (
    df_q9.groupby(["country_code", "year"])["debt_value"]
    .sum()
    .reset_index(name="total_debt")
    .sort_values("total_debt", ascending=False)
)

print(q9_result)

q9_result.to_csv("q9_result.csv", index=False)

print("Q9 result saved successfully!")
# Q10 - Average debt for each country

query_q10 = """
SELECT country_code, debt_value
FROM debt_data
"""

chunks_q10 = []

for chunk in pd.read_sql(query_q10, conn, chunksize=100000):
    chunks_q10.append(chunk)

df_q10 = pd.concat(chunks_q10)

q10_result = (
    df_q10.groupby("country_code")["debt_value"]
    .mean()
    .reset_index(name="average_debt")
    .sort_values("average_debt", ascending=False)
)

print(q10_result)

q10_result.to_csv("q10_result.csv", index=False)

print("Q10 result saved successfully!")