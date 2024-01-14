from scrapper.ludopedia_scrapper import LudopediaScrapper
import scrapper.boardgamegeek_scrapper as bgg
from pandas import DataFrame
from stats_bg.sheets import get_url
from stats_bg.utils import timeit
import itertools
import pandas as pd
import os

def _get_players_bgs_ids_from_sheet() -> list:
    """Get all bgs from players in bg_stats sheet

    Returns:
        list: a list of dicts containing the owner id and game id 
    """
    ls = LudopediaScrapper()
    url = get_url('games')
    df = pd.read_csv(url)
    games = df['NAME'].map(ls.get_game_by_name).to_list()
    bg_ids = [game['id_jogo'] for game in games]
    user_ids = df['ID_OWNER'].to_list()
    return [{'id_dono' : user_ids[i], 'id_jogo': bg_ids[i]} for i in range(len(bg_ids))]

def _get_players_bgs_ids_from_ludopedia(players: DataFrame) -> list:
    """Get all bgs from players who have ludopedia id

    Args:
        conn (Connection): db connection to query users ludopedia_nicknames

    Returns:
        list: a list of dicts containing the owner id and game id  
    """
    ls = LudopediaScrapper()   
    ids = players.query('LUDOPEDIA_NICKNAME.notnull()')['ID'].to_list()
    ls = LudopediaScrapper()
    collection = []
    for id in ids:
        games = ls.get_user_collection(id)
        for game in games:
            collection.append({'id_dono':id, 'id_jogo':game['id_jogo']})
    return collection


def _get_all_bgs_taxonomy_metadata(bgs : list[dict], id_taxonomy_column : str, taxonomy_column : str) -> list:
    """Gets all board game taxonomy such as mechanics, themes, categories or domains.

    Args:
        bgs (list[dict]): list of bgs. each element is a dict got from _get_all_players_bgs function.
        id_taxonomy_column (str): name of id column for the correspondent taxonomy on ludopedia
        taxonomy_column (str): name of value column for the correspondent taxonomy on ludopedia

    Returns:
        list: list of tuples. each element is the board game id with the correspondent taxonomy id
    """
    data = []
    for bg in bgs:
        game_id = bg['id_jogo']
        metadata_id = list(map(lambda x : x[id_taxonomy_column], bg[taxonomy_column]))
        data.extend(list(zip(itertools.repeat(game_id), metadata_id)))
    return data

def _get_game_lst_dt_plyd_column() -> dict:
    """Gets the last data a game was played based on matches table

    Returns:
        dict: game as key and date as value.
    """
    matches_url = get_url('matches')
    matches = pd.read_csv(matches_url)
    matches.drop_duplicates(subset=['game'], keep='last', inplace=True)
    return dict(zip(matches['game'], matches['date']))

@timeit
def get_all_bgs(players : DataFrame) -> list:
    """Get all the ludopedia metadata from every board game

    Args:
        conn (Connection): db connection to query users ludopedia_nicknames

    Returns:
        list: all board game metadata
    """
    ls = LudopediaScrapper()
    all_bgs = _get_players_bgs_ids_from_sheet() + _get_players_bgs_ids_from_ludopedia(players)
    bgs_ids = [id for id in all_bgs]
    games_ids = [id for id in bgs_ids]
    bgs = []
    for id in games_ids:
        game = ls.get_bg_metadata(id.get('id_jogo'))
        game['id_dono'] = id.get('id_dono')
        bgs.append(game)
    return bgs

@timeit
def create_bg_mechanics_table(bgs : list[dict]) -> DataFrame:
    """Creates board game mechanics table for each board game in collection

    Args:
        bgs (list[dict]): list of boardgames and its mechanics

    Returns:
        DataFrame: dataframe with game id, and mechanic id columns.  
    """
    columns = ['GAME_ID', 'MECHANIC_ID']
    data = _get_all_bgs_taxonomy_metadata(bgs, 'id_mecanica', 'mecanicas')
    return pd.DataFrame(data, columns=columns)

@timeit
def create_bg_themes_table(bgs : list[dict]) -> DataFrame:
    """Creates board game themes table for each board game in collection

    Args:
        bgs (list[dict]): list of boardgames and its themes

    Returns:
        DataFrame: dataframe with game id, and theme id columns.  
    """
    columns = ['GAME_ID', 'THEME_ID']
    data = _get_all_bgs_taxonomy_metadata(bgs, 'id_tema', 'temas')
    return pd.DataFrame(data, columns=columns)

@timeit
def create_bg_categories_table(bgs : list[dict]) -> DataFrame:
    """Creates board game categories table for each board game in collection

    Args:
        bgs (list[dict]): list of boardgames and its categories

    Returns:
        DataFrame: dataframe with game id, and category id columns.  
    """
    columns = ['GAME_ID', 'CATEGORY_ID']
    data = _get_all_bgs_taxonomy_metadata(bgs, 'id_categoria', 'categorias')
    return pd.DataFrame(data, columns=columns)

@timeit
def create_bg_domains_table(games_urls: DataFrame) -> DataFrame:
    """Creates board game domains table for each board game in collection

    Args:
        bgs (list[dict]): list of boardgames and its domains

    Returns:
        DataFrame: dataframe with game id, and category id columns.  
    """
    ls = LudopediaScrapper()
    ids = games_urls['ID'].tolist()
    domains = games_urls['LUDOPEDIA_URL'].apply(ls.get_game_domain).tolist()
    return pd.DataFrame({
        'GAME_ID' : ids,
        'DOMAIN_ID' : domains
    })

@timeit
def create_bg_owners_table(bgs : list[dict]) -> DataFrame:
    """Creates board game owner table for each board game in collection

    Args:
        bgs (list[dict]): list of boardgames and its owners

    Returns:
        DataFrame: dataframe with game id, and category id columns.         
    """
    user_id = [bg['id_dono'] for bg in bgs]
    game_id = [bg['id_jogo'] for bg in bgs]
    df = pd.DataFrame({'USER_ID' : user_id, 'GAME_ID' : game_id})
    return df.drop_duplicates()

@timeit
def create_board_games_table(bgs : list[dict]) -> DataFrame:
    """Creates board game table

    Args:
        bgs (list[dict]): list of users boardgames

    Returns:
        DataFrame: dataframe with following columns:
            - 'ID'
            - 'NAME'
            - 'GAME_TYPE'
            - 'LUDOPEDIA_URL'
            - 'BGG_URL'
            - 'MIN_AGE'
            - 'PLAYING_TIME'
            - 'MIN_PLAYERS'
            - 'MAX_PLAYERS'
            - 'LST_DT_PLAYED'
            - 'WEIGHT'
            - 'MIN_BEST_PLAYERS'
            - 'MAX_BEST_PLAYERS'
    """
    ded_bg          = {bg['id_jogo']: bg for bg in bgs}.values() #deduplicating bgs
    id              = [bg['id_jogo'] for bg in ded_bg]
    name            = [bg['nm_jogo'] for bg in ded_bg]
    game_type       = [bg['tp_jogo'].upper() for bg in ded_bg]
    ludopedia_url   = [bg['link'] for bg in ded_bg]
    bgg_url         = [bgg.get_BGG_url_by_Ludopedia_search(os.path.basename(url)) for url in ludopedia_url]
    min_age         = [bg['idade_minima'] for bg in ded_bg]
    playing_time    = [bg['vl_tempo_jogo'] for bg in ded_bg]
    min_players     = [bg['qt_jogadores_min'] for bg in ded_bg]
    max_players     = [bg['qt_jogadores_max'] for bg in ded_bg]
    games_played    = _get_game_lst_dt_plyd_column()
    df = pd.DataFrame({
        'ID' : id, 
        'NAME' : name,
        'GAME_TYPE' : game_type,
        'LUDOPEDIA_URL' : ludopedia_url,
        'BGG_URL' : bgg_url,
        'MIN_AGE': min_age,
        'PLAYING_TIME': playing_time,
        'MIN_PLAYERS': min_players,
        'MAX_PLAYERS': max_players
    })
    df['LST_DT_PLAYED'] = df['NAME'].map(games_played)
    df['WEIGHT'] = df['BGG_URL'].map(bgg.get_BGG_game_weight, na_action='ignore')
    df[['MIN_BEST_PLAYERS', 'MAX_BEST_PLAYERS']] = df['BGG_URL'].apply(bgg.get_BGG_min_max_best_players).to_list()
    return df