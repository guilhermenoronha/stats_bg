import logging
import re
import pandas as pd
from stats_bg.sheets import get_url
from xml.etree import ElementTree
import urllib.request
from urllib.parse import urlparse, parse_qs
import os

def _get_content(url: str) -> ElementTree:
    """Get decoded content from an url

    Args:
        url (str): url

    Raises:
        ValueError: raises error if url page isn't found.

    Returns:
        ElementTree: return XML content parsed
    """    
    BGG_TOKEN = os.getenv("BOARDGAME_GEEK_TOKEN")
    try:
        request = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {BGG_TOKEN}"
            }
        )

        with urllib.request.urlopen(request) as response:
            result = ElementTree.fromstring(response.read())
        return result
    except ValueError:
        return None


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

def get_BGG_public_url(api_url: str) -> str:
    """Get BGG public URL from API URL

    Args:
        api_url (str): api url to be converted to public url  

    """
    if api_url is None:
        return None

    game_id = parse_qs(urlparse(api_url).query).get("id", [None])[0]

    return f"https://boardgamegeek.com/boardgame/{game_id}" if game_id else None

def get_BGG_url_by_Ludopedia_search(search:str) -> str:
    """Try to find the game url based on a search string

    Args:
        search (str): string to search the game

    Raises:
        ValueError: raises error if the page isn't found

    Returns:
        str: game url
    """    
    params = urllib.parse.urlencode({
        "query": search,
        "type": "boardgame"
    })

    url = f"https://boardgamegeek.com/xmlapi2/search?{params}"
    root = _get_content(url)
    if not root:
        url = _get_game_url_from_sheet_aid(search)
        if url is None:
            logging.warning(f"Warning! Search {search} returned nothing!")
            return None
    items = root.findall("item")
    game_id = items[0].attrib["id"]
    return f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}&stats=1"    


def get_BGG_game_weight(url: str) -> float:
    """Get the complexity rate (weight) of a game

    Args:
        url (str): game url on BGG

    Returns:
        float: game complexity rounded on 2 decimals
    """    
    root = _get_content(url)
    if not root:
        return None
    items = root.findall("item")
    weight = items[0].find(".//averageweight").attrib["value"]
    return round(float(weight), 2)


def get_BGG_min_max_best_players(url: str) -> tuple[str]:
    """Get the min and the max recommend players for a game

    Args:
        url (str): game url on BGG

    Returns:
        tuple[str]: the recommended min and max number of players
    """    
    root = _get_content(url)
    if not root:
        return None, None
    items = root.findall("item")
    content = items[0].find(".//poll-summary[@name='suggested_numplayers']/result[@name='bestwith']").attrib["value"]
    min_max = re.findall(r'\d+', content)
    min = min_max[0]
    max = min_max[-1] 

    return min, max
