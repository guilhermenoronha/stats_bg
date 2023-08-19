import scrapper.boardgamegeek_scrapper as bgg

def test_get_BGG_url_by_Ludopedia_search():
    search = 'terra-mystica'
    url = bgg.get_BGG_url_by_Ludopedia_search(search)
    assert url == 'https://boardgamegeek.com/boardgame/120677/terra-mystica'

def test_get_BGG_game_weight():
    url = 'https://boardgamegeek.com/boardgame/13/catan'
    weight = bgg.get_BGG_game_weight(url)
    assert 2 <= weight <= 2.5

def test_get_BGG_min_max_best_players():
    url = 'https://boardgamegeek.com/boardgame/13/catan'
    min, max = bgg.get_BGG_min_max_best_players(url)
    assert 3 <= int(min) <= 4
    assert 3 <= int(max) <= 4