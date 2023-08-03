from scrapper.ludopedia_scrapper import LudopediaScrapper
from sqlite3 import Connection
import logging
import pandas as pd

def create_boardgame_metadata_table(conn : Connection, table_name : str, metadata_type : str):
    """Creates a table with Ludopedia metadatas.
        The Ludopedia stores the following boardgames metadata:

    Args:
        conn (Connection): Database connection where the table will be recorded
        table_name (str): The name of the table in the database
        metadata_type (str): Type of metadata to be created. Available options:
            -  themes: describe the environments, ages, or universes of the boardgame
            -  categories: describe the essence of the boardgame according to main components, gameplay style and profile
            -  domains:  describe the main audience of the boardgame
            -  mechanics: describe how the boardgame is played
    """
    if metadata_type == 'themes':
        url = 'https://ludopedia.com.br/temas'
    elif metadata_type == 'categories': 
        url = 'https://ludopedia.com.br/categorias'
    elif metadata_type == 'domains':
        url = 'https://ludopedia.com.br/dominios'
    elif metadata_type == 'mechanics':
        url = 'https://ludopedia.com.br/mecanicas'
    else:
        raise ValueError('Error! Invalid option for metadata_type')
    ls = LudopediaScrapper()
    data = ls.get_ludopedia_taxonomy(url)
    df = pd.DataFrame.from_records(data)
    df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
    logging.info(f'Table {table_name} was successfully created with {len(df)} rows.')
