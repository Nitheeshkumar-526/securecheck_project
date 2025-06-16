from data_processing import clean_data
from db_config import get_engine

# Load and clean the dataset
df = clean_data("traffic_stops.csv")

# Connect to DB
engine = get_engine()

# Insert into MySQL
df.to_sql("traffic_stops", engine, if_exists='append', index=False)

print("✅ Data inserted successfully!")
