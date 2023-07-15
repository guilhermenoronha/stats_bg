import pandas as pd
import sqlite3
from decouple import config

def get_url(sheet_name):
    sheet_id = config('SHEET_ID')
    return f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'

def create_connection():
    return sqlite3.connect('bg.db')

def createpersons_table(conn):
    try:
        persons  = pd.read_csv(get_url('persons'))
        matches = pd.read_csv(get_url('matches'))
        matches.drop(columns=['game', 'host'], inplace=True)
        # mapping the person name with the last the day he/she attended to a match 
        dict_ = {}
        for i in range(1, len(matches.columns)):
            dict_.update({matches.columns[i] : matches.loc[matches.iloc[:, i].notnull(), 'date'].iloc[-1]})
        persons['LAST_DATE_ATTENDED'] = persons['NAME'].map(dict_)
        persons['DAYS_SINCE_LAST_ATTENDANCE'] = (pd.to_datetime('today') - pd.to_datetime(persons['LAST_DATE_ATTENDED'], format='%d/%m/%y')).dt.days 
        persons.to_sql(name='PERSONS', con=conn, if_exists='replace', index=False)
        print(f'Table PERSONS was successfully created with {len(persons)} rows.')
    except Exception as e:
        print(f'Error creating PERSONS table: {e}')

def create_games_table(conn):
    try:
        games = pd.read_csv(get_url('games'))
        matches = pd.read_csv(get_url('matches'))
        # Create column with the date the game was last played
        matches.drop_duplicates(subset=['game'], keep='last', inplace=True)
        games['LAST_DATE_PLAYED'] = games['NAME'].map(matches.set_index('game')['date'])
        # Created calculated column with the amount of days a game was last played
        games['DAYS_SINCE_LAST_PLAYED'] = (pd.to_datetime('today') - pd.to_datetime(games['LAST_DATE_PLAYED'], format='%d/%m/%y')).dt.days 
        games['ID'] = range(1, len(games) + 1)
        games.to_sql(name='GAMES', con=conn, if_exists='replace', index=False)
        print(f'Table GAMES was successfully created with {len(games)} rows.')
    except Exception as e:
        print(f'Error creating GAMES table: {e}')

def create_attendances_table(conn):
    try:
        persons = pd.read_csv(get_url('persons'))
        matches = pd.read_csv(get_url('matches'))
        matches.drop(columns=['game'], inplace=True)
        # mapping persons names to ids
        name_id_mapping = persons.set_index('NAME')['ID'].to_dict()
        name_id_mapping.update({'host':'host', 'date':'date', 'game':'game'})
        # changing columns to ids
        matches.columns = matches.columns.map(name_id_mapping)
        # changing host names to ids
        matches['host'] = matches['host'].map(name_id_mapping)    
        # changing all names in the columns to ids
        for i in range(1, len(persons) + 1):
            # filtering to only when the person attended to a game (not null)
            mask = matches[i].notnull()
            matches.loc[mask, i] = True
        # creating final table
        attendances = pd.DataFrame(columns = ['DATE', 'IS_HOST', 'PERSON_ID'])
        # looping over persons
        for i in range(1, len(persons) + 1):
            person = pd.DataFrame(columns = ['DATE', 'IS_HOST', 'PERSON_ID'])
            person['DATE'] = matches[matches[i] == True]['date']
            person['PERSON_ID'] = i
            person['IS_HOST'] = matches['host'] == i
            # keeping only the first record each person attended for each date.
            person = person.drop_duplicates(subset=['DATE', 'PERSON_ID'], keep='first')
            attendances = pd.concat([attendances, person])
        attendances.to_sql(name='ATTENDANCES', con=conn, if_exists='replace', index=False)
        print(f'Table ATTENDANCES was successfully created with {len(attendances)} rows.')
    except Exception as e:
        print(f'Error creating ATTENDANCES table: {e}')

def create_matches_table(conn):
    try:
        games = pd.read_csv(get_url('games'))
        games['ID'] = range(1, len(games) + 1)
        persons = pd.read_csv(get_url('persons'))
        matches = pd.read_csv(get_url('matches'))
        # host column isn't needed in matches table 
        matches.drop(columns=['host'], inplace=True)
        # mapping persons names to ids
        name_id_mapping = persons.set_index('NAME')['ID'].to_dict()
        name_id_mapping.update({'host':'host', 'date':'date', 'game':'game'})
        matches.columns = matches.columns.map(name_id_mapping)
        # creating ID column
        matches['ID'] = range(1, len(matches) + 1)
        # mapping game names to id
        game_id_mapping = games.set_index('NAME')['ID'].to_dict()
        matches['game'] = matches['game'].map(game_id_mapping)
        # looping over persons
        final_matches = pd.DataFrame(columns = ['DATE', 'ID', 'PERSON_ID', 'GAME_ID', 'SCORE'])
        for i in range(1, len(persons) + 1):
            tmp_matches = matches[matches[i].notnull()]
            person_matches = pd.DataFrame(columns = ['DATE', 'ID', 'PERSON_ID', 'GAME_ID', 'SCORE'])
            person_matches['ID'] = tmp_matches['ID']
            person_matches['DATE'] = tmp_matches['date']
            person_matches['PERSON_ID'] = i
            person_matches['GAME_ID'] = tmp_matches['game']
            person_matches['SCORE'] = tmp_matches[i]
            final_matches = pd.concat([final_matches, person_matches])
        final_matches.to_sql(name='MATCHES', con=conn, if_exists='replace', index=False)
        print(f'Table MATCHES was successfully created with {len(final_matches)} rows.')
    except Exception as e:
        print(f'Error creating MATCHES table: {e}')

if __name__ == '__main__':
    conn = sqlite3.connect('bg.db')
    createpersons_table(conn)
    create_games_table(conn)
    create_attendances_table(conn)
    create_matches_table(conn)