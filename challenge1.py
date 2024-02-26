import pyarrow.parquet as pq

file_path = 'domains.snappy.parquet'
table = pq.read_table(file_path)
df = table.to_pandas()
