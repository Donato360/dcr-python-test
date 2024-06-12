import sqlite3

# Global variable 'conn', holding the database connection.
conn = None


# Class 'DBO': handle database operations for the SQLite database countries.db
class DBO:
    DB_FILE = "../data/countries.db"

    # __init__ method is called when an instance of DBO is created.
    def __init__(self):
        # Access to global 'conn' variable defined outside of the class
        global conn

        # Check if the database connection does not already exist before establishing a new connection to the SQLite database countries.db
        if conn is None:
            conn = sqlite3.connect(self.DB_FILE)
        # cursor object used to execute SQL commands
        self.cursor = conn.cursor()

        # 'data' variable: store fetched data from the database
        self.data = None

# Class 'Region': inherits from the 'DBO' class.


class Region(DBO):
    # Method to insert a new region with the given 'name' into the 'region' table
    def create(self, name):
        insert_query = "INSERT INTO region (name) VALUES (?)"
        # Executes the SQL insert query with the provided name parameter.
        self.cursor.execute(insert_query, (name,))
        conn.commit()

    # Method to fetch a region by 'name'
    def get_by_name(self, name):
        select_query = "SElECT id, name FROM region WHERE name=?"
        self.cursor.execute(select_query, (name,))
        region_data = self.cursor.fetchone()
        if not region_data:
            return False
        # Extract column headers from the cursor description
        headers = [header[0] for header in self.cursor.description]
        # Combine headers and row data into a dictionary
        self.data = {k: v for k, v in zip(headers, region_data)}
        return True

    # Method to fetch an existing region or create a new one if it does not exist
    def get_or_create_by_name(self, name):
        self.get_by_name(name)
        if not self.data:
            self.create(name)
        self.get_by_name(name)


# Class 'Country': Minherits from the 'DBO' class
class Country(DBO):
    # Method insert: inserts a new country with provided details into the 'country' table
    def insert(self, name, alpha2Code, alpha3Code, population, region_id, topLevelDomain, capital):
        insert_query = (
            "INSERT INTO country (name, alpha2Code, alpha3Code, population, topLevelDomain, capital, "
            "region_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
        )
        self.cursor.execute(
            insert_query, (name, alpha2Code, alpha3Code,
                           population, region_id, topLevelDomain, capital)
        )
        conn.commit()
        # Refreshes local data by fetching the inserted country
        self.get_by_name(name)

    # Method update: updates an existing country's details in the 'country' table
    def update(self, name, alpha2Code, alpha3Code, population, region_id, topLevelDomain, capital):
        update_query = (
            "UPDATE country SET "
            "name = ?, alpha3Code = ?, population = ?, topLevelDomain = ?, capital = ?, region_id = ? "
            "WHERE alpha2Code = ?"
        )
        self.cursor.execute(
            update_query, (name, alpha3Code, population,
                           topLevelDomain, capital, region_id, alpha2Code)
        )
        conn.commit()
        # Refreshes local data by fetching the updated country
        self.get_by_name(name)

    # Method get_by_name: fetches a country by its name
    def get_by_name(self, name):
        select_query = "SElECT * FROM country WHERE name=?"
        self.cursor.execute(select_query, (name,))
        region_data = self.cursor.fetchone()
        if not region_data:
            return False
        headers = [header[0] for header in self.cursor.description]
        self.data = {k: v for k, v in zip(headers, region_data)}
        return self.data

    @classmethod
    # Classmethod list_all: lists all entries from the 'country' table along with their associated 'region'.
    def list_all(cls):
        dbo = DBO()
        select_statement = """
            SELECT c.name AS country_name, c.alpha2Code, c.alpha3Code,
                    c.population, r.name AS region_name, c.topLevelDomain, c.capital
                FROM country c
                JOIN region r ON c.region_id = r.id;
            """
        dbo.cursor.execute((select_statement))
        headers = [header[0] for header in dbo.cursor.description]

        for row in dbo.cursor.fetchall():
            obj = cls()
            obj.data = {k: v for k, v in zip(headers, row)}
            yield obj
