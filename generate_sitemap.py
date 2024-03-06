import requests
import xml.etree.ElementTree as ET


def find_sitemap_and_extract_urls(base_url):

    sitemap_variants = ['sitemap.xml', 'index.xml',
                        'sitemap_index.xml', 'wp-sitemap.xml']
    urls = []

    for variant in sitemap_variants:
        try:
            sitemap_url = f"http://{base_url}/{variant}"
            response = requests.get(sitemap_url)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                namespaces = {
                    'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                found = False
                for url in root.findall('.//ns:url/ns:loc', namespaces):
                    urls.append(url.text)
                    found = True
                if found:
                    return urls
        except Exception as e:
            print(f"Error processing {sitemap_url}: {e}")

    return [base_url] if not urls else urls


base_url = ""
urls = find_sitemap_and_extract_urls(base_url)
print(urls)
