# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, '../../../buscador_scripts/')
import requests
import os
from time import sleep


class SolrLoad(object):

    def __init__(self, filetype, collectiondir, transformdir, localhost, collection, content_type, schemadir):
        # type: (object, object, object, object, object, object, object) -> object

        self.fileslist = []
        self.filetype = filetype
        self.collectiondir = collectiondir
        self.transformdir = transformdir
        self.localhost = localhost
        self.collection = collection
        self.content_type = content_type
        self.schemadir = schemadir

    def list_output_files(self):
        if self.collection == 'wos' or self.collection == 'lattes' or self.collection in ['capes_discentes','capes_docentes','capes_programas','rais_estabelecimentos']:

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
                        if f.endswith(self.filetype) and f.startswith('SP'):
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
                sleep(0.5)
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
            req = requests.get(url)
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
        url = 'http://192.168.0.212/solr/admin/collections?action=RELOAD&name=' + self.collection
        # url = 'http://192.168.0.212/solr/' + \
        #       self.collection + \
        #       '/update?commit=true&stream.body=<delete><query>*:*</query></delete>'
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
        command = '/opt/solr-6.6.2/bin/solr zk -upconfig -n ' + self.collection + ' -z 192.168.0.35:2181 -d ' + \
                  self.schemadir
        os.system(command)

    def full_sequence(self):
        print('Deleting collection')
        self.delete_collection()

        sleep(5)
        print('\n')
        print('Upload do schema')
        self.upload_schema()

        sleep(20)

        print('\n')
        print('Collection refresh')
        self.reload_collection()

        sleep(5)

        print('\n')
        print('Collection upload')
        self.files_load()

        print('\n')
        print('Carga finalizada')

# http://192.168.0.212/solr/< COLLECTION >/update?commit=true&stream.body=<delete><query>*:*</query></delete>

# HTTPERROR

# checar responses

# /opt/solr-6.6.2/bin/solr zk -upconfig -n enade  -z localhost:9983 -d <dir onde se encontra o managed-schema>
# /opt/solr-6.6.2/bin/solr zk -upconfig -n wos  -z localhost:9983 -d /home/gro/solr_conf/wos
# /opt/solr-6.6.2/bin/solr zk -upconfig -n bv_memoria  -z localhost:9983 -d /home/gro/solr_conf/bv_memoria

# http://192.168.0.212/solr/admin/collectionsaction=RELOAD&name=enade&wt=jso

# /opt/solr-6.6.2/bin/solr zk downconfig -z localhost:9983 -n capes_discentes -d /home/gro/solr_conf/capes_discentes/

# /opt/solr-6.6.2/bin/solr zk -n capes_docentes -upconfig -z 192.168.0.35:2181 -d  ./
# /opt/solr-6.6.2/bin/solr zk -n capes_docentes downconfig -z 192.168.0.35:2181 -d /home/gro/solr_conf/capes_docentes/
