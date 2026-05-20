from stats_bg.sheets import get_url
from stats_bg.utils import timeit
from pandas import DataFrame
import pandas as pd


@timeit
def create_matches_table() -> DataFrame:
    """Create matches table

    Args:
        players (DataFrame): df with players' name and id
        games (DataFrame): df  with games' name and id

    Returns:
        DataFrame: with date, player id, game id and score
    """
    matches = pd.read_csv(get_url("matches"))
    cols = ["date",	"host_name", "match_id", "game_name", "game_owner"]
    matches[cols] = matches[cols].ffill()
    return matches
