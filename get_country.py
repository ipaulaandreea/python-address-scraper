from urllib.parse import urlparse
import tldextract
from challenge1 import df
my_object = df['domain'].tolist()


def extract_tlds(websites):
    tld_dict = {}
    for website in websites:
        extracted = tldextract.extract(website)
        tld = extracted.suffix
        tld_dict[website] = f".{tld}" if tld else ''
    return tld_dict


tlds_dict = extract_tlds(my_object)
domains_and_suffixes = tlds_dict.items()
domains_and_suffixes_list = list(domains_and_suffixes)
