from get_contact_pages import check_contact_page
import os
import pymysql
from dotenv import load_dotenv
import pyarrow.parquet as pq
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
# Extracts from the original file the domains, check for contact pages and stores them in mysql

def save_domains_contact_paths_to_mysql():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.getenv('FILE_PATH')
    file_path = os.path.join(script_dir, file_name)
    table = pq.read_table(file_path)
    df = table.to_pandas()

    websites_and_contact_pages = check_contact_page(df)


    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO main_db (domain, contact_url) VALUES (%s, %s)"

            cursor.executemany(sql, websites_and_contact_pages)
            connection.commit()
            return websites_and_contact_pages

    finally:
        connection.close()
