from deepparse.parser import AddressParser
address_parser = AddressParser(model_type="bpemb", device=0)


def organize_contact_info(address_string):
    print("Parsing", address_string)
    final_address = {
        'country': 'N/A', 
        'city': 'N/A',
        'region': 'N/A',
        'postcode': 'N/A',
        'road': 'N/A',
        'road_number': 'N/A',
    }
    try:
        parsed_address = address_parser(address_string)
        
        final_address.update({
            'city': parsed_address.Municipality or 'N/A',
            'region': parsed_address.Province or 'N/A',
            'postcode': parsed_address.PostalCode or 'N/A',
            'road': parsed_address.StreetName or 'N/A',
            'road_number': parsed_address.StreetNumber or 'N/A',
        })

        print(final_address)

    except Exception as e:
        print(f"Error parsing address '{address_string}': {e}")
    
    return final_address


def process_addresses_in_parallel(address_strings):
    organized_addresses = []
    for address_str in address_strings:
        organized_address = organize_contact_info(address_str)
        organized_addresses.append(organized_address)
    
    return organized_addresses
