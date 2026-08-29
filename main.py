from stats_bg.players import create_players_table
from stats_bg.board_game_taxonomy import create_boardgame_metadata_table
from stats_bg.matches import create_matches_table
from stats_bg.postgres_utils import PostgresUtils
from decouple import config
import stats_bg.board_games as bg
import logging
import argparse
import pandas as pd


def main():
    logging.basicConfig(level=logging.INFO)
    CLI = argparse.ArgumentParser()
    CLI.add_argument("--mode", type=str, default="all")
    CLI.add_argument("--increment_mode", type=str, default="upsert")
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
    search = args.increment_mode
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
        players = pu.get_table_data(
            db, schema, "PLAYERS", ["ID", "LUDOPEDIA_NICKNAME"]
        )        
        if search == "upsert":
            # ACHAR MODO DE ADICIONAR UM JOGO COMPRADO POR ALGUEM QUE OUTRA PESSOA TENHA
            current_owners = pu.get_table_data(db, schema, "BG_OWNERS", ["USER_ID", "GAME_ID"])
            users_bgs = pd.DataFrame(bg.get_players_bgs_ids_from_ludopedia(players))
            # block to delete the owners who don't have in collection anymore.
            # idx vars are the compound keys for BG_OWNERS table
            idx_users = pd.MultiIndex.from_arrays([users_bgs['id_jogo'], users_bgs['id_dono']])
            idx_owners = pd.MultiIndex.from_arrays([current_owners['GAME_ID'], current_owners['USER_ID']])
            deleted_bgs = current_owners[~idx_owners.isin(idx_users)]
            if len(deleted_bgs) > 0:
                # Cria uma lista de strings no formato "(GAME_ID, USER_ID)"
                tuples = [f'({row["GAME_ID"]}, {row["USER_ID"]})' for _, row in deleted_bgs.iterrows()]
                where_condition = f'("GAME_ID", "USER_ID") IN ({", ".join(tuples)})'
                pu.delete_table_data(db, schema, "BG_OWNERS", where_condition)
            # block to add new owners
            added_bgs = users_bgs[~idx_users.isin(idx_owners)]
            if len(added_bgs) > 0:
                added_bgs = added_bgs.rename(columns={'id_jogo': 'GAME_ID', 'id_dono': 'USER_ID'})
                pu.save_table(added_bgs, schema, "BG_OWNERS", mode="append")
            # block to add new the boardgames the owners acquired.
            current_bgs = pu.get_table_data(db, schema, "GAMES", ["ID", "NAME"])
            new_bgs = users_bgs[~users_bgs['id_jogo'].isin(current_bgs["ID"])]
            new_bgs = bg.get_bgs(new_bgs)
            if len(new_bgs) > 0:
                bgs = bg.create_board_games_table(new_bgs)
                pu.save_table(bgs, schema, "GAMES", mode="append")
            # block to add played boardgames without owners
            matches_table = create_matches_table()
            bg_names_without_owners = matches_table[~matches_table["game_name"].isin(current_bgs["NAME"])]
            dedup_bg_names_without_owners = bg_names_without_owners["game_name"].drop_duplicates().to_list()
            bgs_without_owners = bg.get_bgs_by_name(dedup_bg_names_without_owners)         
            bgs =  bg.create_board_games_table(bgs_without_owners)
            pu.save_table(bgs, schema, "GAMES", mode="append")    
        elif search == "full_refresh":
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
