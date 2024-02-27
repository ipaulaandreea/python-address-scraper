import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def check_for_address_word(urls):
    link = ''
    for url in urls: 
        link = url['address']
       
        response = requests.get(link)
        # print(f"First attempt response code: {response.status_code}")


        if response.status_code == 410:
            # print("Received a 410 status code, trying again with custom headers...")

            headers = {'User-Agent': 'whatever'}

            response = requests.get(link, headers=headers)
            # print(f"Second attempt response code: {response.status_code}")

            if response.status_code == 200:
                # print("Successfully fetched the page with custom headers.")
                html_content = response.text

            else:
                print(f"Failed to fetch the page, status code: {response.status_code}")
        else:
            # print("Successfully fetched the page on the first attempt.")
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
                print(f"'{search_word}' found in '{link}'")
                break
            # else:
            #     print(f"'{search_word}' not found in the text.")
        # else:
        #     print(f"Text element not found on '{link}'.")


def connect_to_db(host, user, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return conn

def fetch_domains(conn):
    cursor = conn.cursor()
    query = "SELECT domain, contact_page FROM domains_with_address"
    cursor.execute(query)
    return cursor.fetchall()

def process_domains(domains):
    urls_list = []
    for domain, address in domains:
        urls_list.append({'domain': domain, 'address': address})
    print (urls_list)
    print(check_for_address_word(urls_list))

def main():
    host =  os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    database = os.getenv('DB_NAME')

    conn = connect_to_db(host, user, password, database)
    try:
        domains = fetch_domains(conn)
        process_domains(domains)
    finally:
        conn.close()

if __name__ == "__main__":
    main()


