import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime

# Read CSV file
df = pd.read_csv("/Users/kunika/Downloads/try.csv")



def parse_mixed_date(date):
    formats = ["%Y-%m-%d", "%d/%m/%Y"]  # List of potential formats
    for fmt in formats:
        try:
            return datetime.strptime(date, fmt)  # Try each format
        except ValueError:
            continue
    raise ValueError(f"Date format for '{date}' is not recognized.")

# Apply the function to your column
df['transaction_date'] = df['transaction_date'].apply(parse_mixed_date)
df['transaction_type'] = df['transaction_type'].str.title()
df['user_name']=df['user_name'].str.title()

# Ensure date format is consistent


# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="postgres", user="postgres", password="", host="localhost"
)
cursor = conn.cursor()

# Prepare and execute insert query
for index, row in df.iterrows():
    cursor.execute(
        sql.SQL("INSERT INTO public.expenses (user_name, category, subcategory, amount, transaction_type, transaction_date, year, month, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"),
        [row['user_name'], row['category'], row['subcategory'], row['amount'], row['transaction_type'], row['transaction_date'], row['year'], row['month'], row['notes']]
    )

# Commit and close connection
conn.commit()
cursor.close()
conn.close()
