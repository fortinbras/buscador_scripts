# -*- coding: utf-8 -*-

import urllib2
import os


class solrLoad():
    """
    Classe realiza um POST pra uma determinada url no solr com uma lista de arquivos da maquina local
    os parametros :
    directory - Path para a pasta local ex.'c:/root/folder'
    filetype - extensão do arquivo em formato de string ex. '.xml'
    localhost - dominio do servidor ex. 'localhost:8983'
    collection - pasta no servidor que os arquivos serão enviados ex.'lattes'
    Content_type - adiciona o tipo do conteudo no cabecalho ex 'text/xml'

    """

    def __init__(self, directory, filetype, localhost, collection, content_type):

        self.directory = directory
        self.filetype = filetype
        self.localhost = localhost
        self.collection = collection
        self.content_type = content_type

    def list_files(self):
        self.asps = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith(self.filetype):
                    print(file)
                    self.asps.append(os.path.join(root, file))
        print(len(self.asps))
        return self.asps

    def files_load(self):

        filelist = self.list_files()
        for file in filelist:
            with open(file, 'rb') as data_file:
                my_data = data_file.read()
            if self.filetype == '.csv':
                req = urllib2.Request(
                    url='http://' + self.localhost + '/solr/' + self.collection + '/update?commit=true&separator=;',
                    data=my_data)
            else:
                req = urllib2.Request(
                    url='http://' + self.localhost + '/solr/' + self.collection + '/update?commit=true',
                    data=my_data)
            req.add_header('Content-type', self.content_type)
            print 'conectando ...'
            f = urllib2.urlopen(req)
            print f.read()

    def delete_collection(self):
        req = urllib2.Request(
            url='http://192.168.0.212/solr/' + self.collection + '/update?commit=true&stream.body=<delete><query>*:*</query></delete>')
        f = urllib2.urlopen(req)
        print(f)

# 'http://localhost:8983/solr/lattes/update?commit=true'

# http://192.168.0.212/solr/< COLLECTION >/update?commit=true&stream.body=<delete><query>*:*</query></delete>