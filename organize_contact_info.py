from get_contact_info import process_urls
from concurrent.futures import ThreadPoolExecutor, as_completed
import pyap


def parse_address(address_string):
    address_parser = pyap.parse(address_string, country='US')
    if address_parser:
        parsed_address = address_parser[0]
        return {
            'country': "US",
            'city': parsed_address.city if parsed_address.city else "N/A",
            'region': parsed_address.region if parsed_address.region else "N/A",
            'postcode': parsed_address.postal_code if parsed_address.postal_code else "N/A",
            'road': parsed_address.street_name if parsed_address.street_name else "N/A",
            'road_number': parsed_address.street_number if parsed_address.street_number else "N/A"
        }
    else:
        print("No address found in:", address_string)
        return {
            'country': "N/A",
            'city': "N/A",
            'region': "N/A",
            'postcode': "N/A",
            'road': "N/A",
            'road_number': "N/A"
        }

def organize_contact_info(urls):
    address_strings = process_urls(urls)
    organized_addresses = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_address = {executor.submit(parse_address, address): address for address in address_strings}
        for future in as_completed(future_to_address):
            organized_addresses.append(future.result())

    return organized_addresses
