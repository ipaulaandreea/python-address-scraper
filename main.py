from preprocessing_data import save_domains_contact_paths_to_mysql
from get_contact_pages import get_first_20_domains_from_db
from get_contact_info import process_urls
from get_address_from_other_services import get_address_from_other_services
from update_domains_in_mysql import update_domains_in_mysql
from organize_contact_info import organize_contact_info
from add_organized_addresses_to_db import add_organized_addresses_to_db

### idea - make strategy 1 group and strategy 2 group and check them in one go
def main():
    # domains = save_domains_contact_paths_to_mysql()
    domains = get_first_20_domains_from_db()
    batch_for_db = []

    for domain in domains:
        urls_to_process = [domain['contact_url']] if domain['contact_url'] is not None else [f"http://{domain['domain']}"]
        address_str_results = process_urls(urls_to_process)
        # print(address_str_results)
        address_str = ''
        strategy = ''
        finished = 'N'
        organized_address = {}
        
        if address_str_results:
            for url, address_str in address_str_results:
                if address_str:
                    organized_address = organize_contact_info(address_str)
                    strategy = 'strategy 1' if domain['contact_url'] is not None else 'strategy 2'
                    finished = 'Y'
                    break  # Exit the loop after finding the first valid address
                else:
                    strategy = 'strategy 3'
                    address_str = get_address_from_other_services(url)  # Assuming this returns a single address string
                    if address_str:
                        organized_address = organize_contact_info(address_str)
                        finished = 'Y'
                        # No need for a break here since get_address_from_other_services is called for each URL
        else:
            # Fallback strategy if no URLs to process
            strategy = 'strategy 3'
            address_str = get_address_from_other_services(domain['domain'])  # Fallback to domain if no contact_url
            if address_str:
                organized_address = organize_contact_info(address_str)
                finished = 'Y'

        # Check if organized_address has been populated
        if organized_address:
            address_tuple = (
                domain['domain'],
                organized_address.get('country', 'N/A'),
                organized_address.get('city', 'N/A'),
                organized_address.get('region', 'N/A'),
                organized_address.get('postcode', 'N/A'),
                organized_address.get('road', 'N/A'),
                organized_address.get('road_number', 'N/A')
            )
            batch_for_db.append(address_tuple)

    # After processing all domains, add organized addresses to the database
    if batch_for_db:
        add_organized_addresses_to_db(batch_for_db)

main()
