from scrapper.ludopedia_scrapper import LudopediaScrapper
from pandas import DataFrame
import pandas as pd


def create_boardgame_metadata_table(metadata_type: str) -> DataFrame:
    """Creates a table with Ludopedia metadatas.
        The Ludopedia stores the following boardgames metadata:

    Args:
        metadata_type (str): Type of metadata to be created. Available options:
            -  themes: describe the environments, ages, or universes of the boardgame
            -  categories: describe the essence of the boardgame according to main components, gameplay style and profile
            -  domains:  describe the main audience of the boardgame
            -  mechanics: describe how the boardgame is played

    Returns:
        DataFrame: dataframe with date, player id, and is host columns.
    """
    if metadata_type == "themes":
        url = "https://ludopedia.com.br/temas"
    elif metadata_type == "categories":
        url = "https://ludopedia.com.br/categorias"
    elif metadata_type == "domains":
        url = "https://ludopedia.com.br/dominios"
    elif metadata_type == "mechanics":
        url = "https://ludopedia.com.br/mecanicas"
    else:
        raise ValueError("Error! Invalid option for metadata_type")
    ls = LudopediaScrapper()
    data = ls.get_ludopedia_taxonomy(url)
    return pd.DataFrame.from_records(data)
