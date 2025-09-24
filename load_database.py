import sqlite3
import pandas as pd

# Define the name of your CSV file and the future database file
CSV_FILE = 'oil_production_data.csv'
DATABASE_FILE = 'energy_data.db'
TABLE_NAME = 'oil_production'

# 1. Read the data from the CSV file into a Pandas DataFrame
try:
    df = pd.read_csv(CSV_FILE)
    print(f"Successfully loaded {len(df)} rows from {CSV_FILE}")
except FileNotFoundError:
    print(f"Error: The file {CSV_FILE} was not found. Please make sure it's in the same directory.")
    exit()

# 2. Create a connection to the SQLite database
# The database file will be created if it doesn't exist
conn = sqlite3.connect(DATABASE_FILE)
print(f"Successfully connected to the database {DATABASE_FILE}")

# 3. Use the .to_sql() method from Pandas to write the DataFrame to a new table
# if_exists='replace': If the table already exists, it will be dropped and recreated.
# index=False: We don't want to save the Pandas index as a column in the SQL table.
df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
print(f"Data successfully loaded into the '{TABLE_NAME}' table.")

# 4. (Optional) Verify the data was loaded by running a query
print("\nVerifying data... Here are the first 5 rows from the SQL table:")
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 5")

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# 5. Close the database connection
conn.close()
print("\nDatabase connection closed.")