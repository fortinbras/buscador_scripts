# -*- coding: utf-8 -*-

import sys
from solr_load import SolrLoad
from settings import BASE_PATH_DATA
from settings import SOLR_URL, SOLR_PORT

collection = {

    'wos': {
        'filetype': '.xml',
        'collectiondir': BASE_PATH_DATA + 'wos',
        'transformdir': 'transform/',
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
        'collection': 'wos',
        'content_type': 'text/xml',
        'schema': '_transform/wos/conf'},

    'enade': {
        'filetype': '.csv',
        'collectiondir': BASE_PATH_DATA + 'enade',
        'transformdir': 'transform/',
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
        'collection': 'enade',
        'content_type': 'text/csv',
        'schema': '_transform/enade/conf'},

    'inep_alunos': {
        'filetype': '.csv',
        'collectiondir': BASE_PATH_DATA + 'inep',
        'transformdir': 'transform/alunos',
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
        'collection': 'inep_alunos',
        'content_type': 'text/csv',
        'schema': '_transform/inep_alunos/conf'},

    'inep_docentes': {
        'filetype': '.csv',
        'collectiondir': BASE_PATH_DATA + 'inep',
        'transformdir': 'transform/docentes',
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
        'collection': 'inep_docentes',
        'content_type': 'text/csv',
        'schema': '_transform/inep_docentes/conf'},

    'pnad': {
        'filetype': '.csv',
        'collectiondir': BASE_PATH_DATA + 'pnade',
        'transformdir': 'transform/',
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
        'collection': 'pnade',
        'content_type': 'text/csv',
        'schema': '_transform/pnade/conf'},

    'enem': {
        'filetype': '.csv',
        'collectiondir': BASE_PATH_DATA + 'enem',
        'transformdir': 'transform/',
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
        'collection': 'enem',
        'content_type': 'text/csv',
        'schema': '_transform/enem/conf'},

    'rais': {
        'filetype': '.csv',
        'collectiondir': BASE_PATH_DATA + 'rais',
        'transformdir': 'transform/',
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
        'collection': 'rais',
        'content_type': 'text/csv',
        'schema': '_transform/rais/conf'},

<<<<<<< HEAD
=======
    'rais_estabelecimentos': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/solr_front/collections/rais_estabelecimentos',
        'transformdir': 'transform/',
        'localhost': '192.168.0.212:8983',
        'collection': 'rais_estabelecimentos',
        'content_type': 'text/csv',
        'schema': '_transform/rais_estabelecimentos/conf'},

>>>>>>> carlos
    'capes_discentes': {
        'filetype': '.csv',
        'collectiondir': BASE_PATH_DATA + 'capes/discentes',
        'transformdir': 'transform/',
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
        'collection': 'capes_discentes',
        'content_type': 'text/csv',
        'schema': '_transform/capes_discentes/conf'},

    'capes_docentes': {
        'filetype': '.csv',
        'collectiondir': BASE_PATH_DATA + 'capes/docentes',
        'transformdir': 'transform/',
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
        'collection': 'capes_docentes',
        'content_type': 'text/csv',
        'schema': '_transform/capes_docentes/conf'},

<<<<<<< HEAD
    'capes_teses': {
        'filetype': '.csv',
        'collectiondir': BASE_PATH_DATA + 'capes_teses',
        'transformdir': 'transform/',
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
        'collection': 'capes_teses',
        'content_type': 'text/csv',
        'schema': '_transform/capes_teses/conf'},
=======
    'capes_programas': {
        'filetype': '.csv',
        'collectiondir': '/var/tmp/solr_front/collections/capes/programas',
        'transformdir': 'transform/',
        'localhost': '192.168.0.212:8983',
        'collection': 'capes_programas',
        'content_type': 'text/csv',
        'schema': '_transform/capes_programas/conf'},
>>>>>>> carlos

    'lattes': {
        'filetype': '.xml',
        'collectiondir': BASE_PATH_DATA + 'lattes',
        'transformdir': 'transform/',  # deve estar em /var/tm/lattes/transform
        'localhost': SOLR_URL,
        'port': SOLR_PORT,
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
            filetype=param['filetype'],
            collectiondir=param['collectiondir'],
            transformdir=param['transformdir'],
            localhost=param['localhost'],
            port=param['port'],
            collection=param['collection'],
            content_type=param['content_type'],
            schemadir=param['schema']
        )

        load.full_sequence()

    except (TypeError, KeyError):
        print 'collection invalida'
    except KeyboardInterrupt:
        print '\nAtividade interrompida pelo usuario!'


if __name__ == "__main__":
    try:
        executa(sys.argv[1])
    except IndexError:
        print('digite collection como parametro')
