# -*- coding: utf-8 -*-

import sys
from solr_load import solrLoad

collection = {
    'wos': {
        'filetype': '.xml',
        'localhost': '192.168.0.212:8983',
        'collection': 'wos',
        'content_type': 'text/xml',
        'collectiondir': '/var/tmp/wos',
        'transformdir': 'transform/wos'
    },

    'lattes': {
        'filetype': '.xml',
        'localhost': '192.168.0.212:8983',
        'collection': 'lattes',
        'content_type': 'text/xml',
        'collectiondir': '/var/tmp/lattes',
        'transformdir': 'transform/'},

    'enade': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/enade',
        'transformdir': 'transform/',
        'localhost': '192.168.0.212:8983',
        'collection': 'enade',
        'content_type': 'text/csv',
        'schema': 'transform/enade/'},

    'inep_alunos': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/inep',
        'transformdir': 'transform/alunos',
        'localhost': '192.168.0.212:8983',
        'collection': 'inep_alunos',
        'content_type': 'text/csv',
        'schema': 'transform/inep_alunos/'},

    'inep_docentes': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/inep',
        'transformdir': 'transform/docentes',
        'localhost': '192.168.0.212:8983',
        'collection': 'inep_docentes',
        'content_type': 'text/csv',
        'schema': 'transform/inep_docentes/'},

}


def executa(coll):
    """
    :param coll: argumento para selecionar collection que será executada ex. "python calls.py wos" para webOfScience

    """

    if coll == 'inep_alunos':
        param = collection['inep_alunos']
        load = solrLoad(param['filetype'], param['collectiondir'], param['transformdir'], param['content_type'],
                        param['schema'])
        load.full_sequence()

    elif coll == 'inep_docentes':
        param = collection['inep_docentes']
        load = solrLoad(param['filetype'], param['collectiondir'], param['transformdir'], param['localhost'],
                        param['collection'], param['content_type'], param['schema'])
        load.full_sequence()

    elif coll == 'enade':
        param = collection['enade']
        load = solrLoad(param['filetype'], param['collectiondir'], param['transformdir'], param['localhost'],
                        param['collection'], param['content_type'], param['schema'])
        load.full_sequence()


    elif coll == 'wos':
        param = collection['wos']
        load = solrLoad(param['filetype'], param['collectiondir'], param['transformdir'], param['localhost'],
                        param['collection'], param['content_type'], param['schema'])
        # load.list_output_files()
        load.full_sequence()


if __name__ == "__main__":
    try:
        executa(sys.argv[1])
    except IndexError:
        print('digite collection como parametro')

# import relativo
