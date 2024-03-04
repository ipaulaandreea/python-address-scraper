import os
import pymysql
from dotenv import load_dotenv
load_dotenv()

host_name = os.getenv('DB_HOST')
user_name = os.getenv('DB_USER')
user_password = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')


def add_organized_addresses_to_db(batch):
    connection = pymysql.connect(host=host_name,
                                 user=user_name,
                                 password=user_password,
                                 database=db_name,
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT IGNORE INTO domain_address_info (domain, country, city, region, postcode, road, road_number) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(sql, batch)
            connection.commit()
    finally:
        connection.close()

