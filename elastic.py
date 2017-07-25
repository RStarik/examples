#!/usr/bin/env python

from __future__ import print_function
from pprint import pprint
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import argparse
import elasticsearch
import datetime


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--url', "-u", help='Elasticsearch URL for output data in format [http|https]://domain:port',
                        type=str)
script_args = arg_parser.parse_args()

ES_SCHEME_DEFAULT = 'http'
ES_PORT_DEFAULT = 9200
ES_HOST_DEFAULT = '127.0.0.1'
# We suppose that Elasticsearch is a local instance
ES_URL_DEFAULT = '{scheme}://{host}:{port}'.format(scheme=ES_SCHEME_DEFAULT, host=ES_HOST_DEFAULT, port=ES_PORT_DEFAULT)
ES_TYPE = 'es_test_type'
ES_MSG = {'@timestamp': datetime.datetime.utcnow(),  # Elasticsearch datetime API convention
          'message': 'Hello World!',
          'test_int_attr': 1,
          'test_float_attr': 3.14,
          'test_string_attr': 'string attribute',
          'test_list': [1, 2, 3, 4, 5, 1.1],
          'test_dict': {'key_1': 1, 'key_2': 2.2, 'key_3': 'string'}}

if script_args.url is None:
    es_url = ES_URL_DEFAULT
else:
    url_parser = urlparse(script_args.url)
    es_url = script_args.url
    if url_parser.hostname is None:
        raise ValueError('Wrong URL {url}'.format(url=es_url))
    if url_parser.port is None:
        es_url = '{url}:{port}'.format(url=es_url, port=ES_PORT_DEFAULT)

print('Elasticsearch: {0}'.format(es_url))

es = elasticsearch.Elasticsearch([es_url])
query = es.index(index='logstash-{date}'.format(date=datetime.datetime.utcnow().strftime('%Y.%m.%d')),
                  doc_type=ES_TYPE,
                  body=ES_MSG)
if query.get('result', None)is not None and query.get('created', None) is not None:
    pprint(query)
else:
    print('ERROR. Elasticsearch answer: {0}'.format(query))
