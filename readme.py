# SecureCheck: A Python-SQL Digital Ledger for Police Post Logs

SecureCheck is a real-time digital ledger system that enables efficient monitoring and querying of police check post activity. It integrates Python, MySQL, and Streamlit to analyze and visualize traffic stop data through an interactive dashboard.

# Project Structure 

securecheck_project/
├── create_database.sql       # SQL script to create database & tables
├── db_config.py              # MySQL database configuration
├── traffic_stops.csv         # Dataset for traffic stops
├── insert_data.py            # Script to load CSV data into MySQL
├── data_processing.py        # Python functions to perform SQL queries
├── queries.sql               # Contains 20 categorized SQL queries
├── streamlit_app.py          # Streamlit-based dashboard
└── readme.py                 # Script for auto-generating README (optional)

# Features

Load and store traffic data from CSV to MySQL

Categorized 20 SQL queries:

Medium: Gender stats, violations, vehicle counts

Hard: Multi-condition filters, joins, aggregations

Real-time dashboard with Streamlit

Visual representation of queries using charts & metrics

# Technologies Used
Python 3.12

MySQL

Pandas

Streamlit

Matplotlib / Seaborn (if used)

# Getting Started
1. Clone the repository

git clone https://github.com/yourusername/securecheck_project.git
cd securecheck_project

2. Set up MySQL Database
Open create_database.sql and execute it in your MySQL environment to create tables.

3. Configure Database Connection
Edit db_config.py with your MySQL credentials:

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'securecheck'
}

4. Load the Data
python insert_data.py

5. Launch the Dashboard
streamlit run streamlit_app.py

# SQL Query Categories

| Level  | Category             | Example Queries                             |
| ------ | -------------------- | ------------------------------------------- |
| Medium | Basic Analysis       | Gender count, Arrest reasons, Vehicle type  |
| Hard   | Complex Conditions   | Combined filters, Group By, Aggregates      |
| Hard   | Joins and Subqueries | Cross-reference drivers with stop locations |

All queries can be found in queries.sql.

# Example Dashboard Output
Top locations with highest stops

Pie chart of driver gender distribution

Bar chart of arrest reasons

Query-based custom results with filters

# License
This project is for educational use only.