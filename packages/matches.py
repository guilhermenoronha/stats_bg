from packages.sheets import get_url
from packages.utils import timeit
from pandas import DataFrame
import pandas as pd

def _get_player_matches(df: DataFrame, player: DataFrame, games: DataFrame) -> DataFrame:
    """Get all matches played by player

    Args:
        df (DataFrame): matches
        player (DataFrame): df with player name and id
        games (DataFrame): df with names and ids

    Returns:
        DataFrame: Dataframw with date, player id, game id, and scoore by the player
    """
    df = df.loc[df[player['NAME']].notnull()]
    id = df['id']
    date = df['date']
    score = df[player['NAME']]
    game_id = df['game'].map(dict(games.values))
    return pd.DataFrame({
        'ID'        : id,
        'DATE'      : date,
        'PLAYER_ID' : player['ID'],
        'GAME_ID'   : game_id,
        'SCORE'     : score
    })

@timeit
def create_matches_table(players: DataFrame, games: DataFrame) -> DataFrame:
    """Create matches table

    Args:
        players (DataFrame): df with players' name and id
        games (DataFrame): df  with games' name and id

    Returns:
        DataFrame: with date, player id, game id and score
    """
    matches = pd.read_csv(get_url('matches'))
    matches['id'] = range(1, len(matches) + 1)
    final_matches = pd.DataFrame(columns=['DATE', 'PLAYER_ID', 'GAME_ID', 'SCORE'])
    for _, player in players.iterrows():
        final_matches = pd.concat([final_matches, _get_player_matches(matches, player, games)])
    return final_matches