import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

host_name = os.getenv('DB_HOST')
user_name = os.getenv('DB_USER')
user_password = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')

connection = pymysql.connect(host=host_name,
                                user=user_name,
                                 password=user_password,
                                 database=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)


def update_domains_in_mysql(domains):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO main_db (domain, contact_url, finished, address_str, strategy) VALUES (%s, %s)"

            cursor.executemany(sql, domains)
            connection.commit()

    finally:
        connection.close()
