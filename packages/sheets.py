from decouple import config

def get_url(sheet_name : str) -> str:
    """Method to get the full URL to google sheets where the data lies. 
       The sheed_id is an env variable setup previously. 

    Args:
        sheet_name (str): the name of the sheet 

    Returns:
        str: the full URL
    """
    sheet_id = config('SHEET_ID')
    return f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'