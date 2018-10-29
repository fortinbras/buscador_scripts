# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, '../../../buscador_scripts/')

from settings import BASE_PATH_DATA
import os, errno
import requests
import zipfile
import patoolib

"""
Este script faz o downloa dos arquivos do ENEM e descompacta-os na pasta dos respectivos anos.
Deve-se escolher o ano de inicio e o ano final dos arquivos a serem baixados.
Antes de 2009, a nomenclatura e formato dos arquivos nao batem.
"""

all_links = {

    # '2011': 'http://download.inep.gov.br/microdados/microdados_enem2011.zip', #Não esta em csv
    # '2012': 'http://download.inep.gov.br/microdados/microdados_enem2012.zip',
    # '2013': 'http://download.inep.gov.br/microdados/microdados_enem2013.zip',
    # '2014': 'http://download.inep.gov.br/microdados/microdados_enem2014.zip',
    # '2015': 'http://download.inep.gov.br/microdados/microdados_enem2015.zip',
    # '2016': 'http://download.inep.gov.br/microdados/microdados_enem2016.zip',
    '2017': 'http://download.inep.gov.br/microdados/microdados_enem2017.zip',
}


def download_enem(ano):
    dir_destino = BASE_PATH_DATA + 'enem/' + str(ano) + '/download/'
    mbyte = 1024 * 1024
    ano_str = str(ano)
    nome_arquivo = ano_str + '.zip'
    fullpath = dir_destino + nome_arquivo

    # Criando o diretorio de destino dos arquivos baixados
    try:
        os.makedirs(dir_destino)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Fazendo o _download do arquivo
    url = all_links[ano_str]
    print(url)
    resp = requests.get(url, stream=True)

    fsize = int(resp.headers['content-length'])
    print 'Downloading %s (%sMb)' % (fullpath, fsize / mbyte)
    # Gravando o arquivo zip
    with open(fullpath, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):  # chuck size can be larger
            if chunk:  # ignore keep-alive requests
                f.write(chunk)
        f.close()

    archive = zipfile.ZipFile(fullpath, 'r')
    archive.extractall(dir_destino)
    archive.close()

    os.remove(fullpath)

    if ano == '2013':
        try:
            exclude_prefixes = ('__', '.')
            for root, dirs, files in os.walk(dir_destino, topdown=True):
                dirs[:] = [dirname for dirname in dirs if not dirname.startswith(exclude_prefixes)]
                for f in files:
                    if f.endswith('.rar'):
                        patoolib.extract_archive(os.path.join(root, f), outdir=root)
                        os.remove(os.path.join(root, f))
        except:
            raise
    print "Download do ano {} finalizado".format(ano)


def executa_download_enem():
    anos = all_links.keys()
    for ano in anos:
        try:
            download_enem(ano)
        except IndexError:
            print('digite ano que deseja como parametro entre (2009~2016)')
        except KeyError:
            print('Ano invalido digite ano entre (2009~2016)')

#
# if __name__ == "__main__":
#     anos = all_links.keys()
#     for ano in anos:
#         try:
#             download_enem(ano)
#         except IndexError:
#             print('digite ano que deseja como parametro entre (2009~2017)')
#         except KeyError:
#             print('Ano invalido digite ano entre (2009~2017)')
