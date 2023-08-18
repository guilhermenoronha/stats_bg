from packages.players import create_players_table
from packages.board_game_taxonomy import create_boardgame_metadata_table
from packages.board_games import get_all_bgs, create_bg_category_table, create_bg_domains_table, create_bg_mechanics_table, \
                                 create_bg_owners_table, create_bg_themes_table, create_board_games_table
from packages.attendances import create_attendances_table
from packages.matches import create_matches_table
import logging
import sqlite3



def main():
    logging.basicConfig(level=logging.INFO)
    conn = sqlite3.connect('bg.db')
    create_players_table(conn)
    bgs = get_all_bgs(conn)
    create_board_games_table(conn, bgs)
    create_boardgame_metadata_table(conn, 'THEMES', 'themes')
    create_boardgame_metadata_table(conn, 'CATEGORIES', 'categories')
    create_boardgame_metadata_table(conn, 'DOMAINS', 'domains')
    create_boardgame_metadata_table(conn, 'MECHANICS', 'mechanics')
    create_bg_domains_table(conn)
    create_bg_owners_table(conn, bgs)
    create_bg_mechanics_table(conn, bgs)
    create_bg_themes_table(conn, bgs)
    create_bg_category_table(conn, bgs)
    create_attendances_table(conn)
    create_matches_table(conn)

if __name__ == '__main__':
    main()