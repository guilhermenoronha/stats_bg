from pandas import DataFrame
from stats_bg.sheets import get_url
from stats_bg.utils import timeit
import pandas as pd


def _get_player_attendances(df: DataFrame, player: DataFrame) -> DataFrame:
    """Get attendances for a specific player

    Args:
        df (DataFrame): matches df
        player (DataFrame): id, name of a player

    Returns:
        DataFrame: dataframe with date, player id, and is host columns.
    """
    df = df.loc[df[player["NAME"]].notnull()]
    date = df["date"]
    is_host = df["host"] == player["NAME"]
    result = pd.DataFrame({"DATE": date, "PLAYER_ID": player["ID"], "IS_HOST": is_host})
    result = result.drop_duplicates(subset=["DATE", "PLAYER_ID"], keep="first")
    return result


@timeit
def create_attendances_table(players: DataFrame) -> DataFrame:
    """Create attendances table based on matches sheet

    Args:
        players (DataFrame): df with name and id

    Returns:
        DataFrame: dataframe with date, player id, and is host columns.
    """
    matches = pd.read_csv(get_url("matches"))
    attendances = pd.DataFrame(columns=["DATE", "PLAYER_ID", "IS_HOST"])
    for _, player in players.iterrows():
        attendances = pd.concat([attendances, _get_player_attendances(matches, player)])
    return attendances
