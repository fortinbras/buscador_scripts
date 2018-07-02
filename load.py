# -*- coding: utf-8 -*-

import sys
from solr_load import SolrLoad

collection = {
    'wos': {
        'filetype': '.xml',
        'localhost': '192.168.0.212:8983',
        'collection': 'wos',
        'content_type': 'text/xml',
        'collectiondir': '/var/tmp/wos',
        'transformdir': '_transform/wos'
    },

    'enade': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/enade',
        'transformdir': '_transform/',
        'localhost': '192.168.0.212:8983',
        'collection': 'enade',
        'content_type': 'text/csv',
        'schema': '_transform/enade/conf'},

    'inep_alunos': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/inep',
        'transformdir': '_transform/alunos',
        'localhost': '192.168.0.212:8983',
        'collection': 'inep_alunos',
        'content_type': 'text/csv',
        'schema': '_transform/inep_alunos/conf'},

    'inep_docentes': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/inep',
        'transformdir': '_transform/docentes',
        'localhost': '192.168.0.212:8983',
        'collection': 'inep_docentes',
        'content_type': 'text/csv',
        'schema': '_transform/inep_docentes/conf'},

    'lattes': {
        'filetype': '.xml',
        'collectiondir': '/var/tmp/lattes',
        'transformdir': '_transform/',  #deve estar em /var/tm/lattes/_transform/
        'localhost': '192.168.0.212:8983',
        'collection': 'lattes',
        'content_type': 'text/xml',
        'schema': '_transform/lattes/conf'},

}


def executa(coll):
    """
    :param coll: argumento para selecionar collection que será executada ex. "python load.py wos" para webOfScience

    """

    if coll == 'inep_alunos':
        param = collection['inep_alunos']
        load = SolrLoad(param['filetype'], param['collectiondir'], param['transformdir'], param['localhost'],
                        param['collection'], param['content_type'], param['schema'])
        load.full_sequence()

    elif coll == 'inep_docentes':
        param = collection['inep_docentes']
        load = SolrLoad(param['filetype'], param['collectiondir'], param['transformdir'], param['localhost'],
                        param['collection'], param['content_type'], param['schema'])
        load.full_sequence()

    elif coll == 'enade':
        param = collection['enade']
        load = SolrLoad(param['filetype'], param['collectiondir'], param['transformdir'], param['localhost'],
                        param['collection'], param['content_type'], param['schema'])
        load.full_sequence()

    elif coll == 'wos':
        param = collection['wos']
        load = SolrLoad(param['filetype'], param['collectiondir'], param['transformdir'], param['localhost'],
                        param['collection'], param['content_type'], param['schema'])
        load.full_sequence()

    elif coll == 'lattes':
        param = collection['lattes']
        print('Os arquivos lattes devem estar em /var/tm/lattes/_transform/ ')
        load = SolrLoad(param['filetype'], param['collectiondir'], param['transformdir'], param['localhost'],
                        param['collection'], param['content_type'], param['schema'])
        load.full_sequence()


if __name__ == "__main__":
    try:
        executa(sys.argv[1])
    except IndexError:
        print('digite collection como parametro')

