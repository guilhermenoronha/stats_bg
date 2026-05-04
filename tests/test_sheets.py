from unittest.mock import patch
from stats_bg.sheets import get_url


@patch("stats_bg.sheets.config")
def test_get_url(sheet_id):
    sheet_id.return_value = 5
    result = get_url("name")
    expected_result = "https://docs.google.com/spreadsheets/d/5/gviz/tq?tqx=out:csv&sheet=name"
    assert result == expected_result