import requests
from bs4 import BeautifulSoup
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def check_for_address_word(urls, conn):
    links = []
    for url in urls:
        link = url['address']
        try:
            response = requests.get(link, headers={'User-Agent': 'Custom User Agent'})
            if response.status_code in [200, 410]:  
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                text_element = soup.find(text=lambda t: "contact" in t.lower() or "address" in t.lower())
                if text_element:
                    # print(f"'Contact' or 'Address' found in '{link}'")
                    links.append((url)) 
        except requests.RequestException as e:
            print(f"Failed to fetch '{link}': {e}")

    save_entries(links, conn)

def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def fetch_domains(conn):
    cursor = conn.cursor()
    query = "SELECT domain, contact_page FROM domains_with_address"
    cursor.execute(query)
    domains = cursor.fetchall()
    cursor.close()
    return domains

def process_domains(domains, conn):
    urls_list = [{'domain': domain, 'address': address} for domain, address in domains]
    check_for_address_word(urls_list, conn)

def save_entries(links, conn):
    cursor = conn.cursor()
    insert_stmt = "INSERT INTO domains_with_address_word_on_page (domain) VALUES (%s)"
    cursor.executemany(insert_stmt, links)
    conn.commit()
    cursor.close()

def main():
    conn = connect_to_db()
    if conn:
        try:
            domains = fetch_domains(conn)
            process_domains(domains, conn)
        finally:
            conn.close()

if __name__ == "__main__":
    main()
