from sqlalchemy import create_engine, text
from packages.players import create_players_table
import pandas as pd
import packages.board_games as bg
import logging
from pandas import DataFrame

def get_games_data(sql_string: str, db: str, schema: str, columns: str) -> DataFrame:
    """Get data from games table.

    Args:
        sql_string (str): string to connect onto postgres
        db (str): database name
        schema (str): schema name
        columns (str): columns to retrieve

    Returns:
        DataFrame: table
    """
    engine = create_engine(sql_string)
    engine.execution_options(autocommit=True)
    columns = ', '.join(f'"{column}"' for column in columns)
    qry = f'SELECT DISTINCT {columns} FROM {db}.{schema}."GAMES"'
    with engine.connect() as conn:
        try:
            return pd.read_sql(qry, conn)
        except:
            try:
                bgs
            except:
                players = get_players_data(sql_string, db, schema, ['ID', 'LUDOPEDIA_NICKNAME'])
                bgs = bg.get_all_bgs(players)            
                save_table(bg.create_board_games_table(bgs), schema, sql_string, 'GAMES')
                return pd.read_sql(qry, conn)
    
def get_players_data(sql_string: str, db: str, schema: str, columns: str) -> DataFrame:
    """Get data from players' table.

    Args:
        sql_string (str): string to connect onto postgres
        db (str): database name
        schema (str): schema name
        columns (str): columns to retrieve

    Returns:
        DataFrame: table
    """    
    engine = create_engine(sql_string)
    engine.execution_options(autocommit=True)
    columns = ', '.join(f'"{column}"' for column in columns)
    qry = f'SELECT {columns} FROM {db}.{schema}."PLAYERS"'
    with engine.connect() as conn:
        try:     
            return pd.read_sql(qry, conn)
        except:
            save_table(create_players_table, schema, sql_string, 'PLAYERS')
            return pd.read_sql(qry, conn)
        
def save_table(df: DataFrame, schema: str, sql_string: str, table_name: str, mode='append') -> None:
    """Saves a Dataframe into the database

    Args:
        df (DataFrame): table to be saved
        schema (str): name of the schema on database
        sql_string (str): string connection to database
        table_name (str): name of the table to save the df
        mode (str, optional): if the table will be replaced or appended. Defaults to 'append'.
    """
    truncate_table(sql_string, schema, table_name)
    engine = create_engine(sql_string)
    with engine.connect() as conn:
        df.to_sql(name=table_name, con=conn, if_exists=mode, schema=schema, index=False)
        logging.info(f'Table {table_name} was successfully created with {len(df)} rows.')
        
def truncate_table(sql_string: str, schema: str, table_name: str) -> None:
    """truncate a table to be appended.

    Args:
        sql_string (str): string to connect onto postgres
        schema (str): schema name
        table_name (str): table name
    """
    try:
        engine = create_engine(sql_string)
        with engine.connect() as conn:
            conn.execute(text(f'TRUNCATE TABLE {schema}."{table_name}"'))
            conn.commit()
    except:
        logging.warning(f"Table {table_name} wasn't truncated because it doesn't exist.")