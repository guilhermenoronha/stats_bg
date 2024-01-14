import os
import requests
from decouple import config
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from contextlib import closing


class LudopediaScrapper:
    def __init__(self) -> None:
        """Constructor which creates a header for a good request in https://ludopedia.com.br
        The user must have an account and a access key on this site before call this constructor
        """
        self.headers = {"Authorization": f'Bearer {config("ACCESS_KEY")}'}

    def _get_ludopedia_response(self, url: str) -> requests.Response:
        """Method to request the Ludopedia url response. Its append the url with the headers added on constructor

        Args:
            url (str): the Ludopedia url to be requested

        Raises:
            requests.RequestException: raises error if the response is not ok (Code 200)

        Returns:
            requests.Response: the response of the page
        """
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200:
            return response
        else:
            raise requests.RequestException(
                "An error occurred when requesting url. Check if the url or the access_token is correct."
            )

    def get_user_id(self, username: str) -> str:
        """Get the user id based on username

        Args:
            username (str): the user's username on Ludopedia

        Returns:
            str: the user ID
        """
        url = f"https://ludopedia.com.br/api/v1/usuarios?search={username}"
        response = self._get_ludopedia_response(url)
        data = response.json()
        user = data.get("usuarios")[0]
        return user.get("id_usuario")

    def get_user_collection(self, user_id: str) -> dict:
        """Get the user board game collection based on user ID

        Args:
            user_id (str): user ID on Ludopedia

        Returns:
            dict: a dict with all user's board game collection
        """
        url = f"https://ludopedia.com.br/api/v1/colecao?id_usuario={user_id}&lista=colecao&rows=100"
        response = self._get_ludopedia_response(url)
        data = response.json()
        return data.get("colecao")

    def get_bg_metadata(self, game_id: str) -> dict:
        """Get game metadata based on board game ID

        Args:
            game_id (str): board game ID on Ludopedia

        Returns:
            dict: _description_
        """
        url = f"https://ludopedia.com.br/api/v1/jogos/{game_id}"
        response = self._get_ludopedia_response(url)
        return response.json()

    def get_game_by_name(self, name: str) -> dict:
        """Get board game by name

        Args:
            name (str): whole name of board game

        Raises:
            ValueError: raises error if response returns no data

        Returns:
            dict: board game metadata
        """
        url = f'https://ludopedia.com.br/api/v1/jogos?search={name.replace(" ", "%20")}'
        response = self._get_ludopedia_response(url)
        data = response.json()
        if len(data) != 0:
            id = data["jogos"][0]["id_jogo"]
            game = self._get_game_by_id(id)
            if game["nm_jogo"] == name:
                return game
            else:
                raise ValueError(
                    f'Error! game found is different. Name: {name}. Game found: {game["nm_jogo"]}'
                )
        else:
            raise ValueError("Error! Game not found!")

    def _get_game_by_id(self, id: str) -> dict:
        """Get board game by ID

        Args:
            id (str): Board game ID

        Returns:
            dict: ludopedia metadata containing game id
        """
        url = f"https://ludopedia.com.br/api/v1/jogos/{id}"
        response = self._get_ludopedia_response(url)
        return response.json()

    def get_ludopedia_taxonomy(self, taxonomy_url: str) -> list:
        """Get the Ludopedia taxonomy for board games

        Args:
            taxonomy_url (str): URL with taxonomy metadata

        Raises:
            ValueError: raises error when the response returns no metadata

        Returns:
            list: dicts with id, name, and url for each taxonomy found on the url
        """
        options = Options()
        options.add_argument("--headless")
        with closing(Firefox(options=options)) as browser:
            browser.get(taxonomy_url)
            links = browser.find_elements(By.CLASS_NAME, "full-link")
            if len(links) == 0:
                raise ValueError("Error! Metadata not found. The number of links is 0!")
            return [
                {
                    "ID": os.path.basename(link.get_attribute("href")),
                    "NAME": link.accessible_name[
                        0 : link.accessible_name.find("(") - 1
                    ],
                    "URL": link.get_attribute("href"),
                }
                for link in links
            ]

    def get_game_domain(self, game_url: str) -> str:
        """Get game domain based on game url

        Args:
            game_url (str): game url on Ludopedia

        Returns:
            str: game domain id
        """
        options = Options()
        options.add_argument("--headless")
        with closing(Firefox(options=options)) as browser:
            browser.get(game_url)
            links = browser.find_elements(By.CLASS_NAME, "text-primary")
            for link in links:
                metadata_link = link.get_attribute("href")
                if "dominio" in metadata_link:
                    return os.path.basename(metadata_link)
