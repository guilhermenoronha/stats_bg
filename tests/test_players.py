import pandas as pd
from unittest.mock import patch
from pandas.testing import assert_frame_equal, assert_series_equal
from stats_bg.players import create_players_table, _create_player_id_column


@patch("stats_bg.players.pd.read_csv")
@patch("stats_bg.players.get_url")
@patch("stats_bg.players._create_player_id_column")
def test_create_players_table(mock__create_player_id_column, mock_get_url, mock_read_csv):
    expected_df = pd.DataFrame({
        "NAME": ["George Constanza", "Elaine Benes"],
        "LUDOPEDIA_NICKNAME": ["Art Vandelay", "Nip"],
        "MEMBERSHIP": ["M", "G"]
    })

    mock_get_url.return_value = "fake_url"
    mock_read_csv.return_value = expected_df
    mock__create_player_id_column.return_value = pd.Series()

    result = create_players_table()

    assert_frame_equal(result, expected_df)



@patch("stats_bg.players.LudopediaScrapper")
def test_create_player_id_column(mock_ludopedia_scrapper):

    def _mock_ids(x):
        return "1"

    mock_instance = mock_ludopedia_scrapper.return_value
    mock_instance.get_user_id =  lambda x: _mock_ids(x)
    
    expected_value = pd.Series([1, 1], dtype="Int64")
    result = _create_player_id_column(pd.Series(["George Constanza", "b"]))
    
    assert_series_equal(expected_value, result)


@patch("stats_bg.players.LudopediaScrapper")
def test_create_player_id_column_with_nan(mock_ludopedia_scrapper):

    mock_instance = mock_ludopedia_scrapper.return_value
    mock_instance.get_user_id = lambda x: 1

    nicknames = pd.Series(["George Constanza", None])

    result = _create_player_id_column(nicknames)

    expected = pd.Series([1, pd.NA], dtype="Int64")

    assert_series_equal(expected, result)