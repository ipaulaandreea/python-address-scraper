import os
from dotenv import load_dotenv
import pyarrow.parquet as pq
load_dotenv()


script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = os.getenv('FILE_PATH')
file_path = os.path.join(script_dir, file_name)
table = pq.read_table(file_path)
df = table.to_pandas()
