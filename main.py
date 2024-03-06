from get_contact_info import process_urls
from generate_sitemap import find_sitemap_and_extract_urls_for_domain

def main():
    domains = []
    urls = find_sitemap_and_extract_urls_for_domain(domains)
    process_urls(urls)
    

main()
