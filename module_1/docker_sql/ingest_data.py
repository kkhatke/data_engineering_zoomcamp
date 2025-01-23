import os
import argparse
from time import time 
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    
    # Parquet File
    
    parquet_file = "data.parquet"
    
    os.system(f'curl -o {parquet_file} {params.url}')
    
    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
    engine.connect()

    df = pq.ParquetFile(parquet_file)
    # Iterate over row groups or specific row ranges
    for rg in range(df.num_row_groups):
        t_start = time()
        df_chunk = df.read_row_group(rg).to_pandas()
        df_chunk['lpep_pickup_datetime'] = pd.to_datetime(df_chunk['lpep_pickup_datetime'])
        df_chunk['lpep_dropoff_datetime'] = pd.to_datetime(df_chunk['lpep_dropoff_datetime'])
        df_chunk.to_sql(name='green_taxi_data', con=engine, if_exists='append')
        t_end = time()
        
        print("Inserted another chunk, took %.3f seconds..." % (t_end-t_start))
        
    # # CSV File

    # df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # df = next(df_iter)

    # df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    # df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    # df.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')

    # df.to_sql(name=table_name, con=engine, if_exists='append')

    # while True:
    #     t_start = time()
    #     df = next(df_iter)
    #     df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    #     df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        
    #     df.to_sql(name=table_name, con=engine, if_exists='append')
    #     t_end = time()
        
    #     print("Inserted another chunk, took %.3f seconds..." % (t_end-t_start))
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Parquet data to Postgres')

    # user, password, host, port, database name, table name
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', default='localhost', help='host for postgres')
    parser.add_argument('--port', default=5432, help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='table name for postgres')

    # url
    parser.add_argument('--url', help='url of the parquet file')

    args = parser.parse_args()
    main(args)

