from requests.exceptions import ProxyError, ConnectTimeout
from get_country import my_object
import requests
from extract_db import df

patterns = [
    '/contact',
    '/contact-us',
    '/support',
    '/help',
    '/about/contact',
    '/about',
    '/about-us'
]
print(df)
dummy_pages = []

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
    results = {}
    for website in websites:
        results[website] = False 
        for pattern in patterns:
            contact_url = f"http://{website}{pattern}"
            response = lookup(contact_url) 
            
            if not response:
                continue 
                
            if response.status_code == 200:
                results[website] = contact_url
                break
    return results


contact_page_exists = check_contact_page(my_object[11:30], patterns)
websites_with_contact_pages=[]
for website, contact_url in contact_page_exists.items():
    websites_with_contact_pages.append({website, contact_url})
print(websites_with_contact_pages)

