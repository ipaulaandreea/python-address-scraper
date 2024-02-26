import requests
from bs4 import BeautifulSoup
from get_pages_with_contact_page import websites_with_contact_pages

import requests


url = ''


response = requests.get(url)
print(f"First attempt response code: {response.status_code}")


if response.status_code == 410:
    print("Received a 410 status code, trying again with custom headers...")

    headers = {'User-Agent': 'whatever'}

    response = requests.get(url, headers=headers)
    print(f"Second attempt response code: {response.status_code}")

    if response.status_code == 200:
        print("Successfully fetched the page with custom headers.")
        html_content = response.text

    else:
        print(f"Failed to fetch the page, status code: {response.status_code}")
else:
    print("Successfully fetched the page on the first attempt.")
    html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

text_element = soup.find(['!DOCTYPE', 'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdi', 'bdo',
                          'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup', 'data',
                          'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset',
                          'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header',
                          'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main',
                          'map', 'mark', 'meta', 'meter', 'nav', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output',
                          'p', 'param', 'picture', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section',
                          'select', 'small', 'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup', 'svg', 'table',
                          'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'u',
                          'ul', 'var', 'video', 'wbr'])


if text_element:
    text = text_element.text.strip()

    search_words = ["contact", "Contact", "address", "Address"]

for search_word in search_words:
    if search_word in text:
        print(f"'{search_word}' found in the text element.")
    else:
        print(f"'{search_word}' not found in the text.")
else:
    print("Text element not found on the page.")
