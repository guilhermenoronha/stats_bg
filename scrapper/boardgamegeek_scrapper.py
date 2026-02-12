import requests
from requests.exceptions import ChunkedEncodingError
import logging
import re
import time
import pandas as pd
from stats_bg.sheets import get_url


def _get_content(url: str) -> str:
    """Get decoded content from an url

    Args:
        url (str): url

    Raises:
        ValueError: raises error if url page isn't found.

    Returns:
        str: return content from the url decoded in utf-8
    """
    for _ in range(5):
        try:
            response = requests.get(url)
            break
        except ChunkedEncodingError:
            time.sleep(5)
    requests_num = 0
    while response.status_code == 429:  # avoiding requests limits
        time.sleep(5)
        response = requests.get(url)
        requests_num += 1
        if requests_num == 10:  # throws an error if the limits persists.
            raise ValueError(f"Request limits exceeded!")
    if response.status_code != 200:
        raise ValueError(f"Page not found! Status code: {response.status_code}")
    else:
        return response.content.decode("utf-8")


def _get_game_url_from_sheet_aid(search: str) -> str:
    """This function use a sheet as an aid to get BGG urls where the search found nothing.

    Args:
        search (str): string to search the game

    Returns:
        str: game url
    """
    try:
        url = get_url("ludopedia-bgg")
        df = pd.read_csv(url)
        idx = df.loc[df["search"] == search].index[0]
        return df.at[idx, "bgg_url"]
    except Exception:
        return None


def get_BGG_url_by_Ludopedia_search(search: str) -> str:
    """Try to find the game url based on a search string

    Args:
        search (str): string to search the game

    Raises:
        ValueError: raises error if the page isn't found

    Returns:
        str: game url
    """
    url = f"https://boardgamegeek.com/geeksearch.php?action=search&objecttype=boardgame&q={search}"
    content = _get_content(url)
    res = re.findall(r"/boardgame.*/\d+/", content)
    if len(res) == 0:
        url = _get_game_url_from_sheet_aid(search)
        if url is None:
            logging.warning(f"Warning! Search {search} returned nothing!")
            return None
        else:
            return url
    else:
        id = re.search(r"\d+", res[0]).group()
        return f"https://boardgamegeek.com/boardgame/{id}/{search}"


def get_BGG_game_weight(url: str) -> float:
    """Get the complexity rate (weight) of a game

    Args:
        url (str): game url on BGG

    Returns:
        float: game complexity rounded on 2 decimals
    """
    content = _get_content(url)
    match = re.search(r'boardgameweight":{"averageweight":(\d+(\.\d+)?)', content)
    return round(float(match[1][0:5]), 2)


def get_BGG_min_max_best_players(url: str) -> tuple[str]:
    """Get the min and the max recommend players for a game

    Args:
        url (str): game url on BGG

    Returns:
        tuple[str]: the recommended min and max number of players
    """
    if url is None:
        return (None, None)
    content = _get_content(url)
    min_pattern = r"{\"userplayers\":{\"best\":\[{\"min\":(\d+)"
    min = re.search(min_pattern, content)
    max = re.search(min_pattern + r",\"max\":(\d+)", content)
    min = min[min.lastindex] if min is not None else None
    max = max[max.lastindex] if max is not None else None
    return min, max
