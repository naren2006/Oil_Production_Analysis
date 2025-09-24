import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# The URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_oil_production'

# Add a User-Agent header to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

# Fetch the page using the URL and the headers
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the page.")
else:
    print(f"Failed to fetch page. Status code: {response.status_code}")
    exit()

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the correct table. Wikipedia tables often have the class "wikitable".
table = soup.find('table', {'class': 'wikitable'})

if table is None:
    print("Could not find the data table. The page structure might have changed.")
    exit()

# --- START OF THE FIX ---
# Extract the table headers from the first table row (`tr`) instead of `thead`
headers = []
for th in table.find('tr').find_all('th'):
    headers.append(th.text.strip())
# --- END OF THE FIX ---


# Extract the rows
rows = []
for tr in table.find('tbody').find_all('tr'):
    cells = []
    # This check ensures we only process rows with actual data cells (td)
    if tr.find_all('td'):
        for td in tr.find_all('td'):
            cells.append(td.text.strip())
        rows.append(cells)
        
# Create a Pandas DataFrame
df = pd.DataFrame(rows, columns=headers[:len(rows[0])])

print("Initial data extracted:")
print(df.head())

# --- DATA CLEANING ---
print("\nCleaning data...")

df = df.iloc[:, [0, 1]]
df.columns = ['Country', 'Production_bbl_per_day']

df['Production_bbl_per_day'] = df['Production_bbl_per_day'].apply(lambda x: re.sub(r'\[\d+\]', '', x))
df['Production_bbl_per_day'] = df['Production_bbl_per_day'].str.replace(',', '')
df['Production_bbl_per_day'] = pd.to_numeric(df['Production_bbl_per_day'])

print("\nCleaned DataFrame:")
print(df.head())
print("\nData types:")
df.info()

# Save the cleaned data to a CSV file
df.to_csv('oil_production_data.csv', index=False)
print("\nCleaned data successfully saved to oil_production_data.csv")