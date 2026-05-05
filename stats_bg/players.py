import pandas as pd
from scrapper.ludopedia_scrapper import LudopediaScrapper
from pandas import Series, DataFrame
from stats_bg.sheets import get_url
from stats_bg.utils import timeit


def _create_player_id_column(nicknames: Series) -> Series:
    """Create ID column for Pandas Dataframe based on the column LUDOPEDIA_NICKNAME.
    If a player has a nickname on Ludopedia, this function retrieves the correspondent ID.

    Args:
        nicknames (Series): Pandas Series with players Data

    Returns:
        Series: Pandas Series with unique ID for every player
    """
    ls = LudopediaScrapper()
    ids = nicknames.map(ls.get_user_id,na_action="ignore")
    return ids.astype("Int64")


@timeit
def create_players_table() -> DataFrame:
    """Create players table.

    Returns:
        DataFrame: dataframe with date, player id, and is host columns.
    """
    url = get_url("players")
    players = pd.read_csv(url)
    players["ID"] = _create_player_id_column(players["LUDOPEDIA_NICKNAME"])
    return players
