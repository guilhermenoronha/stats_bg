from sqlalchemy import create_engine
from packages.utils import save_table
from packages.players import create_players_table
import pandas as pd
import packages.board_games as bg

def get_games_data(sql_string, db, schema, columns):
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
    
def get_players_data(sql_string, db, schema, columns):
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