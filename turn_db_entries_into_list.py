import mysql.connector
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

conn = mysql.connector.connect(
    host=host_name,
    user=user_name,
    password=user_password,
    database=db_name
)

cur = conn.cursor()

query = 'SELECT domain FROM domains ORDER BY id LIMIT 10;'


cur.execute(query)


domains = cur.fetchall()


domain_list = [item[0] for item in domains]


cur.close()
conn.close()