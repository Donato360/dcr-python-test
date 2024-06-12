import json
from collections import defaultdict

# Constants for file paths
INPUT_FILENAME = '../data/countries.json'
OUTPUT_FILENAME = 'region_stats.json'


class CountryStats:
    # Declare stats with slots attribute enabling faster attribute access and reduced memory usage
    __slots__ = ['stats']

    def __init__(self):
        # Initialize stats property
        self.stats = None

    def compute_statistics(self, input_filename):
        # Initialize region_stats dictionary with a lambda that returns a new stats dictionary
        region_stats = defaultdict(
            lambda: {"number_countries": 0, "total_population": 0})

        # Open and read input file containing JSON data
        with open(input_filename, 'r') as file:
            data = json.load(file)
            for country in data:
                # Extract the region and population of each country
                region = country['region']
                population = country['population']

                # Update the counts and totals for the current region
                stats = region_stats[region]
                stats['number_countries'] += 1
                stats['total_population'] += population

        # After processing all countries, save the statistics
        self.stats = {"regions": [{"name": region,
                                   "number_countries": stats['number_countries'],
                                   "total_population": stats['total_population']}
                                  for region, stats in region_stats.items()]}

    def write_statistics_to_file(self, output_filename):
        # Write the computed statistics to a file in a pretty-printed JSON format
        with open(output_filename, 'w') as file:
            json.dump(self.stats, file, indent=4)

    def print_statistics(self):
        # Write the computed statistics to the console in a pretty-printed JSON format
        print(json.dumps(self.stats, indent=4))


def main():
    # Create an instance of CountryStats class
    country_stats = CountryStats()
    # Compute statistics using the input file
    country_stats.compute_statistics(INPUT_FILENAME)
    # Print out the statistics to the console
    country_stats.print_statistics()
    # Write the statistics to the output file
    country_stats.write_statistics_to_file(OUTPUT_FILENAME)


# Entry point for script execution
if __name__ == "__main__":
    main()
