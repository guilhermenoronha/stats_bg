import pandas as pd
import sqlite3
from decouple import config

# global variables
_conn = sqlite3.connect('bg.db')
_SHEET_ID = config('SHEET_ID')

def _get_url(SHEET_NAME):
    return f'https://docs.google.com/spreadsheets/d/{_SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'

def _get_name_id_mapping(SHEET_NAME, KEY, VALUE):
        url = _get_url(SHEET_NAME)
        df = pd.read_csv(url)
        name_id_mapping = df.set_index(KEY)[VALUE].to_dict()
        return name_id_mapping 

def _create_persons_table():
    try:
        url = _get_url('persons')
        persons  = pd.read_csv(url, usecols=[0,1])
        persons.to_sql(name='PERSONS', con=_conn, if_exists='replace', index=False)
        print(f'Table PERSONS was successfully created with {len(persons)} rows.')
    except Exception as e:
        print(f'Error: {e}')

def _create_games_table():
    try:
        url = _get_url('games')
        games = pd.read_csv(url)
        games['ID'] = range(1, len(games) + 1)
        games.to_sql(name='GAMES', con=_conn, if_exists='replace', index=False)
        print(f'Table GAMES was successfully created with {len(games)} rows.')
    except Exception as e:
        print(f'Error {e}')

def _create_attendances_table():
    try:
        persons_url = _get_url('persons')
        matches_url = _get_url('matches')
        persons  = pd.read_csv(persons_url, usecols=[0,1])
        matches = pd.read_csv(matches_url)
        # mapping persons names to ids
        name_id_mapping = _get_name_id_mapping('persons', 'NAME', 'ID')
        name_id_mapping.update({'host':'host', 'date':'date', 'game':'game'})
        # game column isn't needed in the attendances_table
        tmp_attendances = matches.drop(columns=['game'])
        tmp_attendances = tmp_attendances[tmp_attendances['host'].notnull()]
        # changing columns to ids
        tmp_attendances.columns = tmp_attendances.columns.map(name_id_mapping)
        # changing host names to ids
        tmp_attendances['host'] = tmp_attendances['host'].map(name_id_mapping)    
        # changing all names in the columns to ids
        for i in range(1, len(persons) + 1):
            # filtering to only when the person attended to a game (not null)
            mask = tmp_attendances[i].notnull()
            tmp_attendances.loc[mask, i] = True
        # creating final table
        attendances = pd.DataFrame(columns = ['DATE', 'IS_HOST', 'PERSON_ID'])
        # looping over persons
        for i in range(1, len(persons) + 1):
            person = pd.DataFrame(columns = ['DATE', 'IS_HOST', 'PERSON_ID'])
            person['DATE'] = tmp_attendances[tmp_attendances[i] == True]['date']
            person['PERSON_ID'] = i
            person['IS_HOST'] = tmp_attendances['host'] == i
            attendances = pd.concat([attendances, person])
        attendances.to_sql(name='ATTENDANCES', con=_conn, if_exists='replace', index=False)
        print(f'Table ATTENDANCES was successfully created with {len(attendances)} rows.')
    except Exception as e:
        print(f'Error: {e}')

def _create_matches_table():
    try:
        url_matches = _get_url('matches')
        url_persons = _get_url('persons')
        matches = pd.read_csv(url_matches)
        persons = pd.read_csv(url_persons)
        final_matches = pd.DataFrame(columns = ['ID', 'DATE', 'PERSON_ID', 'GAME_ID', 'SCORE'])
        # host column isn't needed in matches table 
        matches.drop(columns=['host'], inplace=True)
        # mapping persons names to ids
        name_id_mapping = _get_name_id_mapping('persons', 'NAME', 'ID')
        name_id_mapping.update({'host':'host', 'date':'date', 'game':'game'})  
        matches.columns = matches.columns.map(name_id_mapping)
        # creating ID column
        matches['ID'] = range(1, len(matches) + 1)
        # mapping game names to id
        game_id_mapping = _get_name_id_mapping('games', 'NAME', 'ID_OWNER')
        matches['game'] = matches['game'].map(game_id_mapping)
        # looping over persons
        for i in range(1, len(persons) + 1):
            tmp_matches = matches[matches[i].notnull()]
            person_matches = pd.DataFrame(columns = ['ID', 'DATE', 'PERSON_ID', 'GAME_ID', 'SCORE'])
            person_matches['ID'] = tmp_matches['ID']
            person_matches['DATE'] = tmp_matches['date']
            person_matches['PERSON_ID'] = i
            person_matches['GAME_ID'] = tmp_matches['game']
            person_matches['SCORE'] = tmp_matches[i]
            final_matches = pd.concat([final_matches, person_matches])
        final_matches.to_sql(name='MATCHES', con=_conn, if_exists='replace', index=False)
        print(f'Table MATCHES was successfully created with {len(final_matches)} rows.')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    _create_persons_table()
    _create_games_table()
    _create_attendances_table()
    _create_matches_table()
    

