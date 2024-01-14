from stats_bg.players import create_players_table
from stats_bg.board_game_taxonomy import create_boardgame_metadata_table
from stats_bg.attendances import create_attendances_table
from stats_bg.matches import create_matches_table
from stats_bg.postgres_utils import get_games_data, get_players_data, save_table
from decouple import config
import stats_bg.board_games as bg
import logging
import argparse

def main():
    logging.basicConfig(level=logging.INFO)
    CLI = argparse.ArgumentParser()
    CLI.add_argument('--mode', type=str, default='all')
    args = CLI.parse_args()
    user = config('PG_USER')
    passwd = config('PG_PASSWD')
    host = config('HOST')
    port = config('PORT')
    db = config('DB')
    schema = config('SCHEMA')
    sql_string = f'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'
    mode = args.mode
    if mode in ['players', 'all']:
        save_table(create_players_table(), schema, sql_string, 'PLAYERS')
    if mode in ['taxonomy', 'all']:
        for taxonomy in ['themes', 'categories', 'domains', 'mechanics']:
             save_table(create_boardgame_metadata_table(taxonomy), schema, 
                        sql_string, taxonomy.upper())
    if mode in ['boardgames', 'all']:
        try:
             bgs
        except:
             players = get_players_data(sql_string, db, schema, ['ID', 'LUDOPEDIA_NICKNAME'])
             bgs = bg.get_all_bgs(players)
        save_table(bg.create_board_games_table(bgs), schema, sql_string, 'GAMES')
        save_table(bg.create_bg_owners_table(bgs), schema, sql_string, 'BG_OWNERS')
    if mode in ['metadata' ,'all']:
        try:
             bgs
        except:
             players = get_players_data(sql_string, db, schema, ['ID', 'LUDOPEDIA_NICKNAME'])
             bgs = bg.get_all_bgs(players)
        games = get_games_data(sql_string, db, schema, ['ID', 'LUDOPEDIA_URL'])
        save_table(bg.create_bg_domains_table(games), schema, sql_string, 'BG_DOMAINS')
        save_table(bg.create_bg_themes_table(bgs), schema, sql_string, 'BG_THEMES')
        save_table(bg.create_bg_categories_table(bgs), schema, sql_string, 'BG_CATEGORIES')
        save_table(bg.create_bg_mechanics_table(bgs), schema, sql_string, 'BG_MECHANICS')
    if mode in ['matches', 'all']:
        players = get_players_data(sql_string, db, schema, ['ID', 'NAME'])
        save_table(create_attendances_table(players), schema, sql_string, 'ATTENDANCES')
        games = get_games_data(sql_string, db, schema, ['NAME', 'ID'])
        save_table(create_matches_table(players, games), schema, sql_string, 'MATCHES')

if __name__ == '__main__':
    main()