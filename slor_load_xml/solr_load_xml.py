# -*- coding: utf-8 -*-

import urllib2
import os


class Solr_load_xml():

    """
    Classe realiza um POST pra uma determinada url no solr com uma lista de arquivos da maquina local
    os parametros :
    directory - Path para a pasta local ex.'c:/root/folder'
    filetype - extensão do arquivo em formato de string ex. '.xml'
    localhost - dominio do servidor ex. 'localhost:8983'
    server_folder - pasta no servidor que os arquivos serão enviados ex.'lattes'
    Content_type - adiciona o tipo do conteudo no cabecalho ex 'text/xml'

    """

    def __init__(self, directory, filetype, localhost, server_folder, content_type):

        self.directory = directory
        self.filetype = filetype
        self.localhost = localhost
        self.server_folder = server_folder
        self.content_type = content_type

    def list_files(self):
        self.asps = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(self.filetype):
                    self.asps.append(file)
        return self.asps

    def files_load(self):

        filelist = self.list_files()
        for file in filelist:
            with open(file, 'rb') as data_file:
                my_data = data_file.read()
            req = urllib2.Request(
                url='http://' + self.localhost + '/solr/' + self.server_folder + '/update?commit=true',
                data=my_data)
            req.add_header('Content-type', self.content_type)
            f = urllib2.urlopen(req)
            print f.read()

# 'http://localhost:8983/solr/lattes/update?commit=true'
