from get_contact_pages import check_contact_page
import os
import pymysql
from dotenv import load_dotenv
import pyarrow.parquet as pq
load_dotenv()
import pandas

def save_domains_contact_paths_to_mysql():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.getenv('FILE_PATH')
    file_path = os.path.join(script_dir, file_name)
    table = pq.read_table(file_path)
    df = table.to_pandas()
    domains_list = df['domain'].tolist()
 
    websites_and_contact_pages = check_contact_page(domains_list)
    return websites_and_contact_pages
