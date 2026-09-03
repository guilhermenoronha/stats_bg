import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from unittest.mock import patch

from stats_bg.board_game_taxonomy import create_boardgame_metadata_table


@pytest.mark.parametrize(
    "metadata_type, expected_url",
    [
        ("themes", "https://ludopedia.com.br/temas"),
        ("categories", "https://ludopedia.com.br/categorias"),
        ("domains", "https://ludopedia.com.br/dominios"),
        ("mechanics", "https://ludopedia.com.br/mecanicas"),
    ],
)
@patch("stats_bg.board_game_taxonomy.LudopediaScraper")
def test_create_boardgame_metadata_table(mock_ludopedia_scraper, metadata_type, expected_url):
    scraper = mock_ludopedia_scraper.return_value
    scraper.get_ludopedia_taxonomy.return_value = [
        {"id": 1, "name": "Adventure"},
        {"id": 2, "name": "Fantasy"},
    ]

    result = create_boardgame_metadata_table(metadata_type)

    expected = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Adventure", "Fantasy"],
        }
    )
    assert_frame_equal(result, expected)
    scraper.get_ludopedia_taxonomy.assert_called_once_with(expected_url)


def test_create_boardgame_metadata_table_invalid_metadata_type():
    with pytest.raises(ValueError, match="Invalid option"):
        create_boardgame_metadata_table("invalid")
