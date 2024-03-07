import requests
import xml.etree.ElementTree as ET
from get_contact_info import process_urls
import concurrent.futures


def find_sitemap_and_extract_urls(base_url):
    sitemap_variants = ['sitemap.xml', 'index.xml',
                        'sitemap_index.xml', 'wp-sitemap.xml']
    urls = set()

    for variant in sitemap_variants:
        try:
            sitemap_url = f"http://{base_url}/{variant}"
            response = requests.get(sitemap_url)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                namespaces = {
                    'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                for url in root.findall('.//ns:url/ns:loc', namespaces):
                    urls.add(url.text)

                if urls:
                    process_urls(list(urls), base_url)
                    return list(urls)
        except Exception as e:
            print(f"Error processing {sitemap_url}: {e}")

    if not urls:
        homepage = f"http://{base_url}"
        print(f'Did not find sitemap for {base_url}, adding homepage.')
        urls.add(homepage)
        process_urls(list(urls), base_url)

    return list(urls)


def process_domains_in_parallel(domains, max_workers=12):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(
            find_sitemap_and_extract_urls, domain): domain for domain in domains}

        for future in concurrent.futures.as_completed(future_to_url):
            domain = future_to_url[future]
            try:
                urls = future.result()
                print(f"Processed {domain}, Extracted URLs: {urls}")
            except Exception as exc:
                print(f"{domain} generated an exception: {exc}")
