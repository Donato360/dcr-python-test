from db import DBO


class CreateDB(DBO):
    # SQL command to create a table named 'region' if it does not already exist.
    # The 'region' table will have two fields, 'id' and 'name'.
    # 'id' is the primary key and 'name' is unique across records.
    CREATE_REGIONS = """
        CREATE TABLE IF NOT EXISTS region (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        );"""

    # SQL command to create a table named 'country' if it does not already exist.
    # The 'country' table has fields: 'id', 'name', 'alpha2Code', 'alpha3/Code', 'population', 'region_id'.
    # 'id' is the primary key, 'name' is unique, and 'region_id' is a foreign key.
    CREATE_COUNTRY = """
        CREATE TABLE IF NOT EXISTS country (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            alpha2Code TEXT,
            alpha3Code TEXT,
            population INTEGER,
            region_id INTEGER,
            FOREIGN KEY (region_id) REFERENCES region(id)
        );"""

    # Method 'run': executes the SQL commands to create the 'region' and 'country' tables.
    def run(self):
        self.cursor.execute(self.CREATE_REGIONS)
        self.cursor.execute(self.CREATE_COUNTRY)


if __name__ == "__main__":
    CreateDB().run()
