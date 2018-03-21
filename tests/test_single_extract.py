import insightepy
from insightepy import conf
from tests import resources as rs


def test_on_get():
    api = insightepy.API(
        conf.config.get('test', 'client_id'),
        conf.config.get('test', 'client_secret'),
        conf.config.get('test', 'auth_token'),
    )
    for doc in rs.corpus:
        res = api.single_extract(
            verbatim=doc['text'].decode('utf-8'),
            lang=doc['lang']
        )
        assert res['status'] == 'success'
