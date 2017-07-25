#!/usr/bin/env python

from __future__ import print_function
import elasticsearch
import datetime


ES_SCHEMA = 'http'
# for docker images from elastic.co with X-PACK and HTTP basic auth
# ES_AUTH = {'username': 'elastic', 'password': 'changeme'}
ES_AUTH = None
ES_HOST = '127.0.0.1'
ES_PORT = '9200'

if ES_AUTH is dict() and ES_AUTH.get('username', None) is not None and ES_AUTH.get('password', None) is not None:
    ES_URL = '{schema}://{user}:{password}@{host}:{port}'.format(schema=ES_SCHEMA, user=ES_AUTH['username'],
                                                                 password=ES_AUTH['password'], host=ES_HOST,
                                                                 port=ES_PORT)
else:
    ES_URL = '{schema}://{host}:{port}'.format(schema=ES_SCHEMA, host=ES_HOST, port=ES_PORT)

ES_TYPE = 'es_test_type'
ES_MSG = {'@timestamp': datetime.datetime.utcnow(),
          'message': 'Hello World!',
          'test_int_attr': 1,
          'test_float_attr': 3.14,
          'test_string_attr': 'string attribute',
          'test_list': [1, 2, 3, 4, 5, 1.1],
          'test_dict': {'key_1': 1, 'key_2': 2.2, 'key_3': 'string'}}

es = elasticsearch.Elasticsearch([ES_URL])
result = es.index(index='logstash-{date}'.format(date=datetime.datetime.utcnow().strftime('%Y.%m.%d')),
                  doc_type=ES_TYPE,
                  body=ES_MSG)
from pprint import pprint
pprint(ES_URL)
pprint(ES_MSG)
pprint(result)
