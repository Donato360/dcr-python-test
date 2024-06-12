import json
import requests
from db import Country, Region


# Class LoadData: loads and updates country data
class LoadData:
    # URL to fetch country data in JSON format
    DATA_URL = "https://storage.googleapis.com/dcr-django-test/countries.json"

    def __init__(self):
        # Initialize a cache for regions
        self.regions = {}

    def get_raw_data(self):
        # HTTP GET request to fetch the raw country data
        response = requests.get(self.DATA_URL)
        response.raise_for_status()  # notifications for bad responses
        return response.json()

    def insert_or_update_country_data(self, row):
        # Initialize an instance of the Country model
        country_object = Country()

        # Check if a country with the given name already exists in the database
        existing_country = country_object.get_by_name(row['name'])

        if existing_country:
            update_needed = False

            # Get the keys of the existing country if it is a dictionary
            existing_fields = existing_country.keys()

            # Compare each field of the existing record to see if an update is needed
            for field in existing_fields:
                if field in row and existing_country[field] != row[field]:
                    existing_country[field] = row[field]
                    update_needed = True
            if update_needed:
                # Serialize topLevelDomain if present and it's a list
                serialized_top_level_domain = json.dumps(
                    row['topLevelDomain']) if 'topLevelDomain' in row and isinstance(row['topLevelDomain'], list) else None

                # Update operation on the existing country entry in the database
                country_object.update(name=existing_country['name'],
                                      alpha2Code=existing_country['alpha2Code'],
                                      alpha3Code=existing_country['alpha3Code'],
                                      population=existing_country['population'],
                                      region_id=existing_country['region_id'],
                                      topLevelDomain=serialized_top_level_domain,
                                      capital=existing_country['capital']
                                      )
                print(f"Country {row['name']} updated.")
            else:
                print(f"Country {row['name']} is already up to date.")
        else:
            # If no existing country found, prepare to insert new country data
            serialized_top_level_domain = json.dumps(
                row['topLevelDomain']) if 'topLevelDomain' in row and isinstance(row['topLevelDomain'], list) else None

            region_name = row.get("region", "Unknown")
            region_id = self.get_region_id(region_name)

            # If the country does not exist, insert it into the database
            country_object.insert(name=row['name'],
                                  alpha2Code=row['alpha2Code'],
                                  alpha3Code=row['alpha3Code'],
                                  population=row['population'],
                                  region_id=region_id,
                                  topLevelDomain=serialized_top_level_domain,
                                  capital=row['capital']
                                  )
            print(f"Country {row['name']} inserted.")

    def get_region_id(self, region_name):
        # Check if the region is already cached
        if region_name not in self.regions:
            region = Region()
            # Get an existing region or create a new one if it doesn't exist
            region.get_or_create_by_name(region_name)
            self.regions[region.data["name"]] = region.data["id"]
        return self.regions[region_name]

    def run(self):
        # Fetch raw data from the DATA_URL
        data = self.get_raw_data()

        # Iterate over each country in the data and insert or update its record
        for row in data:
            self.insert_or_update_country_data(row)


if __name__ == "__main__":
    LoadData().run()
