import json
import os
import pymysql
from dotenv import load_dotenv
load_dotenv()


def get_db_connection():
    host_name = os.getenv('DB_HOST')
    user_name = os.getenv('DB_USER')
    user_password = os.getenv('DB_PASS')
    db_name = os.getenv('DB_NAME')
    return pymysql.connect(host=host_name, user=user_name, password=user_password, database=db_name, cursorclass=pymysql.cursors.DictCursor)


def insert_page_content_to_db(link, base_url, html_content, found_addresses, serialized_data):
    connection = get_db_connection()
    delimited_addresses = '; '.join(found_addresses) if found_addresses else ''
    try:
        with connection.cursor() as cursor:
            sql = """
             INSERT INTO pages_and_addresses (page, domain_name, html_str, address_str, organized_address)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                html_str = VALUES(html_str),
                address_str = VALUES(address_str),
                organized_address = VALUES(organized_address)
            """
            serialized_data = serialized_data if serialized_data is not None else json.dumps([
            ])
            cursor.execute(sql, (link, base_url, html_content,
                           delimited_addresses, serialized_data))
            connection.commit()
    finally:
        connection.close()
