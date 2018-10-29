import sys

sys.path.insert(0, '../../../buscador_scripts/')

from settings import BASE_PATH_DATA
import os, errno
import commands
from ftplib import FTP


# 7za x

def get_rais():
    anos = [str(x) for x in range(2013, 2015)]
    ftp = FTP("ftp.mtps.gov.br", timeout=10)
    ftp.login()
    ftp.cwd('pdet/microdados/RAIS/')
    for ano in anos:
        dir_destino = BASE_PATH_DATA + 'rais/' + str(ano) + '/download/'
        try:
            os.makedirs(dir_destino)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        ftp.cwd(ano)
        filelist = ftp.nlst()
        for f in filelist:
            if "estb" not in f.lower() and any(f.endswith(ext) for ext in '.7z'):
                fullpath = dir_destino + f
                print fullpath
                with open(fullpath, 'wb') as arq:
                    print ftp.retrbinary('RETR ' + f, arq.write, 8192 * 100)
                print commands.getstatusoutput('7za e ' + fullpath + ' -o' + dir_destino)[1]
                os.remove(fullpath)

        ftp.cwd('../')


def executa_rais():
    get_rais()
