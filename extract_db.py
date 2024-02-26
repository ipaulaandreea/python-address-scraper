import pyarrow.parquet as pq
from dotenv import load_dotenv
import os
load_dotenv()

file_path = os.getenv('FILE_PATH')
table = pq.read_table(file_path)
df = table.to_pandas()
