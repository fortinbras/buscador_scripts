# -*- coding: utf-8 -*-

import sys
from solr_load import SolrLoad

collection = {


    'wos': {
        'filetype': '.xml',
        'collectiondir': '/var/tmp/wos',
        'transformdir': 'transform/',
        'localhost': '192.168.0.212:8983',
        'collection': 'wos',
        'content_type': 'text/xml',
        'schema': '_transform/wos/conf'},

    'enade': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/enade',
        'transformdir': 'transform/',
        'localhost': '192.168.0.212:8983',
        'collection': 'enade',
        'content_type': 'text/csv',
        'schema': '_transform/enade/conf'},

    'inep_alunos': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/inep',
        'transformdir': 'transform/alunos',
        'localhost': '192.168.0.212:8983',
        'collection': 'inep_alunos',
        'content_type': 'text/csv',
        'schema': '_transform/inep_alunos/conf'},

    'inep_docentes': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/inep',
        'transformdir': 'transform/docentes',
        'localhost': '192.168.0.212:8983',
        'collection': 'inep_docentes',
        'content_type': 'text/csv',
        'schema': '_transform/inep_docentes/conf'},

    'pnad': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/pnade',
        'transformdir': 'transform/',
        'localhost': '192.168.0.212:8983',
        'collection': 'pnade',
        'content_type': 'text/csv',
        'schema': '_transform/pnade/conf'},

    'enem': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/enem',
        'transformdir': 'transform/',
        'localhost': '192.168.0.212:8983',
        'collection': 'enem',
        'content_type': 'text/csv',
        'schema': '_transform/enem/conf'},

    'rais': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/rais',
        'transformdir': 'transform/',
        'localhost': '192.168.0.212:8983',
        'collection': 'rais',
        'content_type': 'text/csv',
        'schema': '_transform/rais/conf'},

    'lattes': {
        'filetype': '.xml',
        'collectiondir': '/var/tmp/lattes',
        'transformdir': 'transform/',  # deve estar em /var/tm/lattes/transform
        'localhost': '192.168.0.212:8983',
        'collection': 'lattes',
        'content_type': 'text/xml',
        'schema': '_transform/lattes/conf'},

}


def executa(coll):
    """
    :param coll: argumento para selecionar collection que será executada ex.
     "python load.py wos" para webOfScience

    """
    try:
        param = collection.get(coll)
        load = SolrLoad(
            param['filetype'], param['collectiondir'], param['transformdir'],
            param['localhost'], param['collection'],
            param['content_type'], param['schema']
        )
        load.full_sequence()
    except (TypeError,KeyError):
        print 'collection invalida'
    except KeyboardInterrupt:
        print '\nAtividade interrompida pelo usuario!'


if __name__ == "__main__":
    try:
        executa(sys.argv[1])
    except IndexError:
        print('digite collection como parametro')
