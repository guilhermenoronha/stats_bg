import pandas as pd
from unittest.mock import patch
from pandas.testing import assert_frame_equal

from stats_bg.matches import create_matches_table


@patch("stats_bg.matches.pd.read_csv")
@patch("stats_bg.matches.get_url")
def test_create_matches_table_reads_matches_sheet(mock_get_url, mock_read_csv):
    raw_df = pd.DataFrame(
        {
            "date": ["2026-01-01"],
            "host_name": ["Alice"],
            "match_id": [1],
            "game_name": ["Catan"],
            "game_owner": ["Bob"],
            "winner": ["Alice"],
        }
    )
    mock_get_url.return_value = "fake_matches_url"
    mock_read_csv.return_value = raw_df

    result = create_matches_table()

    mock_get_url.assert_called_once_with("matches")
    mock_read_csv.assert_called_once_with("fake_matches_url")
    assert_frame_equal(result, raw_df)


@patch("stats_bg.matches.pd.read_csv")
@patch("stats_bg.matches.get_url")
def test_create_matches_table_forward_fills_target_columns(mock_get_url, mock_read_csv):
    raw_df = pd.DataFrame(
        {
            "date": ["2026-01-01", None, None],
            "host_name": ["Alice", None, None],
            "match_id": [10, None, None],
            "game_name": ["Catan", None, None],
            "game_owner": ["Bob", None, None],
            "winner": ["Alice", None, "Carol"],
        }
    )
    mock_get_url.return_value = "fake_matches_url"
    mock_read_csv.return_value = raw_df

    result = create_matches_table()

    expected = pd.DataFrame(
        {
            "date": ["2026-01-01", "2026-01-01", "2026-01-01"],
            "host_name": ["Alice", "Alice", "Alice"],
            "match_id": [10.0, 10.0, 10.0],
            "game_name": ["Catan", "Catan", "Catan"],
            "game_owner": ["Bob", "Bob", "Bob"],
            "winner": ["Alice", None, "Carol"],
        }
    )
    assert_frame_equal(result, expected)

