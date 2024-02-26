import mysql.connector
import pymysql.cursors
import pymysql
import json
from dotenv import load_dotenv
import os
from get_pages_with_contact_page import websites_with_contact_pages

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

cursor = conn.cursor()

insert_stmt = "INSERT INTO domains_with_address (domain, contact_page) VALUES (%s, %s)"

for website, contact_url in websites_with_contact_pages:
    data = (website, contact_url)
    cursor.execute(insert_stmt, data)

conn.commit()

cursor.close()
conn.close()