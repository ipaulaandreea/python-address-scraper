import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
import concurrent
import requests
from update_db import insert_page_content_to_db
from organize_contact_info import organize_contact_info
import json


address_regexes = [
    r'\b(P\.?O\.? BOX \d+ [A-Za-z\s]+, [A-Z]{2} \d{5})(?=\S?)',
    r'\d+[\s\w]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Circle|Cir|Drive|Dr|Court|Ct|Parkway|Pkwy|Square|Sq|Trail|Trl|Way)\W+(?:[A-Za-z]+\W+){1,3},?\s*(?:[A-Z]{2})?\s*\d{5}(-\d{4})?',
    r'\d+\s(?:[A-Za-z]+\s){1,3}(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Circle|Cir|Drive|Dr|Court|Ct|Parkway|Pkwy|Square|Sq|Trail|Trl|Way|Platz|Straße|Weg|Allee|Piazza|Via|Rua|Calle)\W+(?:[A-Za-z]+\W+){1,3}\d{4,5}',
    r'\d+\s[\w\s]+(?:#\d+|Apt\s\d+|Suite\s\d+|Floor\s\d+|Unit\s\d+)?,?\s+(?:[A-Za-z]+\s)+,?\s+(?:[A-Z]{2}\s+)?\d{5}(-\d{4})?',
    r'[A-Z]{1,2}\d{1,2}\s?\d[A-Z]{2}',
    r'\b(?:P\.?O\.?\s?BOX)\s+\d+\s+([A-Za-z\s]+),\s*([A-Z]{2})\s*(\d{5}(-\d{4})?)\b',
    r'/^ *((#\d+)|((box|bin)[-. \/\\]?\d+)|(.*p[ \.]? ?(o|0)[-. \/\\]? *-?((box|bin)|b|(#|n|num|number)?\d+))|(p(ost|ostal)? *(o(ff(ice)?)?)? *((box|bin)|b)? *(#|n|num|number)*\d+)|(p *-?\/?(o)? *-?box)|post office box|((box|bin)|b) *(#|n|num|number)? *\d+|(#|n|num|number) *\d+)/i',
    r'\b\d+\s[\w\s-]+,\s(?:Unit\s\w+-\d+,)?\s[\w\s-]+,\s[A-Z]{2}\s\d{5}\b',
    r'(\d+\s[A-Za-z\s]+(?:Street|St|Ave|Avenue|Road|Rd|Boulevard|Blvd|Lane|Ln|Circle|Cir|Drive|Dr|Court|Ct|Parkway|Pkwy|Square|Sq|Trail|Trl|Way)\.?\s?(?:S\.?|N\.?|E\.?|W\.?)?)(?:\s-\sPO\sBox\s\d+)?,\s([A-Za-z\s]+),\s([A-Z]{2})\s(\d{5})',
    r'(\d+\s[A-Za-z\s]+(?:Avenue|Ave|Street|St|Road|Rd|Boulevard|Blvd|Lane|Ln|Circle|Cir|Drive|Dr|Court|Ct|Parkway|Pkwy|Square|Sq|Trail|Trl|Way)),\s*(?:Suite|Ste|Unit|Apt|#)?\s*([\d\-]+)?\s*([A-Za-z\s]+),\s*([A-Z]{2})\s*(\d{5})',
    r'\d+\s\w+\.\w+\sSt\.\s\w+,\s\w{2}\s\d{5}',
    r'\b\d+\s+[A-Za-z0-9\s]*\b(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Parkway|Pkwy|Circle|Cir|Square|Sq|Trail|Trl|Way|Terrace|Terr|Place|Pl)(?:,?\s+(?:Suite|Ste|Unit|Apt|#)\s+\w+)?,?\s+[A-Za-z\s]+,\s+[A-Z]{2}\s+\d{5}(-\d{4})?\b',
    r'\d+\s+[A-Z0-9][a-z0-9\s]*\b(?:Street|St|Rd|Road|Ave|Avenue|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Parkway|Pkwy|Circle|Cir|Square|Sq|Trail|Trl|Way|Terrace|Terr|Place|Pl)(?:,?\s+Suite\s+[A-Z0-9]+)?,?\s+[A-Za-z\s]+,\s+[A-Z]{2}\s+\d{5}(-\d{4})?',
    r'\b\d+\s+[A-Za-z0-9\s]*\b(?:St|Street|Rd|Road|Ave|Avenue|Blvd|Boulevard|Ln|Lane|Dr|Drive|Ct|Court|Pkwy|Parkway|Cir|Circle|Sq|Square|Trl|Trail|Way|Terr|Terrace|Pl|Place)\b(?:\s+(?:Suite|Ste|Unit|Apt|#)\s*\w+)?,?\s+[A-Za-z\s]+,\s+[A-Z]{2}\s+\d{5}(-\d{4})?'

]

address_patterns = [re.compile(pattern, re.IGNORECASE)
                    for pattern in address_regexes]


def get_contact_info(link):
    found_addresses = []
    organized_addresses = []
    keywords = ['contact', 'address', 'location', 'office',
                'warehouse', 'connect', 'house', 'headquarter']
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(link, headers=headers)
    except requests.RequestException as e:
        print(f"Failed to fetch {link} due to: {e}")
        return

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = ' '.join(soup.stripped_strings).lower()
            if any(keyword in text_content for keyword in keywords):

                for address_pattern in address_patterns:
                    matches = address_pattern.findall(
                        text_content, re.IGNORECASE)
                    for match in matches:
                        match_str = ' '.join(match) if isinstance(
                            match, tuple) else match

                        if match_str.strip() and len(match_str) >= 20:
                            found_addresses.append(match_str)
                if found_addresses:
                    try:
                        for found_address in found_addresses:
                            organized_address = organize_contact_info(
                                found_address)
                            organized_addresses.append(organized_address)
                        serialized_data = json.dumps(organized_addresses)
                        insert_page_content_to_db(
                            link, response.text, found_addresses, serialized_data)
                        print(f"Saved content for {link}")
                    except Exception as process_error:
                        print(
                            f"Error processing addresses for {link}: {process_error}")
                else:
                    print(f"Keyword found but no address match for {link}")
        except Exception as parse_error:
            print(f"Error parsing content from {link}: {parse_error}")


def process_urls(urls):
    for url in urls:
        get_contact_info(url)
