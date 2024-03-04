from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from requests.exceptions import ProxyError, ConnectTimeout, HTTPError, RequestException
import requests
import tldextract
import os
import pymysql
from dotenv import load_dotenv
load_dotenv()

host_name = os.getenv('DB_HOST')
user_name = os.getenv('DB_USER')
user_password = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')


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
    extracted = tldextract.extract(website)
    tld = f".{extracted.suffix}" if extracted.suffix else ''
    for pattern in patterns: 
        contact_url = f"http://{website}{pattern}"
        response = lookup(contact_url)
        if response and response.status_code == 200: 
            return (website, contact_url, tld)
        else:
            continue
    return (website, None, tld)

def insert_batch_to_db(batch):
    connection = pymysql.connect(host=host_name,
                                 user=user_name,
                                 password=user_password,
                                 database=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO main_db (domain, contact_url, suffix) VALUES (%s, %s, %s)"
            cursor.executemany(sql, batch)
            connection.commit()
    finally:
        connection.close()

def check_contact_page(websites, batch_size=15):
    def batch_process(websites_batch):
        results = []
        with ThreadPoolExecutor(max_workers=12) as executor:
            future_to_website = {executor.submit(check_single_website, website): website for website in websites_batch}
            for future in as_completed(future_to_website):
                result = future.result()
                results.append(result)
        insert_batch_to_db(results)
        return results
    
    start = time.time()
    all_results = []

    for i in range(0, len(websites), batch_size):
        websites_batch = websites[i:i+batch_size]
        batch_results = batch_process(websites_batch)
        all_results.extend(batch_results)
    
    end = time.time()
    print(f"Execution time: {(end - start) * 1000} ms")
    return all_results

def get_first_20_domains_from_db():
    connection = pymysql.connect(host=host_name,
                                 user=user_name,
                                 password=user_password,
                                 database=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT domain, contact_url FROM main_db LIMIT 20"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    finally:
        connection.close()