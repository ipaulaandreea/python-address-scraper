import pypostalwin
from concurrent.futures import ThreadPoolExecutor
import concurrent


def organize_contact_info(address_string):
    print("Parsing", address_string)
    try:
        parser = pypostalwin.AddressParser()
        parsed_address = parser.runParser(address_string)
        consolidated_address = {}
        for component_dict in parsed_address:
            for key, value in component_dict.items():
                consolidated_address[key] = value

        final_address = {
            'country': consolidated_address.get('country', 'N/A'),
            'city': consolidated_address.get('city', 'N/A'),
            'region': consolidated_address.get('state', 'N/A'),
            'postcode': consolidated_address.get('postcode', 'N/A'),
            'road': consolidated_address.get('road', 'N/A'),
            'road_number': consolidated_address.get('house_number', 'N/A'),
        }
    except Exception as e:
        print(f"Error parsing address '{address_string}': {e}")
        final_address = {
            'country': 'N/A',
            'city': 'N/A',
            'region': 'N/A',
            'postcode': 'N/A',
            'road': 'N/A',
            'road_number': 'N/A',
            'original_address': address_string
        }

    return final_address


def process_addresses_in_parallel(address_strings):
    organized_addresses = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_address = {executor.submit(
            organize_contact_info, addr): addr for addr in address_strings}
        for future in concurrent.futures.as_completed(future_to_address):
            address = future_to_address[future]
            try:
                organized_addresses.append(future.result())
            except Exception as exc:
                print(f'Address {address} generated an exception: {exc}')
    return organized_addresses
