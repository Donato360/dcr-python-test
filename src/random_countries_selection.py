import sqlite3
import random
from tabulate import tabulate
from colorama import Fore, Style, init

# Database file path
DB_FILE = "../data/countries.db"


def get_random_countries(limit):
    # Connect to the SQLite database file
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Get the total number of records in the country table
    cursor.execute("SELECT COUNT(*) FROM country")
    total_records = cursor.fetchone()[0]

    # Select a 'limit' number of random row ids from the available records
    random_ids = random.sample(range(1, total_records + 1), limit)

    # Retrieve records with these random ids
    placeholders = ','.join('?' for _ in random_ids)
    select_query = f"""
    SELECT name, alpha2Code, alpha3Code, population, region_id, topLevelDomain, capital
    FROM country
    WHERE rowid IN ({placeholders})
    """

    # Execute the SQL query using the random ids
    cursor.execute(select_query, random_ids)
    records = cursor.fetchall()

    # Close the database connection
    conn.close()
    return records

# Define a function to stylize headers


def style_header(text):
    return f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}"


if __name__ == "__main__":
    # Initialize colorama
    init(autoreset=True)

    # Fetch 15 random countries from the database
    countries = get_random_countries(15)

   # Transform the tuple records into a list of dictionaries and color specific fields
    countries_dicts = [{
        'Name': country[0],
        'Alpha-2 Code': country[1],
        'Alpha-3 Code': country[2],
        'Population': country[3],
        'Region ID': country[4],
        # Using ANSI escape code to color Top Level Domain value green
        'Top Level Domain': f"\033[92m{country[5]}\033[0m",
        # Using ANSI escape code to color Capital value green
        'Capital': f"\033[92m{country[6]}\033[0m",
    } for country in countries]

    # Styled headers dictionary
    headers = {
        "Name": style_header("Name"),
        "Alpha-2 Code": style_header("Alpha-2 Code"),
        "Alpha-3 Code": style_header("Alpha-3 Code"),
        "Population": style_header("Population"),
        "Region ID": style_header("Region ID"),
        "Top Level Domain": style_header("Top Level Network Domain"),
        "Capital": style_header("Capital")
    }

    # Print the table with tabulate
    print(tabulate(countries_dicts, headers=headers, tablefmt="grid"))
