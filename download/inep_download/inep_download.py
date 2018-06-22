# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, '../../../buscador_scripts/')

import os, errno
import requests
import zipfile
import patoolib


"""
Este script faz o downloa dos arquivos do INEP e descompacta-os na pasta dos respectivos anos.
Deve-se escolher o ano de inicio e o ano final dos arquivos a serem baixados.
Antes de 2009, a nomenclatura e formato dos arquivos nao batem.
"""

all_links = {
    # '1995': 'http://download.inep.gov.br/microdados/micro_censo_edu_superior1995.zip',
    # '1996': 'http://download.inep.gov.br/microdados/micro_censo_edu_superior1996.zip',
    # '1997': 'http://download.inep.gov.br/microdados/micro_censo_edu_superior1997.zip',
    # '1998': 'http://download.inep.gov.br/microdados/micro_censo_edu_superior1998.zip',
    # '1999': 'http://download.inep.gov.br/microdados/micro_censo_edu_superior1999.zip',
    # '2000': 'http://download.inep.gov.br/microdados/micro_censo_edu_superior2000.zip',
    # '2001': 'http://download.inep.gov.br/microdados/micro_censo_edu_superior2001.zip',
    # '2002': 'http://download.inep.gov.br/microdados/micro_censo_edu_superior2002.zip',
    # '2003': 'http://download.inep.gov.br/microdados/micro_censo_edu_superior2003.zip',
    # '2004': 'http://download.inep.gov.br/microdados/microdados_censo_educacao_superior_2004.zip',
    # '2005': 'http://download.inep.gov.br/microdados/microdados_censo_educacao_superior_2005.zip',
    # '2006': 'http://download.inep.gov.br/microdados/microdados_educacao_superior_2006.zip',
    # '2007': 'http://download.inep.gov.br/microdados/microdados_educacao_superior_2007.zip',
    # '2008': 'http://download.inep.gov.br/microdados/micro_censo_edu_superior2008.zip',
    '2009': 'http://download.inep.gov.br/microdados/microdados_censo_superior_2009.zip',
    '2010': 'http://download.inep.gov.br/microdados/microdados_censo_superior_2010.zip',
    '2011': 'http://download.inep.gov.br/microdados/microdados_censo_superior_2011.zip',
    '2012': 'http://download.inep.gov.br/microdados/microdados_censo_superior_2012.zip',
    '2013': 'http://download.inep.gov.br/microdados/microdados_censo_superior_2013.zip',
    '2014': 'http://download.inep.gov.br/microdados/microdados_censo_superior_2014.zip',
    '2015': 'http://download.inep.gov.br/microdados/microdados_censo_superior_2015.zip',
    '2016': 'http://download.inep.gov.br/microdados/microdados_censo_superior_2016.zip'
}


def download_censo_superior(ano):
    dir_destino = '/var/tmp/inep/' + str(ano) + '/download/'
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

    # Fazendo o download do arquivo
    url = all_links[ano_str]
    print(url)
    resp = requests.get(url, stream=True)

    fsize = int(resp.headers['content-length'])
    print 'Downloading %s (%sMb)' % (fullpath, fsize / mbyte)
    # Gravando o arquivo zip
    with open(fullpath, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        f.close()

    archive = zipfile.ZipFile(fullpath, 'r')
    archive.extractall(dir_destino)
    archive.close()

    os.remove(fullpath)

    try:
        for root, dirs, files in os.walk(dir_destino):
            for file in files:
                if file.endswith('.rar'):
                    patoolib.extract_archive(os.path.join(root, file), outdir=root)
                    os.remove(os.path.join(root, file))
    except:

        raise


if __name__ == "__main__":
    anos = all_links.keys()
    for ano in anos:
        try:
            download_censo_superior(ano)
        except IndexError:
            print('digite ano que deseja como parametro entre (2009~2016)')
        except KeyError:
            print('Ano invalido digite ano entre (2009~2016)')
