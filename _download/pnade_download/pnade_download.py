# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, '../../../buscador_scripts/')

import os, errno
import requests
import zipfile
import subprocess

"""
Este script faz o downloa dos arquivos do Pnade e descompacta-os na pasta dos respectivos anos.
Deve-se escolher o ano de inicio e o ano final dos arquivos a serem baixados.
Antes de 2009, a nomenclatura e formato dos arquivos nao batem.
"""

all_links = {

    # '2011': 'http://web.fflch.usp.br/centrodametropole/pnad/PNAD_2011.7z',
    # '2012': 'http://web.fflch.usp.br/centrodametropole/pnad/PNAD_2012.7z',
    # '2013': 'http://web.fflch.usp.br/centrodametropole/pnad/PNAD_2013.7z',
    # '2014': 'http://web.fflch.usp.br/centrodametropole/pnad/PNAD_2014_atual.7z',
    '2015': 'http://web.fflch.usp.br/centrodametropole/pnad/PNAD_2015.7z',
}



# def download_enade(ano):
#     dir_destino = '/var/tmp/pnade/' + str(ano) + '/download/'
#     mbyte = 1024 * 1024
#     ano_str = str(ano)
#     nome_arquivo = ano_str + '.zip'
#     fullpath = dir_destino + nome_arquivo
#
#     # Criando o diretorio de destino dos arquivos baixados
#     try:
#         os.makedirs(dir_destino)
#     except OSError as e:
#         if e.errno != errno.EEXIST:
#             raise
#
#     # Fazendo o _download do arquivo
#     url = all_links[ano_str]
#     print(url)
#     resp = requests.get(url, stream=True)
#
#     fsize = int(resp.headers['content-length'])
#     print 'Downloading %s (%sMb)' % (fullpath, fsize / mbyte)
#     # Gravando o arquivo zip
#     with open(fullpath, 'wb') as f:
#         for chunk in resp.iter_content(chunk_size=1024*100):  # chuck size can be larger
#             if chunk:  # ignore keep-alive requests
#                 f.write(chunk)
#         f.close()
#
#     archive = zipfile.ZipFile(fullpath, 'r')
#     archive.extractall(dir_destino)
#     archive.close()
#
#     os.remove(fullpath)
#     print "Download do ano {} finalizado".format(ano)
#
# def executa_download_enade():
#     anos = all_links.keys()
#     for ano in anos:
#         try:
#             download_enade(ano)
#         except IndexError:
#             print('digite ano que deseja como parametro entre (2009~2016)')
#         except KeyError:
#             print('Ano invalido digite ano entre (2009~2016)')
#
# if __name__ == "__main__":
#     anos = all_links.keys()
#     for ano in anos:
#         try:
#             download_enade(ano)
#         except IndexError:
#             print('digite ano que deseja como parametro entre (2009~2016)')
#         except KeyError:
#             print('Ano invalido digite ano entre (2009~2016)')
# #
