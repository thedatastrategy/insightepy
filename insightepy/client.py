# -*- coding: utf-8 -*-
import codecs
import json
import os
import requests
import sys
import time
import tarfile
import traceback
from urllib3 import HTTPConnectionPool

from insightepy import conf

HOST_ADDR = conf.config.get('server', 'host')
HOST_PORT = conf.config.get('server', 'port')
ROUTE_PREFIX = conf.config.get('server', 'route_prefix')


class API(object):
    def __init__(self, clientid, clientsecret, authtoken):
        self._cid = clientid
        self._csecret = clientsecret
        self._authtoken = authtoken
        self.pool = HTTPConnectionPool(HOST_ADDR + ':' + HOST_PORT)

    def make_request(self, method, url, fields):
        # adding user information to field

        fields['cid'] = self._cid
        fields['csecret'] = self._csecret
        fields['authtoken'] = self._authtoken
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
        # TODO enable NER
        # :param ifNER: if extract named entities
        ifNER = False

        if not isinstance(verbatim, unicode):
            raise Exception("Verbatim not of type Unicode")

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

    #
    # Temporarily Deprecated
    #  |
    #  V
    def post_file(self, url, fields):
        urlfull = 'http://' + HOST_ADDR + ':' + HOST_PORT + ROUTE_PREFIX + url
        r = requests.post(ROUTE_PREFIX + urlfull, files=fields)
        try:
            return json.loads(r.content)
        except:
            return r.content

    def _post_verbatim_file(self, filepath):
        # check if exist file
        if not os.path.exists(filepath):
            raise Exception("File not found : " + filepath)
        try:
            # post file
            _file = codecs.open(filepath, mode='rb', encoding='utf-8')
            filedata = {'file': (_file.name, open(filepath, 'rb'))}
            return self.post_file('/batch/extract', filedata)
        except:
            e = sys.exc_info()[0]
            print ("ERROR %s", e)
            traceback.print_exc(file=sys.stdout)
            raise Exception("Encoding Error : File was not found to be utf8 encoded")

    def __batch_extract(
            self,
            filepath, lang, dest_dir,
            ifterm=True, ifkeyword=True, ifconcept=False,
            ifpos=True, ifemotion=True, ifsentiment=True, ifNER=True,
            ifHashTags=True, ifMentions=True, ifUrl=True
    ):
        """
        Post verbatim file
        Make batch extraction request
        Wait for success
        """
        # TODO make batch extract work
        r = self._post_verbatim_file(filepath)
        if r['s'] and 'filename' in r:
            # make schedule request
            r1 = self.make_request('GET', '/batch/extract', {
                'action': 'schedule',
                'file': filepath,
                'filepath': r['filename'],
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
            if r1['s']:
                ifdone = False
                r2 = None
                while not ifdone:
                    r2 = self.make_request('GET', '/batch/extract', {
                        'action': 'check_if_done',
                        'file': filepath,
                        'filepath': r['filename'],
                    })
                    if r2['s']:
                        ifdone = True
                    else:
                        time.sleep(5)

                _dir_curr = os.getcwd() + '/'
                dir_new = r2['compressed_file'].replace('.tar', '') + '/'
                compressed_file = r2['compressed_file']

                if not os.path.exists(dest_dir):
                    os.mkdir(dest_dir)
                if not os.path.exists(dest_dir + dir_new):
                    os.mkdir(dest_dir + dir_new)

                # download compressed file
                tmp_compressed_file_path = self._get_resource('compressed_file', compressed_file, dest_dir)

                # move compressed file into new directory
                os.rename(tmp_compressed_file_path, dest_dir + dir_new + compressed_file)
                os.chdir(dest_dir + dir_new)

                # extract tar
                tar = tarfile.open(compressed_file)
                tar.extractall()

                # remove tar
                os.remove(compressed_file)
                os.chdir(_dir_curr)

                # build response
                return {'s': True, 'results_location': dest_dir + dir_new}
        else:
            return r

    def _get_resource(self, _type, name, dest_dir):
        url = '/resources/get/' + _type + '/' + name
        r = self.make_request('GET', url, {})
        with open(dest_dir + name, 'w') as new_file:
            new_file.write(r)
        new_file.close()

        # return filename
        return dest_dir + name
