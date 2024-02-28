from turn_db_entries_into_list import domain_list;
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from requests.exceptions import ProxyError, ConnectTimeout, HTTPError, RequestException
import requests

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
        response.raise_for_status()
        return response
    except (ProxyError, ConnectTimeout, HTTPError, RequestException) as e:
        print(f"Request failed for {url}: {e}")
    return None

def check_single_website(website):
    patterns = [
    '/contact',
    '/contact-us',
    '/about',
    '/about-us',
    '/about/contact',
    '/support',
    '/help',
]
    for pattern in patterns: 
        contact_url = f"http://{website}{pattern}"
        response = lookup(contact_url)
        if response and response.status_code == 200: 
            return (website, contact_url)
        else:
            continue
    return (website, None)

def check_contact_page(websites):
    start = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=12) as executor:  
        future_to_website = {executor.submit(check_single_website, website): website for website in websites}
        for future in as_completed(future_to_website): 
            website, contact_url = future.result()
            if contact_url:
                results.append((website, contact_url))    
    end = time.time()
    print("Execution time:", (end-start) * 1000, "ms")
    return results


websites_with_contact_pages = check_contact_page(domain_list)

print(websites_with_contact_pages)
