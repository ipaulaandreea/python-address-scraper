import requests
from bs4 import BeautifulSoup
import re

address_regexes = [ 
    r'\b(P\.?O\.? BOX \d+ [A-Za-z\s]+, [A-Z]{2} \d{5})(?=\S?)',
    r'\d+[\s\w]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Circle|Cir|Drive|Dr|Court|Ct|Parkway|Pkwy|Square|Sq|Trail|Trl|Way)\W+(?:[A-Za-z]+\W+){1,3},?\s*(?:[A-Z]{2})?\s*\d{5}(-\d{4})?',
    r'\d+\s(?:[A-Za-z]+\s){1,3}(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Circle|Cir|Drive|Dr|Court|Ct|Parkway|Pkwy|Square|Sq|Trail|Trl|Way|Platz|Straße|Weg|Allee|Piazza|Via|Rua|Calle)\W+(?:[A-Za-z]+\W+){1,3}\d{4,5}',
    r'\d+\s[\w\s]+(?:#\d+|Apt\s\d+|Suite\s\d+|Floor\s\d+|Unit\s\d+)?,?\s+(?:[A-Za-z]+\s)+,?\s+(?:[A-Z]{2}\s+)?\d{5}(-\d{4})?',
    r'[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}',
    r'\b(?:P\.?O\.?\s?BOX)\s+\d+\s+([A-Za-z\s]+),\s*([A-Z]{2})\s*(\d{5}(-\d{4})?)\b',
    r'/^ *((#\d+)|((box|bin)[-. \/\\]?\d+)|(.*p[ \.]? ?(o|0)[-. \/\\]? *-?((box|bin)|b|(#|n|num|number)?\d+))|(p(ost|ostal)? *(o(ff(ice)?)?)? *((box|bin)|b)? *(#|n|num|number)*\d+)|(p *-?\/?(o)? *-?box)|post office box|((box|bin)|b) *(#|n|num|number)? *\d+|(#|n|num|number) *\d+)/i'
]

address_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in address_regexes]

def get_contact_info(links):
    addresses = []
    for link in links:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(link, headers=headers)
        
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            
            for address_pattern in address_patterns:
                matches = address_pattern.findall(text)
                for match in matches:
                    if match !='':
                        addresses.append(match) 
        else:
            print(f"Failed to fetch the page, status code: {response.status_code}")
    
    return addresses

urls = [

    ]


addresses = get_contact_info(urls)
print(addresses)
