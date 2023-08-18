from sqlite3 import Connection
from packages.sheets import get_url
from packages.utils import timeit
from pandas import DataFrame
import pandas as pd
import logging

def _get_player_matches(df : DataFrame, player : tuple, games : list[tuple]) -> DataFrame:
    """Get all matches played by player

    Args:
        df (DataFrame): matches
        player (tuple): tuple with player name and id
        games (list[tuple]): tuples with games names and ids

    Returns:
        DataFrame: Dataframw with date, player id, game id, and scoore by the player
    """
    df = df.loc[df[player[0]].notnull()]
    id = df['id']
    date = df['date']
    score = df[player[0]]
    game_id = df['game'].map(dict(games))
    return pd.DataFrame({
        'ID'        : id,
        'DATE'      : date,
        'PLAYER_ID' : player[1],
        'GAME_ID'   : game_id,
        'SCORE'     : score
    })

@timeit
def create_matches_table(conn : Connection) -> None:
    """Create matches table

    Args:
        conn (Connection): Database connection where the table will be created
    """
    table_name = 'MATCHES'
    cur = conn.execute('SELECT NAME, ID FROM PLAYERS')
    players = cur.fetchall()
    cur = conn.execute('SELECT NAME, ID FROM GAMES')
    games = cur.fetchall()
    matches = pd.read_csv(get_url('matches'))
    matches['id'] = range(1, len(matches) + 1)
    final_matches = pd.DataFrame(columns=['DATE', 'PLAYER_ID', 'GAME_ID', 'SCORE'])
    for player in players:
        final_matches = pd.concat([final_matches, _get_player_matches(matches, player, games)])
    final_matches.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
    logging.info(f'Table {table_name} was successfully created with {len(final_matches)} rows.')