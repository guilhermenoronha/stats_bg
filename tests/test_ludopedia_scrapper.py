import pytest
import requests
import pandas as pd
from unittest.mock import patch, MagicMock
from scrapper.ludopedia_scrapper import LudopediaScrapper

@patch("scrapper.ludopedia_scrapper.Session")
def test_get_ludopedia_response_success(mock_session):
    mock_response = MagicMock()
    mock_response.status_code = 200

    mock_session_instance = MagicMock()
    mock_session_instance.get.return_value = mock_response
    mock_session.return_value = mock_session_instance

    scraper = LudopediaScrapper()
    scraper.headers = {"Authorization": "token"}

    result = scraper._get_ludopedia_response("http://fake-url")

    assert result == mock_response
    mock_session_instance.get.assert_called_once_with(
        url="http://fake-url",
        headers=scraper.headers,
        timeout=scraper.request_timeout_seconds,
    )

@patch("scrapper.ludopedia_scrapper.Session")
def test_get_ludopedia_response_error(mock_session):
    mock_response = MagicMock()
    mock_response.status_code = 500

    mock_session_instance = MagicMock()
    mock_session_instance.get.return_value = mock_response
    mock_session.return_value = mock_session_instance

    scraper = LudopediaScrapper()
    scraper.headers = {"Authorization": "token"}

    with pytest.raises(requests.RequestException):
        scraper._get_ludopedia_response("http://fake-url")


@patch("scrapper.ludopedia_scrapper.Session")
def test_get_ludopedia_response_rate_limit_error(mock_session):
    mock_response = MagicMock()
    mock_response.status_code = 429

    mock_session_instance = MagicMock()
    mock_session_instance.get.return_value = mock_response
    mock_session.return_value = mock_session_instance

    scraper = LudopediaScrapper()
    scraper.headers = {"Authorization": "token"}

    with pytest.raises(requests.RequestException) as exc_info:
        scraper._get_ludopedia_response("http://fake-url")

    assert "rate limit exceeded" in str(exc_info.value)
