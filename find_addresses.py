"""
Find Addresses by Street Number or Street Name, Country, City, and Zip Code in OSM PBF

This script parses a local OpenStreetMap PBF (.pbf) file and finds all addresses
with a specified street number OR street name, country, city, and zip code (case-insensitive).
It prints Google Maps search links for each result.

Usage:
1. Place your OSM PBF file (e.g., planet-250818.osm.pbf) in the specified directory.
2. Run the script: python find_addresses.py
3. Enter the street number or street name, country, city, and zip code when prompted.

Requirements:
- Python 3.x
- osmium library (install with: pip install osmium)

Author: GitHub Copilot
"""

import osmium
import urllib.parse

class AddressFinder(osmium.SimpleHandler):
    """
    Osmium handler to find addresses with a specific street number OR street name,
    country, city, and zip code (case-insensitive).
    """
    def __init__(self, street_number_or_name, country, city, postcode):
        super().__init__()
        self.street_number_or_name = street_number_or_name.lower()
        self.country = country.lower()
        self.city = city.lower()
        self.postcode = postcode.lower()
        self.addresses = []

    def node(self, n):
        tags = n.tags
        city_tag = tags.get('addr:city', '').lower()
        country_tag = tags.get('addr:country', '').lower()
        postcode_tag = tags.get('addr:postcode', '').lower()
        housenumber = tags.get('addr:housenumber', '').lower()
        street = tags.get('addr:street', '').lower()
        if (
            (housenumber == self.street_number_or_name or street == self.street_number_or_name) and
            city_tag == self.city and
            country_tag == self.country and
            (self.postcode == "" or postcode_tag == self.postcode)
        ):
            address_parts = []
            if 'addr:housenumber' in tags:
                address_parts.append(tags['addr:housenumber'])
            if 'addr:street' in tags:
                address_parts.append(tags['addr:street'])
            if 'addr:city' in tags:
                address_parts.append(tags['addr:city'])
            if 'addr:postcode' in tags:
                address_parts.append(tags['addr:postcode'])
            if 'addr:country' in tags:
                address_parts.append(tags['addr:country'])
            address_str = ', '.join(address_parts)
            self.addresses.append(address_str)

    def way(self, w):
        tags = w.tags
        city_tag = tags.get('addr:city', '').lower()
        country_tag = tags.get('addr:country', '').lower()
        postcode_tag = tags.get('addr:postcode', '').lower()
        housenumber = tags.get('addr:housenumber', '').lower()
        street = tags.get('addr:street', '').lower()
        if (
            (housenumber == self.street_number_or_name or street == self.street_number_or_name) and
            city_tag == self.city and
            country_tag == self.country and
            (self.postcode == "" or postcode_tag == self.postcode)
        ):
            address_parts = []
            if 'addr:housenumber' in tags:
                address_parts.append(tags['addr:housenumber'])
            if 'addr:street' in tags:
                address_parts.append(tags['addr:street'])
            if 'addr:city' in tags:
                address_parts.append(tags['addr:city'])
            if 'addr:postcode' in tags:
                address_parts.append(tags['addr:postcode'])
            if 'addr:country' in tags:
                address_parts.append(tags['addr:country'])
            address_str = ', '.join(address_parts)
            self.addresses.append(address_str)

def main():
    """
    Main function to prompt user input and print Google Maps search links for matching addresses.
    """
    osm_file = '/home/panagiotisdimitriou/Downloads/planet-250818.osm.pbf'
    street_number_or_name = input("Enter the street number OR street name to search for: ").strip().lower()
    country = input("Enter the country to search for (e.g., CY): ").strip().lower()
    city = input("Enter the city to search for: ").strip().lower()
    postcode = input("Enter the zip code (leave blank to ignore): ").strip().lower()
    finder = AddressFinder(street_number_or_name, country, city, postcode)
    finder.apply_file(osm_file, locations=True)
    if finder.addresses:
        print(f"Google Maps search links for addresses with street number or street name '{street_number_or_name}', country '{country}', city '{city}', zip code '{postcode}':")
        for addr in finder.addresses:
            query = urllib.parse.quote(addr)
            maps_url = f"https://www.google.com/maps/search/?api=1&query={query}"
            print(maps_url)
    else:
        print(f"No addresses found with street number or street name '{street_number_or_name}', country '{country}', city '{city}', zip code '{postcode}'.")

if __name__ == "__main__":
    main()
