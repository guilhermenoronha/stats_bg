from pandas import DataFrame
from packages.sheets import get_url
from packages.utils import timeit
import pandas as pd

def _get_player_attendances(df : DataFrame, player : tuple) -> DataFrame:
    """Get attendances for a specific player

    Args:
        df (DataFrame): matches df
        player (tuple): id, name of a player

    Returns:
        DataFrame: dataframe with date, player id, and is host columns.
    """
    df = df.loc[df[player[0]].notnull()]
    date = df['date']
    is_host = df['host'] == player[0]
    result = pd.DataFrame({
        'DATE' : date,
        'PLAYER_ID' : player[1],
        'IS_HOST': is_host
    })
    return result.drop_duplicates(subset=['DATE', 'PLAYER_ID'], keep='first')

@timeit
def create_attendances_table(players : list[tuple[str]]) -> DataFrame:
    """Create attendances table based on matches sheet

    Args:
        players (tuple[str]): name and id

    Returns:
        DataFrame: dataframe with date, player id, and is host columns.
    """
    matches = pd.read_csv(get_url('matches'))
    attendances = pd.DataFrame(columns=['DATE', 'PLAYER_ID', 'IS_HOST'])
    for player in players:
        attendances = pd.concat([attendances, _get_player_attendances(matches, player)])
    return attendances