import requests
import xml.etree.ElementTree as ET
from get_contact_info import process_urls
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed


def find_sitemap_and_extract_urls(base_url):
    sitemap_variants = ['sitemap.xml', 'index.xml',
                        'sitemap_index.xml', 'wp-sitemap.xml']
    urls = []

    for variant in sitemap_variants:
        try:
            sitemap_url = f"http://{base_url}/{variant}"
            response = requests.get(sitemap_url, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                namespaces = {
                    'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                for url in root.findall('.//ns:url/ns:loc', namespaces):
                    urls.append(url.text)

                if urls:
                    process_urls(urls)
                    return urls
        except requests.exceptions.Timeout:
            print(f"Timeout occurred while processing {sitemap_url}")
        except Exception as e:
            print(f"Error processing {sitemap_url}: {e}")

    if not urls:
        homepage = f"http://{base_url}"
        print(f'Did not find sitemap for {base_url}, adding homepage.')
        urls.append(homepage)
        process_urls(urls)

    return urls

def process_domains_in_parallel(domains, max_workers=8, batch_size=5):
    for i in range(0, len(domains), batch_size):
        if i % 10 == 0:
            print("at index", i)
        batch_domains = domains[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_domain = {executor.submit(find_sitemap_and_extract_urls, domain): domain for domain in batch_domains}  
            for future in as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    urls = future.result() 
                    print(f"Processed {domain}, Extracted URLs: {urls}")
                except Exception as exc:
                    print(f"{domain} generated an exception: {exc}")

