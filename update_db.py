import os
import pymysql
from dotenv import load_dotenv
load_dotenv()
import json

def get_db_connection():
    host_name = os.getenv('DB_HOST')
    user_name = os.getenv('DB_USER')
    user_password = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')
    return pymysql.connect(host=host_name, user=user_name, password=user_password, database=db_name, cursorclass=pymysql.cursors.DictCursor)

def prepare_data_and_send(domain_pages):
    batch = []
    for domain, pages in domain_pages.items():
        for page in pages:
            batch.append((page, domain))
        
    if batch: 
        send_pages_to_db(batch)

def send_pages_to_db(batch):
    connection = get_db_connection() 
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO pages_and_addresses (page, domain_name) VALUES (%s, %s)"
            cursor.executemany(sql, batch)
            connection.commit()
    finally:
        connection.close()

def get_pages_from_db():
    connection = get_db_connection() 
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT `page` FROM `pages_and_addresses`"
            cursor.execute(sql)
            results = cursor.fetchall()
            data_list = [str(row['page']) for row in results]
            return data_list
    finally:
        connection.close()

def add_organized_addresses_to_db(batch):
    connection = get_db_connection() 
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO domain_address_info (domain, country, city, region, postcode, road, road_number) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, batch)
            connection.commit()
    finally:
        connection.close()

def update_domains_in_mysql(batch):
    connection = get_db_connection() 
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO main_db (domain, address_str, strategy, finished)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            strategy = VALUES(strategy),
            finished = VALUES(finished)
            address_str = VALUES(address_str)
            """
            cursor.executemany(sql, batch)
            connection.commit()
    finally:
        connection.close()

def insert_page_content_to_db(link, html_content, found_addresses, serialized_data):
    connection = get_db_connection()
    delimited_addresses = '; '.join(found_addresses) if found_addresses else ''
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT IGNORE INTO pages_and_addresses (page, html_str, address_str, organized_address)
            VALUES (%s, %s, %s, %s)
            """
            serialized_data = serialized_data if serialized_data is not None else json.dumps([])
            cursor.execute(sql, (link, html_content, delimited_addresses, serialized_data))
            connection.commit()
    finally:
        connection.close()