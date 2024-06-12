from db import Country


class ListCountries:
    def run(self):
        # print out a list of countries and their attributes in a tabular format
        for i, country in enumerate(Country.list_all()):
            if i == 0:
                print("\t".join(country.data.keys()))
            print("\t".join(str(s) for s in country.data.values()))


if __name__ == "__main__":
    ListCountries().run()
