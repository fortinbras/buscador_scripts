# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, '../../../buscador_scripts/')
import requests
import os


class SolrLoad(object):
    """
    Classe realiza um POST pra uma determinada url no solr com uma lista de arquivos da maquina local
    os parametros :
    directory - Path para a pasta local ex.'c:/root/folder'
    filetype - extensão do arquivo em formato de string ex. '.xml'
    localhost - dominio do servidor ex. 'localhost:8983'
    collection - pasta no servidor que os arquivos serão enviados ex.'lattes'
    Content_type - adiciona o tipo do conteudo no cabecalho ex 'text/xml'

    """

    def __init__(self, filetype, collectiondir, transformdir, localhost, collection, content_type, schemadir):
        self.fileslist = []
        self.filetype = filetype
        self.collectiondir = collectiondir
        self.transformdir = transformdir
        self.localhost = localhost
        self.collection = collection
        self.content_type = content_type
        self.schemadir = schemadir

    def list_output_files(self):
        if self.collection == 'wos':
            for root, dirs, files in os.walk(self.collectiondir):
                for f in files:
                    if (f.endswith(self.filetype)) and ('transform' in root):
                        self.fileslist.append(os.path.join(root, f))
            print '%s arquivos encontrado' % len(self.fileslist)
            return self.fileslist
        else:
            try:
                anos = os.listdir(self.collectiondir)
                anos.sort()
            except OSError:
                print('Nenhuma pasta encontrada')
                raise
            for ano in anos:
                var = self.collectiondir + '/' + ano + '/' + self.transformdir
                for root, dirs, files in os.walk(var):
                    for f in files:
                        if f.endswith(self.filetype):
                            self.fileslist.append(os.path.join(root, f))
            print '%s arquivos encontrado' % len(self.fileslist)
            return self.fileslist

    def files_load(self):
        for f in self.list_output_files():
            print('Uploading file {}'.format(f))
            with open(f, 'rb') as data_file:
                my_data = data_file.read()
            if self.filetype == '.csv':
                url = 'http://' + self.localhost + '/solr/' + self.collection + '/update?commit=true&separator=;'
            else:
                url = 'http://' + self.localhost + '/solr/' + self.collection + '/update?commit=true'

            try:
                req = requests.post(
                    url,
                    data=my_data, headers={"Content-Type": self.content_type}
                )
                print req.status_code
                # print req.headers['status']

            except requests.ConnectionError as errc:
                print ("Error Connecting:", errc)
            except requests.HTTPError as errh:
                print ("Http Error:", errh)
            except requests.Timeout as errt:
                print ("Timeout Error:", errt)
            except requests.RequestException as err:
                print ("OOps: Something Else", err)

                # 'http://localhost:8983/solr/lattes/update?commit=true'

    def delete_collection(self):
        url = 'http://192.168.0.212/solr/' + \
              self.collection + \
              '/update?commit=true&stream.body=<delete><query>*:*</query></delete>'
        try:
            req = requests.post(url)
            print req.status_code
            # print req.headers['status']

        except requests.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.HTTPError as errh:
            print ("Http Error:", errh)
        except requests.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.RequestException as err:
            print ("OOps: Something Else", err)

    def reload_collection(self):
        url = 'http://192.168.0.212/solr/' + \
              self.collection + \
              '/update?commit=true&stream.body=<delete><query>*:*</query></delete>'
        try:
            req = requests.post(url)
            print req.status_code
            # print req.headers['status']

        except requests.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.HTTPError as errh:
            print ("Http Error:", errh)
        except requests.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.RequestException as err:
            print ("OOps: Something Else", err)

    def upload_schema(self):
        command = 'opt/solr-6.6.2/bin/solr zk -upconfig -n ' + self.collection + ' -z localhost:9983 -d ' +\
                  self.schemadir
        os.system(command)

    def full_sequence(self):
        print('Deleting collection')
        self.delete_collection()

        print('Upload do schema')
        self.upload_schema()

        print('Collection refresh')
        self.reload_collection()

        print('Collection upload')
        self.files_load()

# http://192.168.0.212/solr/< COLLECTION >/update?commit=true&stream.body=<delete><query>*:*</query></delete>

# HTTPERROR

# checar responses

# /opt/solr-6.6.2/bin/solr zk -upconfig -n enade  -z localhost:9983 -d <dir onde se encontra o managed-schema>

# http://192.168.0.212/solr/admin/collectionsaction=RELOAD&name=enade&wt=json
