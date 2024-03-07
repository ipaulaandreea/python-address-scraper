from generate_sitemap import process_domains_in_parallel
from preprocessing_data import preprocess_data

def main():
    domains = preprocess_data()
    process_domains_in_parallel(domains[25:35])
    
main()
