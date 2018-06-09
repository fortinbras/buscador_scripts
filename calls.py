# -*- coding: utf-8 -*-

from slor_load_xml import Solr_load_xml
from Transform import BibtoXML
from Transform.enade import generate_csv


collections = {
    'wos': {
        'transform_function': BibtoXML('wos_data/'),
        'load_function': Solr_load_xml('xml_out/', '.xml', '192.168.0.212:8983', 'wos', 'text/xml')
    },

    'enad2016': {
        'transform_function': generate_csv('enade2016_data/ENADE_2016.txt', 'enade2016_out.csv',
                                           'Transform/enade/lista_municipios.csv')

    },

}


def transform(col):
    param = collections[col]
    param['transform_function']


def load_solr(col):
    param = collections[col]
    param['load_function']


transform_list = [
    # 'wos',
    'enad2016',
]
load_list = [
    # 'wos',
]

if __name__ == "__main__":

    for col in transform_list:
        transform(col)
    for col in load_list:
        load_solr(col)

# /var/tmp/bibtex/
