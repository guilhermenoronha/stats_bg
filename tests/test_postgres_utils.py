import pandas as pd
import pytest
from unittest.mock import MagicMock, patch

from stats_bg.postgres_utils import PostgresUtils


def _mock_engine_with_connection():
    engine = MagicMock()
    conn = MagicMock()
    engine.connect.return_value.__enter__.return_value = conn
    return engine, conn


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.pd.read_sql")
def test_get_table_data_returns_query_result(mock_read_sql, mock_create_engine):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    expected = pd.DataFrame({"ID": [1], "NAME": ["Catan"]})
    mock_read_sql.return_value = expected
    postgres_utils = PostgresUtils("conn")

    result = postgres_utils.get_table_data("DB", "public", "games", ["ID", "NAME"])

    assert result.equals(expected)
    assert mock_read_sql.call_count == 1
    qry = mock_read_sql.call_args[0][0]
    assert qry == 'SELECT "ID", "NAME" FROM DB.public."games"'
    assert mock_read_sql.call_args[0][1] is conn


@patch("stats_bg.postgres_utils.pd.read_sql")
@patch("stats_bg.postgres_utils.create_engine")
def test_get_table_data_raises_runtime_error_on_read_failure(
    mock_create_engine, mock_read_sql
):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    mock_read_sql.side_effect = Exception("missing table")
    postgres_utils = PostgresUtils("conn")

    with pytest.raises(RuntimeError) as exc_info:
        postgres_utils.get_table_data(
            "DB", "public", "players", ["ID", "LUDOPEDIA_NICKNAME"]
        )

    assert 'Failed to read table DB.public."players"' in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, Exception)
    assert str(exc_info.value.__cause__) == "missing table"


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.pd.read_sql")
def test_get_games_data_returns_query_result(mock_read_sql, mock_create_engine):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    expected = pd.DataFrame({"ID": [1], "NAME": ["Catan"]})
    mock_read_sql.return_value = expected
    postgres_utils = PostgresUtils("conn")

    result = postgres_utils.get_games_data("DB", "public", ["ID", "NAME"])

    assert result.equals(expected)
    qry = mock_read_sql.call_args[0][0]
    assert qry == 'SELECT DISTINCT "ID", "NAME" FROM DB.public."GAMES"'
    assert mock_read_sql.call_args[0][1] is conn


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.PostgresUtils.save_table")
@patch("stats_bg.postgres_utils.bg.create_board_games_table")
@patch("stats_bg.postgres_utils.bg.get_all_bgs")
@patch("stats_bg.postgres_utils.PostgresUtils.get_table_data")
@patch("stats_bg.postgres_utils.pd.read_sql")
def test_get_games_data_bootstraps_games_table_on_read_failure(
    mock_read_sql,
    mock_get_table_data,
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
    mock_get_table_data.return_value = players
    mock_get_all_bgs.return_value = bgs_raw
    mock_create_board_games_table.return_value = bgs_df
    postgres_utils = PostgresUtils("conn")

    result = postgres_utils.get_games_data("DB", "public", ["ID", "NAME"])

    assert result.equals(expected)
    mock_get_table_data.assert_called_once_with(
        "DB", "public", "PLAYERS", ["ID", "LUDOPEDIA_NICKNAME"]
    )
    mock_get_all_bgs.assert_called_once_with(players)
    mock_create_board_games_table.assert_called_once_with(bgs_raw)
    mock_save_table.assert_called_once_with(bgs_df, "public", "GAMES")


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.PostgresUtils.truncate_table")
@patch("pandas.DataFrame.to_sql")
def test_save_table_replace_truncates_and_appends(
    mock_to_sql, mock_truncate_table, mock_create_engine
):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    df = pd.DataFrame({"A": [1, 2]})
    postgres_utils = PostgresUtils("conn")

    postgres_utils.save_table(df, "public", "TBL", mode="replace")

    mock_truncate_table.assert_called_once_with("public", "TBL")
    mock_to_sql.assert_called_once_with(
        name="TBL", con=conn, if_exists="append", schema="public", index=False
    )


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.PostgresUtils.truncate_table")
@patch("pandas.DataFrame.to_sql")
def test_save_table_append_does_not_truncate(
    mock_to_sql, mock_truncate_table, mock_create_engine
):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    df = pd.DataFrame({"A": [1]})
    postgres_utils = PostgresUtils("conn")

    postgres_utils.save_table(df, "public", "TBL", mode="append")

    mock_truncate_table.assert_not_called()
    mock_to_sql.assert_called_once_with(
        name="TBL", con=conn, if_exists="append", schema="public", index=False
    )


@patch("stats_bg.postgres_utils.create_engine")
def test_save_table_invalid_mode_raises_value_error(mock_create_engine):
    engine, _ = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    df = pd.DataFrame({"A": [1]})
    postgres_utils = PostgresUtils("conn")

    try:
        postgres_utils.save_table(df, "public", "TBL", mode="invalid")
        assert False, "ValueError was not raised"
    except ValueError as exc:
        assert str(exc) == "Mode must be 'append' or 'replace'!"


@patch("stats_bg.postgres_utils.create_engine")
@patch("stats_bg.postgres_utils.text", side_effect=lambda x: x)
def test_truncate_table_executes_truncate_and_commit(mock_text, mock_create_engine):
    engine, conn = _mock_engine_with_connection()
    mock_create_engine.return_value = engine
    postgres_utils = PostgresUtils("conn")

    postgres_utils.truncate_table("public", "TBL")

    mock_text.assert_called_once_with('TRUNCATE TABLE public."TBL"')
    conn.execute.assert_called_once_with('TRUNCATE TABLE public."TBL"')
    conn.commit.assert_called_once()


@patch("stats_bg.postgres_utils.logging.warning")
@patch("stats_bg.postgres_utils.create_engine")
def test_truncate_table_logs_warning_on_failure(mock_create_engine, mock_warning):
    engine = MagicMock()
    engine.connect.side_effect = Exception("db error")
    mock_create_engine.return_value = engine
    postgres_utils = PostgresUtils("conn")

    postgres_utils.truncate_table("public", "TBL")

    mock_create_engine.assert_called_once_with("conn")
    assert mock_warning.call_count == 1
    assert "wasn't truncated" in mock_warning.call_args[0][0]
