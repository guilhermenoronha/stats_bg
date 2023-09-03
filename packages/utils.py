from functools import wraps
from pandas import DataFrame
from sqlite3 import Connection
import time
import logging
from sqlalchemy import create_engine

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logging.info(f'Function {func.__name__} took {total_time:.2f} seconds')
        return result
    return timeit_wrapper

def save_table(df, schema, sql_string, table_name, mode='replace'):
    engine = create_engine(sql_string)
    engine.execution_options(autocommit=True)
    with engine.connect() as conn:
        df.to_sql(name=table_name, con=conn, if_exists=mode, schema=schema, index=False)
        logging.info(f'Table {table_name} was successfully created with {len(df)} rows.')

