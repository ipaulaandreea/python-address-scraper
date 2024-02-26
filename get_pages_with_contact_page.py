from requests.exceptions import ProxyError, ConnectTimeout
from get_country import my_object
import requests
from extract_db import df
from turn_db_entries_into_list import domain_list;
patterns = [
    '/contact',
    '/contact-us',
    '/support',
    '/help',
    '/about/contact',
    '/about',
    '/about-us'
]

proxies = {
    'http': 'http://user:password@10.10.1.10:3128',
    'https': 'https://user:password@10.10.1.11:1080',
}

def lookup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        return response
    except (ProxyError, ConnectTimeout) as e:
        print(f"Request failed for {url}: {e}")
    except requests.RequestException as e:
        print(f"Request failed for {url}: {e}")
    return None

def check_contact_page(websites, patterns):
    results = []
    for website in websites:
        found_contact_page = False 
        for pattern in patterns:
            contact_url = f"http://{website}{pattern}"
            response = lookup(contact_url)
            
            if response and response.status_code == 200:
                results.append((website, contact_url)) 
                found_contact_page = True
                break

        if not found_contact_page:
            continue 

    return results

websites_with_contact_pages = check_contact_page(domain_list, patterns)

print(websites_with_contact_pages)

