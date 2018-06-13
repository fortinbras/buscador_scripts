# -*- coding: utf-8 -*-

import sys
from transform.wos import BibtoXML
from solr_load import Solr_load_xml
from transform.enade import generate_csv

collection = {
    'wos': ['/var/tmp/bibtex/', '.xml', '/xml_out/', '192.168.0.212:8983', 'wos', 'text/xml'],
    'lattes':['/var/tmp/lattes/','.xml','/var/tmp/lattes/','192.168.0.212:8983','lattes', 'text/xml']

}


def executa(coll):
    """
    :param coll: argumento para selecionar collection que será executada ex. "python calls.py wos" para webOfScience

    """

    if coll == 'wos':
        param = collection['wos']
        bibxml = BibtoXML(param[0])
        bibxml.parse_bib()  # gera XML
        # #######################################
        solrload = Solr_load_xml(param[2], param[1], param[3], param[4], param[5])
        solrload.files_load()  # carrega no server
    elif coll == 'enade2016':
        generate_csv('/home/giuseppe/dados/ENADE_2016.txt','ENADE_2016.CSV')
    elif coll=='lattes':
        param = collection['lattes']

        solrload = Solr_load_xml(param[2], param[1], param[3], param[4], param[5])
        solrload.files_load()
    else:
        print('digite collection como parametro')





if __name__ == "__main__":
    try:
        executa(sys.argv[1])
    except IndexError:
        print('digite collection como parametro')

# /var/tmp/bibtex/

# Dicionarios
#antes de enviar, deletar contuedo do solr  (função de deletar) email robson



#manipular os .rar que os arquivos inep geram

# um modulo de donw e outro de trans

# tratamento de erros no download

#gerar classes para transformação por ano

#download var/tmp/collection/download

# saida  var/tmp/collection/transform



