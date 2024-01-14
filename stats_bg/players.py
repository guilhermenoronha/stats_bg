import pandas as pd
from scrapper.ludopedia_scrapper import LudopediaScrapper
from pandas import Series, DataFrame
from stats_bg.sheets import get_url
from stats_bg.utils import timeit

def _create_player_id_column(nicknames : Series) -> Series:
    """Create ID column for Pandas Dataframe based on the column LUDOPEDIA_NICKNAME. 
    If a player has a nickname on Ludopedia, this function retrieves the correspondent ID,
    otherwise the player receives an autoincremental value. 

    Args:
        nicknames (Series): Pandas Series with players Data

    Returns:
        Series: Pandas Series with unique ID for every player
    """
    ls = LudopediaScrapper()
    ids = nicknames.map(ls.get_user_id, 'ignore')
    ids.loc[ids.isnull()] = [*range(1, ids.isnull().sum() + 1)]
    return ids.astype(int)

def _create_players_lst_dt_att_column(names : Series) -> Series:
    """Create a column for players table with the last time he/she attended to a session

    Args:
        names (Series): column with the players name

    Returns:
        Series: lst_dt_att column
    """
    matches_url = get_url('matches')
    matches = pd.read_csv(matches_url)
    matches.drop(columns=['game', 'host'], inplace=True)
    lst_dt = {matches.columns[i]: matches.loc[matches.iloc[:, i].notnull(), 'date'].iloc[-1] for i in range(1, len(matches.columns))}
    return names.map(lst_dt)

@timeit
def create_players_table() -> DataFrame:
    """Create players table. 

    Returns:
        DataFrame: dataframe with date, player id, and is host columns.
    """
    url = get_url('players')
    players  = pd.read_csv(url)
    players['ID'] = _create_player_id_column(players['LUDOPEDIA_NICKNAME'])
    players['LAST_DATE_ATTENDED'] = _create_players_lst_dt_att_column(players['NAME'])
    return players
