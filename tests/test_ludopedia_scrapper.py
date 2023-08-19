from scrapper.ludopedia_scrapper import LudopediaScrapper

def test_get_user_id():
    username = 'Kamusett'
    ls = LudopediaScrapper()
    id = ls.get_user_id(username)
    assert id == 5724

def test_get_user_collection():
    id = '5724'
    ls = LudopediaScrapper()
    collection = ls.get_user_collection(id)
    assert len(collection) > 0
    assert [g['nm_jogo'] for g in collection].index('Terra Mystica') >= 0

def test_get_bg_metadata():
    game_id = '8917'
    ls = LudopediaScrapper()
    metadata = ls.get_bg_metadata(game_id)
    assert metadata['id_jogo'] == int(game_id)

def test_get_game_by_name():
    name = 'Terra Mystica'
    ls = LudopediaScrapper()
    game = ls.get_game_by_name(name)
    assert game['nm_jogo'] == name

def test_get_ludopedia_taxonomy():
    themes = 'https://ludopedia.com.br/temas'
    categories = 'https://ludopedia.com.br/categorias'
    domains = 'https://ludopedia.com.br/dominios'
    mechanics = 'https://ludopedia.com.br/mecanicas'
    ls = LudopediaScrapper()
    taxonomy = ls.get_ludopedia_taxonomy(themes)
    assert [t['URL'] for t in taxonomy].index('https://ludopedia.com.br/tema/1') >= 0
    taxonomy = ls.get_ludopedia_taxonomy(categories)
    assert [t['URL'] for t in taxonomy].index('https://ludopedia.com.br/categoria/1') >= 0
    taxonomy = ls.get_ludopedia_taxonomy(domains)
    assert [t['URL'] for t in taxonomy].index('https://ludopedia.com.br/dominio/9') >= 0
    taxonomy = ls.get_ludopedia_taxonomy(mechanics)
    assert [t['URL'] for t in taxonomy].index('https://ludopedia.com.br/mecanica/1') >= 0

def test_get_game_domain():
    url = 'https://ludopedia.com.br/jogo/terra-mystica'
    ls = LudopediaScrapper()
    domain = ls.get_game_domain(url)
    assert domain == '9'