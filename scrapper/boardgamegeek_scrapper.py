import requests
import logging
import re
import time

def _get_content(url : str) -> str:
    """Get decoded content from an url

    Args:
        url (str): url

    Raises:
        ValueError: raises error if url page isn't found.

    Returns:
        str: return content from the url decoded in utf-8
    """
    response = requests.get(url)
    requests_num = 0
    while response.status_code == 429: # avoiding requests limits
        time.sleep(5)
        response = requests.get(url)
        requests_num += 1
        if requests_num == 10: # throws an error if the limits persists.
            raise ValueError(f'Request limits exceeded!')
    if response.status_code != 200:
        raise ValueError(f'Page not found! Status code: {response.status_code}')
    else:
        return response.content.decode('utf-8')

def get_BGG_url_by_Ludopedia_search(search : str) -> str:
    """Try to find the game url based on a search string

    Args:
        search (str): string to search the game

    Raises:
        ValueError: raises error if the page isn't found

    Returns:
        str: game url
    """
    url = f'https://boardgamegeek.com/geeksearch.php?action=search&objecttype=boardgame&q={search}'
    content = _get_content(url)
    res = re.findall(r'/boardgame.*/\d+/', content)
    if len(res) == 0:
        logging.warning(f'Warning! Search {search} returned nothing!')
        return None
    else:
        id = re.search(r'\d+', res[0]).group()
        return f'https://boardgamegeek.com/boardgame/{id}/{search}'
    
def get_BGG_game_weight(url : str) -> float:
    """Get the complexity rate (weight) of a game

    Args:
        url (str): game url on BGG

    Returns:
        float: game complexity rounded on 2 decimals
    """
    content = _get_content(url)
    match = re.search(r'boardgameweight":{"averageweight":(\d+(\.\d+)?)', content)
    return round(float(match[1][0:5]), 2)
    
def get_BGG_min_max_best_players(url : str) -> tuple[str]:
    """Get the min and the max recommend players for a game

    Args:
        url (str): game url on BGG

    Returns:
        tuple[str]: the recommended min and max number of players
    """
    if url is None:
        return (None, None)
    content = _get_content(url)
    min_pattern = r'{\"userplayers\":{\"best\":\[{\"min\":(\d+)'
    min = re.search(min_pattern, content)
    max = re.search(min_pattern + r',\"max\":(\d+)', content)
    return min[min.lastindex], max[max.lastindex]
