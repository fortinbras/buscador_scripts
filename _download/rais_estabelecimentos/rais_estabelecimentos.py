import sys

sys.path.insert(0, '../../../buscador_scripts/')

import os, errno
import commands
from ftplib import FTP


# 7za x

def get_rais_estabelecimentos():
    '''
    Função para download dos arquivos da Rais Estabelecimentos, esta função faz
    o download via ftp dos arquivos dos anos de 2010 a 2018 - apenas arquivos
    com o nome ESTB+ano.7z e cria o diretório onde serão salvos.

    PARAMETROS:
    Sem parâmetros.

    RETORNO:
    Sem retorno.

    '''
    anos = [str(x) for x in range(2010, 2018)]
    print
    print('Anos = ', anos)

    ftp = FTP("ftp.mtps.gov.br", timeout=10)
    ftp.login()
    ftp.cwd('pdet/microdados/RAIS/')
    for ano in anos:
        dir_destino = '/var/tmp/solr_front/collections/rais_estabelecimentos/' + str(ano) + '/download/'
        try:
            os.makedirs(dir_destino)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        ftp.cwd(ano)
        filelist = ftp.nlst()
        print
        print('FILELIST = ',filelist)
        print

        for f in filelist:
            if "estb" in f.lower() and any(f.endswith(txt) for txt in '.7z'):
                fullpath = dir_destino + f
                print fullpath

                with open(fullpath, 'wb') as arq:
                    print ftp.retrbinary('RETR ' + f, arq.write, 8192 * 100)
                print commands.getstatusoutput('7za e ' + fullpath + ' -o' + dir_destino)[1]
                os.remove(fullpath)

        ftp.cwd('../')


def executa_rais_estabelecimentos():
    '''
    Função chamada em download.py para download dos arquivos da rais estabelecimentos,
    esta função chama a função get_rais_estabelecimentos que faz o download dos arquivos.

    PARAMETROS:
    Sem parâmetros.

    RETORNO:
    Sem retorno.

    '''
    get_rais_estabelecimentos()
