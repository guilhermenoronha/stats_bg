import pandas as pd
from unittest.mock import MagicMock, patch

from stats_bg.postgres_utils import (
    get_games_data,
    get_players_data,
    save_table,
    truncate_table,
)


def _mock_engine_with_connection():
    engine = MagicMock()
    conn = MagicMock()
    engine.connect.return_value.__enter__.return_value = conn
    return engine, conn


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.pd.read_sql")
def test_get_players_data_returns_query_result(mock_read_sql, mock_create_engine):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    expected = pd.DataFrame({"ID": [1], "LUDOPEDIA_NICKNAME": ["nick"]})
    mock_read_sql.return_value = expected

    result = get_players_data("conn", "DB", "public", ["ID", "LUDOPEDIA_NICKNAME"])

    assert result.equals(expected)
    assert mock_read_sql.call_count == 1
    qry = mock_read_sql.call_args[0][0]
    assert qry == 'SELECT "ID", "LUDOPEDIA_NICKNAME" FROM DB.public."PLAYERS"'
    assert mock_read_sql.call_args[0][1] is conn


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.save_table")
@patch("stats_bg.postgres_utils.pd.read_sql")
def test_get_players_data_creates_table_on_read_failure(
    mock_read_sql, mock_save_table, mock_create_engine
):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    expected = pd.DataFrame({"ID": [1], "LUDOPEDIA_NICKNAME": ["nick"]})
    mock_read_sql.side_effect = [Exception("missing table"), expected]

    result = get_players_data("conn", "DB", "public", ["ID", "LUDOPEDIA_NICKNAME"])

    assert result.equals(expected)
    mock_save_table.assert_called_once()
    args = mock_save_table.call_args[0]
    assert args[1:] == ("public", "conn", "PLAYERS")


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.pd.read_sql")
def test_get_games_data_returns_query_result(mock_read_sql, mock_create_engine):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    expected = pd.DataFrame({"ID": [1], "NAME": ["Catan"]})
    mock_read_sql.return_value = expected

    result = get_games_data("conn", "DB", "public", ["ID", "NAME"])

    assert result.equals(expected)
    qry = mock_read_sql.call_args[0][0]
    assert qry == 'SELECT DISTINCT "ID", "NAME" FROM DB.public."GAMES"'
    assert mock_read_sql.call_args[0][1] is conn


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.save_table")
@patch("stats_bg.postgres_utils.bg.create_board_games_table")
@patch("stats_bg.postgres_utils.bg.get_all_bgs")
@patch("stats_bg.postgres_utils.get_players_data")
@patch("stats_bg.postgres_utils.pd.read_sql")
def test_get_games_data_bootstraps_games_table_on_read_failure(
    mock_read_sql,
    mock_get_players_data,
    mock_get_all_bgs,
    mock_create_board_games_table,
    mock_save_table,
    mock_create_engine,
):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine

    players = pd.DataFrame({"ID": [1], "LUDOPEDIA_NICKNAME": ["nick"]})
    bgs_raw = [{"id": 10, "name": "Catan"}]
    bgs_df = pd.DataFrame({"ID": [10], "NAME": ["Catan"]})
    expected = pd.DataFrame({"ID": [10], "NAME": ["Catan"]})

    mock_read_sql.side_effect = [Exception("missing table"), expected]
    mock_get_players_data.return_value = players
    mock_get_all_bgs.return_value = bgs_raw
    mock_create_board_games_table.return_value = bgs_df

    result = get_games_data("conn", "DB", "public", ["ID", "NAME"])

    assert result.equals(expected)
    mock_get_players_data.assert_called_once_with(
        "conn", "DB", "public", ["ID", "LUDOPEDIA_NICKNAME"]
    )
    mock_get_all_bgs.assert_called_once_with(players)
    mock_create_board_games_table.assert_called_once_with(bgs_raw)
    mock_save_table.assert_called_once_with(bgs_df, "public", "conn", "GAMES")


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.truncate_table")
@patch("pandas.DataFrame.to_sql")
def test_save_table_replace_truncates_and_appends(
    mock_to_sql, mock_truncate_table, mock_create_engine
):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    df = pd.DataFrame({"A": [1, 2]})

    save_table(df, "public", "conn", "TBL", mode="replace")

    mock_truncate_table.assert_called_once_with("conn", "public", "TBL")
    mock_to_sql.assert_called_once_with(
        name="TBL", con=conn, if_exists="append", schema="public", index=False
    )


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.truncate_table")
@patch("pandas.DataFrame.to_sql")
def test_save_table_append_does_not_truncate(
    mock_to_sql, mock_truncate_table, mock_create_engine
):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    df = pd.DataFrame({"A": [1]})

    save_table(df, "public", "conn", "TBL", mode="append")

    mock_truncate_table.assert_not_called()
    mock_to_sql.assert_called_once_with(
        name="TBL", con=conn, if_exists="append", schema="public", index=False
    )


def test_save_table_invalid_mode_raises_value_error():
    df = pd.DataFrame({"A": [1]})

    try:
        save_table(df, "public", "conn", "TBL", mode="invalid")
        assert False, "ValueError was not raised"
    except ValueError as exc:
        assert str(exc) == "Mode must be 'append' or 'replace'!"


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.text", side_effect=lambda x: x)
def test_truncate_table_executes_truncate_and_commit(mock_text, mock_create_engine):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine

    truncate_table("conn", "public", "TBL")

    mock_text.assert_called_once_with('TRUNCATE TABLE public."TBL"')
    conn.execute.assert_called_once_with('TRUNCATE TABLE public."TBL"')
    conn.commit.assert_called_once()


@patch("stats_bg.postgres_utils.logging.warning")
@patch("stats_bg.postgres_utils.create_engine", side_effect=Exception("db error"))
def test_truncate_table_logs_warning_on_failure(mock_create_engine, mock_warning):
    truncate_table("conn", "public", "TBL")

    mock_create_engine.assert_called_once_with("conn")
    assert mock_warning.call_count == 1
    assert "wasn't truncated" in mock_warning.call_args[0][0]
