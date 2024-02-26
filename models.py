import pymysql.cursors
import pymysql
import json
from get_country import domains_and_suffixes_list
from dotenv import load_dotenv
import os

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

try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO domains (domain, suffix) VALUES (%s, %s)"
        
        cursor.executemany(sql, domains_and_suffixes_list)
        connection.commit()
        
finally:
    connection.close()


