from preprocessing_data import save_domains_contact_paths_to_mysql
from get_contact_info import process_urls
from check_for_address_word import check_for_address_word
from get_address_from_other_services import get_address_from_other_services
from update_domains_in_mysql import update_domains_in_mysql

def main():
    domains = save_domains_contact_paths_to_mysql()
    contact_urls = [domain.contact_url for domain in domains if domain.address_path != 'NULL']
    addresses = process_urls(contact_urls)
    for i, domain in enumerate([d for d in domains if d.address_path != 'NULL']):
        if addresses[i]: 
            domain.strategy = 'strategy 1'
            domain.address = addresses[i] 
            domain.finished = 'Y'
        
        else: 
            domain.strategy = 'strategy 2'
            is_word_on_page = check_for_address_word(domain.domain)
            if is_word_on_page:
                result = process_urls(domain.domain)
                if result.contact_url != ' ':
                    domain.finished = 'Y'
                else:
                    domain.strategy = 'strategy 3'
                    get_address_from_other_services(domain.domain)
                    domain.finished = 'Y'
            else:
                domain.strategy = 'strategy 3'
                get_address_from_other_services(domain.domain)
                domain.finished = 'Y'
            

    update_domains_in_mysql(domains)


main()
