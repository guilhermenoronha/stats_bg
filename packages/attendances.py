from pandas import DataFrame
from sqlite3 import Connection
from packages.sheets import get_url
import logging
import pandas as pd

def _get_player_attendances(df : DataFrame, player : tuple) -> DataFrame:
    df = df.loc[df[player[0]].notnull()]
    date = df['date']
    is_host = df['host'] == player[0]
    result = pd.DataFrame({
        'DATE' : date,
        'PLAYER_ID' : player[1],
        'IS_HOST': is_host
    })
    return result.drop_duplicates(subset=['DATE', 'PLAYER_ID'], keep='first')

def create_attendances_table(conn : Connection) -> None:
    table_name = 'ATTENDANCES'
    cur = conn.execute('SELECT NAME, ID FROM PLAYERS')
    players = cur.fetchall()
    matches = pd.read_csv(get_url('matches'))
    attendances = pd.DataFrame(columns=['DATE', 'PLAYER_ID', 'IS_HOST'])
    for player in players:
        attendances = pd.concat([attendances, _get_player_attendances(matches, player)])
    attendances.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
    logging.info(f'Table {table_name} was successfully created with {len(attendances)} rows.')