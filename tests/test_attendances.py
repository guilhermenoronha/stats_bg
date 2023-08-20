from packages import attendances as att
import pandas as pd

def test_get_player_attendances():
    player = ('Art Vandeley', 1)
    df = pd.DataFrame(data={'date': ['01/01/23', '01/01/23', '02/01/23'],
                            'host': ['Art Vandeley', 'Bob Sacamano', 'Newman'],
                            'Art Vandeley': [10, 150, 1]
        })
    attendances = att._get_player_attendances(df, player)
    assert len(attendances) == 2
    assert attendances['DATE'].to_list() == ['01/01/23', '02/01/23']
    assert len(attendances['PLAYER_ID'].drop_duplicates()) == 1
    assert len(attendances[attendances['IS_HOST'] == True]) == 1