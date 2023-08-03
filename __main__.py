from packages.players import create_players_table
from packages.board_game_taxonomy import create_boardgame_metadata_table
from packages.board_games import get_all_bgs, create_bg_category_table, create_bg_domain_table, create_bg_mechanics_table, \
                                 create_bg_owners_table, create_bg_themes_table, create_board_games_table
from packages.attendances import create_attendances_table
from packages.matches import create_matches_table
from functools import wraps
import time
import logging
import sqlite3

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logging.info(f'Function {func.__name__}{args} {kwargs} Took {total_time:.2f} seconds')
        return result
    return timeit_wrapper

@timeit
def main():
    logging.basicConfig(level=logging.INFO)
    conn = sqlite3.connect('bg.db')
    create_players_table(conn)
    bgs = get_all_bgs(conn)
    create_board_games_table(conn, bgs)
    create_boardgame_metadata_table(conn, 'BG_THEMES', 'themes')
    create_boardgame_metadata_table(conn, 'BG_CATEGORIES', 'categories')
    create_boardgame_metadata_table(conn, 'BG_DOMAINS', 'domains')
    create_boardgame_metadata_table(conn, 'BG_MECHANICS', 'mechanics')
    create_bg_owners_table(conn, bgs)
    create_bg_mechanics_table(conn, bgs)
    create_bg_themes_table(conn, bgs)
    create_bg_category_table(conn, bgs)
    create_attendances_table(conn)
    create_matches_table(conn)

if __name__ == '__main__':
    main()