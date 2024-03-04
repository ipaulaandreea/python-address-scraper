from get_contact_info import process_urls
import pypostalwin

def organize_contact_info(urls):
    address_strings = process_urls(urls)
    organized_addresses = []
    for address_string in address_strings:
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
    organized_addresses.append(final_address)

    return final_address


parsed_address = [
    {'house': 'the white house'},
    {'house_number': '1600'},
    {'road': 'pennsylvania avenue nw'},
    {'city': 'washington'},
    {'state': 'dc'},
    {'postcode': '20500'},
    {'country': 'usa'}
]
