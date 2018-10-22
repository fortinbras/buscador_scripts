import sys

sys.path.insert(0, '../../../buscador_scripts/')

import os, errno
import commands
from ftplib import FTP


# 7za x

def get_rais_estabelecimento():
    anos = [str(x) for x in range(2010, 2018)]
    print
    print('Anos = ', anos)

    ftp = FTP("ftp.mtps.gov.br", timeout=10)
    ftp.login()
    ftp.cwd('pdet/microdados/RAIS/')
    for ano in anos:
        dir_destino = '/var/tmp/solr_front/collections/rais_estabelecimento/' + str(ano) + '/download/'
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


def executa_rais_estabelecimento():
    get_rais_estabelecimento()
