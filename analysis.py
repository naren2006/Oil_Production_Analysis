import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the database file
DATABASE_FILE = 'energy_data.db'

# Create a connection to the database
conn = sqlite3.connect(DATABASE_FILE)
print(f"Successfully connected to {DATABASE_FILE}")

# --- Query 1: Top 10 Producers ---
query1 = """
    SELECT Country, Production_bbl_per_day
    FROM oil_production
    ORDER BY Production_bbl_per_day DESC
    LIMIT 10;
"""
top_10_producers = pd.read_sql_query(query1, conn)
print("\n--- Top 10 Oil Producers ---")
print(top_10_producers)

# --- VISUALIZATION 1 ---
# Create a horizontal bar chart for the top 10 producers
plt.figure(figsize=(10, 6)) # Set the figure size for better readability
sns.barplot(x='Production_bbl_per_day', y='Country', data=top_10_producers, palette='viridis')
plt.title('Top 10 Oil Producing Countries')
plt.xlabel('Production (Barrels per Day)')
plt.ylabel('Country')
plt.tight_layout() # Adjust layout to make sure everything fits
plt.savefig('top_10_producers.png') # Save the chart to a file
plt.show() # Display the chart


# --- Query 2: Middle-Tier Producers ---
query2 = """
    SELECT Country, Production_bbl_per_day
    FROM oil_production
    WHERE Production_bbl_per_day BETWEEN 1000000 AND 3000000
    ORDER BY Production_bbl_per_day DESC;
"""
middle_tier_producers = pd.read_sql_query(query2, conn)
print("\n--- Middle-Tier Producers (1M to 3M bbl/day) ---")
print(middle_tier_producers)

# --- VISUALIZATION 2 ---
# Create a vertical bar chart for middle-tier producers
plt.figure(figsize=(12, 7))
sns.barplot(x='Country', y='Production_bbl_per_day', data=middle_tier_producers, palette='plasma')
plt.title('Middle-Tier Oil Producers (1M to 3M bbl/day)')
plt.xlabel('Country')
plt.ylabel('Production (Barrels per Day)')
plt.xticks(rotation=45, ha='right') # Rotate country names for readability
plt.tight_layout()
plt.savefig('middle_tier_producers.png')
plt.show()


# --- Query 3: World Production Summary ---
query3 = """
    SELECT SUM(Production_bbl_per_day) AS Total_Production,
           AVG(Production_bbl_per_day) AS Average_Production_per_Country
    FROM oil_production;
"""
world_summary = pd.read_sql_query(query3, conn)
print("\n--- World Production Summary ---")
# For summary statistics, a simple print is often more effective than a chart
total_prod = world_summary['Total_Production'].iloc[0]
avg_prod = world_summary['Average_Production_per_Country'].iloc[0]
print(f"Total Production (from this list): {total_prod:,.0f} bbl/day")
print(f"Average Production per Country: {avg_prod:,.0f} bbl/day")


# Close the connection to the database
conn.close()
print("\nDatabase connection closed.")