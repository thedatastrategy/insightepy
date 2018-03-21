# -*- coding: utf-8 -*-
import json

from urllib3 import HTTPConnectionPool

from insightepy import conf
from insightepy.core import Logger

HOST_ADDR = conf.config.get('server', 'host')
HOST_PORT = conf.config.get('server', 'port')
ROUTE_PREFIX = conf.config.get('server', 'route_prefix')

logger = Logger('InsightePy')


class API(object):
    def __init__(self, client_id, client_secret, auth_token):
        logger.info('Hello from InsightePy')
        self._cid = client_id
        self._csecret = client_secret
        self._auth_token = auth_token
        self.pool = HTTPConnectionPool(HOST_ADDR + ':' + HOST_PORT, timeout=2)

    def make_request(self, method, url, fields):
        # adding user information to field
        fields['cid'] = self._cid
        fields['csecret'] = self._csecret
        fields['authtoken'] = self._auth_token
        logger.debug('Making request with: {}'.format(fields))
        r = self.pool.request(method, ROUTE_PREFIX + url, fields=fields)
        try:
            return json.loads(r.data)
        except:
            return r.data

    def single_extract(
            self,
            verbatim, lang,
            ifterm=True, ifkeyword=True, ifconcept=True,
            ifpos=True, ifemotion=True, ifsentiment=True,
            ifHashTags=True, ifMentions=True, ifUrl=True
            # ifNER=False,
    ):
        """
        Extract insight for a single verbatim
        :param verbatim: Unicode sentence
        :param lang: language of the sentence {en/fr/de}
        :param ifterm: if extract terms
        :param ifkeyword: if extract keywords
        :param ifconcept: if extract concepts 
        :param ifpos: if extract part of speech tags
        :param ifemotion: if extract emotions
        :param ifsentiment: if extract sentiments
        :param ifHashTags: if extract hashtags
        :param ifMentions: if extract mentions
        :param ifUrl: if extract urls
        :return: dict
        """
        logger.info('Running Single Extract on: {}'.format(verbatim))

        # TODO enable NER
        # :param ifNER: if extract named entities
        ifNER = False

        return self.make_request('GET', '/extract', {
            'verbatim': verbatim,
            'lang': lang,
            'ifterm': ifterm,
            'ifkeyword': ifkeyword,
            'ifconcept': ifconcept,
            'ifpos': ifpos,
            'ifemotion': ifemotion,
            'ifsentiment': ifsentiment,
            'ifner': ifNER,
            'ifhashtags': ifHashTags,
            'ifmention': ifMentions,
            'ifurl': ifUrl,
        })

    def _get_resource(self, _type, name, dest_dir):
        url = '/resources/get/' + _type + '/' + name
        r = self.make_request('GET', url, {})
        with open(dest_dir + name, 'w') as new_file:
            new_file.write(r)
        new_file.close()

        # return filename
        return dest_dir + name
