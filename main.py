from stats_bg.players import create_players_table
from stats_bg.board_game_taxonomy import create_boardgame_metadata_table
from stats_bg.matches import create_matches_table
from stats_bg.postgres_utils import PostgresUtils
from decouple import config
import stats_bg.board_games as bg
import logging
import argparse


def main():
    logging.basicConfig(level=logging.INFO)
    CLI = argparse.ArgumentParser()
    CLI.add_argument("--mode", type=str, default="all")
    args = CLI.parse_args()
    user = config("PG_USER")
    passwd = config("PG_PASSWD")
    host = config("HOST")
    port = config("PORT")
    db = config("DB")
    schema = config("SCHEMA")
    sql_string = f"postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}"
    pu = PostgresUtils(sql_string)
    mode = args.mode
    if mode in ["players", "all"]:
        pu.save_table(create_players_table(), schema, "PLAYERS")
    if mode in ["taxonomy", "all"]:
        for taxonomy in ["themes", "categories", "domains", "mechanics"]:
            pu.save_table(
                create_boardgame_metadata_table(taxonomy),
                schema,
                taxonomy.upper(),
            )
    if mode in ["boardgames", "all"]:
        try:
            bgs
        except:
            players = pu.get_table_data(
                db, schema, "PLAYERS", ["ID", "LUDOPEDIA_NICKNAME"]
            )
            bgs = bg.get_all_bgs(players)
        pu.save_table(bg.create_board_games_table(bgs), schema, "GAMES")
        pu.save_table(bg.create_bg_owners_table(bgs), schema, "BG_OWNERS")
    if mode in ["metadata", "all"]:
        try:
            bgs
        except:
            players = pu.get_table_data(db, schema, "PLAYERS", ["ID", "LUDOPEDIA_NICKNAME"])
            bgs = bg.get_all_bgs(players)
        games = pu.get_games_data(db, schema, ["ID", "LUDOPEDIA_URL"])
        pu.save_table(bg.create_bg_domains_table(games), schema, "BG_DOMAINS")
        pu.save_table(bg.create_bg_themes_table(bgs), schema, "BG_THEMES")
        pu.save_table(bg.create_bg_categories_table(bgs), schema, "BG_CATEGORIES")
        pu.save_table(bg.create_bg_mechanics_table(bgs), schema, "BG_MECHANICS")
    if mode in ["matches", "all"]:
        matches_table = create_matches_table()
        pu.save_table(matches_table, schema, "MATCHES")


if __name__ == "__main__":
    main()
