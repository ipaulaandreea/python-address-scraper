import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
import concurrent
import requests


address_regexes = [ 
    r'\b(P\.?O\.? BOX \d+ [A-Za-z\s]+, [A-Z]{2} \d{5})(?=\S?)',
    r'\d+[\s\w]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Circle|Cir|Drive|Dr|Court|Ct|Parkway|Pkwy|Square|Sq|Trail|Trl|Way)\W+(?:[A-Za-z]+\W+){1,3},?\s*(?:[A-Z]{2})?\s*\d{5}(-\d{4})?',
    r'\d+\s(?:[A-Za-z]+\s){1,3}(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Circle|Cir|Drive|Dr|Court|Ct|Parkway|Pkwy|Square|Sq|Trail|Trl|Way|Platz|Straße|Weg|Allee|Piazza|Via|Rua|Calle)\W+(?:[A-Za-z]+\W+){1,3}\d{4,5}',
    r'\d+\s[\w\s]+(?:#\d+|Apt\s\d+|Suite\s\d+|Floor\s\d+|Unit\s\d+)?,?\s+(?:[A-Za-z]+\s)+,?\s+(?:[A-Z]{2}\s+)?\d{5}(-\d{4})?',
    r'[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}',
    r'\b(?:P\.?O\.?\s?BOX)\s+\d+\s+([A-Za-z\s]+),\s*([A-Z]{2})\s*(\d{5}(-\d{4})?)\b',
    r'/^ *((#\d+)|((box|bin)[-. \/\\]?\d+)|(.*p[ \.]? ?(o|0)[-. \/\\]? *-?((box|bin)|b|(#|n|num|number)?\d+))|(p(ost|ostal)? *(o(ff(ice)?)?)? *((box|bin)|b)? *(#|n|num|number)*\d+)|(p *-?\/?(o)? *-?box)|post office box|((box|bin)|b) *(#|n|num|number)? *\d+|(#|n|num|number) *\d+)/i',
    r'\b\d+\s[\w\s-]+,\s(?:Unit\s\w+-\d+,)?\s[\w\s-]+,\s[A-Z]{2}\s\d{5}\b'
]

address_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in address_regexes]

def get_contact_info(link):
    addresses = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            for address_pattern in address_patterns:
                matches = address_pattern.findall(text)
                for match in matches:
                    if match != '':
                        addresses.append(match)
                        break 
    except requests.RequestException as e:
        print(f"Failed to fetch {link} due to: {e}")

    return (link, addresses[0] if addresses else '')

def process_urls(urls):
    all_addresses = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_addresses = [executor.submit(get_contact_info, url) for url in urls]
        for future in concurrent.futures.as_completed(future_to_addresses):
            addresses = future.result()
            all_addresses.extend(addresses) 
    return all_addresses

urls = [
]
    
print(process_urls(urls))
