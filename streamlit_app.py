import streamlit as st
import pandas as pd
from db_config import get_engine

st.set_page_config(page_title="SecureCheck Dashboard", layout="wide")
st.title("🚓 SecureCheck: Police Check Post Dashboard")

engine = get_engine()

@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM traffic_stops", engine)

df = load_data()

# ========== FILTER SECTION ==========
st.sidebar.header("🔎 Filter Logs")
selected_country = st.sidebar.selectbox("🌍 Country", df['country_name'].dropna().unique())
selected_gender = st.sidebar.multiselect("👤 Gender", df['driver_gender'].dropna().unique(), default=df['driver_gender'].dropna().unique())
selected_race = st.sidebar.multiselect("🧬 Race", df['driver_race'].dropna().unique(), default=df['driver_race'].dropna().unique())
selected_violation = st.sidebar.multiselect("⚖ Violation", df['violation'].dropna().unique(), default=df['violation'].dropna().unique())
search_age = st.sidebar.number_input("🎯 Search Driver Age", min_value=0, max_value=100, value=0)

filtered_df = df[
    (df['country_name'] == selected_country) &
    (df['driver_gender'].isin(selected_gender)) &
    (df['driver_race'].isin(selected_race)) &
    (df['violation'].isin(selected_violation))
]

if search_age > 0:
    filtered_df = filtered_df[filtered_df['driver_age'] == search_age]

st.subheader(f"📋 Logs from {selected_country}")
st.dataframe(filtered_df, use_container_width=True)

# ========== EXPORT SECTION ==========
@st.cache_data
def convert_df(download_df):
    return download_df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_df)
st.download_button("⬇️ Download CSV", csv, "filtered_logs.csv", "text/csv")

st.markdown("---")

# ========== ANALYTICS ==========
st.subheader("📈 Violation Frequency")
st.bar_chart(filtered_df['violation'].value_counts())

st.subheader("👮 Arrests by Age")
st.line_chart(filtered_df[filtered_df['is_arrested'] == True]['driver_age'].value_counts().sort_index())

st.subheader("💊 Drug-related Stops")
st.bar_chart(filtered_df[filtered_df['drugs_related_stop'] == True]['country_name'].value_counts())

st.subheader("🚨 High-Risk Alerts")
high_risk = filtered_df[
    (filtered_df['drugs_related_stop'] == True) |
    (filtered_df['is_arrested'] == True)
]

st.warning(f"{len(high_risk)} high-risk stop(s) detected.")
st.dataframe(high_risk, use_container_width=True)

st.markdown("---")
st.subheader("📄 SQL Analytical Reports")

# Dictionary: {Title: SQL}
query_map = {
    "🚗 Top 10 Drug-Related Stops": """
        SELECT * FROM traffic_stops
        WHERE drugs_related_stop = TRUE
        LIMIT 10
    """,
    
    "🧍 Arrest Rate by Age": """
        SELECT driver_age, COUNT(*) AS arrest_count
        FROM traffic_stops
        WHERE is_arrested = TRUE
        GROUP BY driver_age
        ORDER BY arrest_count DESC
        LIMIT 5
    """,
    
    "🧬 Search Rate by Race + Gender": """
        SELECT driver_race, driver_gender, COUNT(*) AS search_count
        FROM traffic_stops
        WHERE search_conducted = TRUE
        GROUP BY driver_race, driver_gender
        ORDER BY search_count DESC
        LIMIT 5
    """,

    "🕒 Hourly Stop Distribution": """
        SELECT HOUR(stop_time) AS hour_of_day, COUNT(*) AS total_stops
        FROM traffic_stops
        GROUP BY hour_of_day
        ORDER BY hour_of_day
    """,
    
    "⚖️ Top Violations < Age 25": """
        SELECT violation, COUNT(*) AS count
        FROM traffic_stops
        WHERE driver_age < 25
        GROUP BY violation
        ORDER BY count DESC
        LIMIT 5
    """,

    "🌍 Drug Stops by Country": """
        SELECT country_name, COUNT(*) AS total_drug_stops
        FROM traffic_stops
        WHERE drugs_related_stop = TRUE
        GROUP BY country_name
        ORDER BY total_drug_stops DESC
    """,

    "🧠 Yearly Arrests by Country": """
        SELECT country_name, YEAR(stop_date) AS year, COUNT(*) AS stops, SUM(is_arrested) AS arrests
        FROM traffic_stops
        GROUP BY country_name, YEAR(stop_date)
        ORDER BY year
    """
}

selected_report = st.selectbox("📌 Select SQL Report", list(query_map.keys()))

if st.button("🔍 Run Report"):
    result_df = pd.read_sql(query_map[selected_report], engine)
    st.dataframe(result_df, use_container_width=True)

    csv = result_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Results as CSV", csv, f"{selected_report.replace(' ', '_')}.csv", "text/csv")
