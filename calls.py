# -*- coding: utf-8 -*-

import sys
from solr_load import solrLoad

collection = {
    'wos': {
        'filetype': '.xml',
        'directory_transform': '/var/tmp/wos/transform/',
        'localhost': '192.168.0.212:8983',
        'collection': 'wos',
        'content_type': 'text/xml'},

    'lattes': {
        'filetype': '.xml',
        'directory_transform': '/var/tmp/lattes/',
        'localhost': '192.168.0.212:8983',
        'collection': 'lattes',
        'content_type': 'text/xml'},

    'enade': {
        'filetype': '.csv',
        'directory_transform': '/var/tmp/enade/',
        'localhost': '192.168.0.212:8983',
        'collection': 'enade',
        'content_type': 'text/csv'},

    'inep': {
        'filetype': '.csv',
        'directory_transform': '/var/tmp/inep/',
        'localhost': '192.168.0.212:8983',
        'collection': 'inep',
        'content_type': 'text/csv'},

}


def executa(coll):
    """
    :param coll: argumento para selecionar collection que será executada ex. "python calls.py wos" para webOfScience

    """

    if coll == 'wos':

        param = collection['wos']
        solr_request = solrLoad(
            param['directory_transform'], param['filetype'], param['localhost'],
            param['collection'], param['content_type']
        )
        solr_request.delete_collection()  # deleta collection do solr
        solr_request.files_load()  # carrega no server

    elif coll == 'enade':

        param = collection['enade']

        solr_request = solrLoad(
            param['directory_transform'], param['filetype'], param['localhost'],
            param['collection'], param['content_type']
        )
        solr_request.delete_collection()  # deleta collection do solr
        solr_request.files_load()  # carrega no server

    elif coll == 'lattes':

        param = collection['lattes']
        solr_request = solrLoad(
            param['directory_transform'], param['filetype'], param['localhost'],
            param['collection'], param['content_type']
        )
        solr_request.delete_collection()  # deleta collection do solr
        solr_request.files_load()  # carrega no server

    elif coll == 'inep':

        param = collection['inep']
        solr_request = solrLoad(
            param['directory_transform'], param['filetype'], param['localhost'],
            param['collection'], param['content_type']
        )
        solr_request.delete_collection()  # deleta collection do solr
        solr_request.list_files()  # carrega no server
    else:
        print('digite collection como parametro')


if __name__ == "__main__":
    try:
        executa(sys.argv[1])
    except IndexError:
        print('digite collection como parametro')


# import relativo