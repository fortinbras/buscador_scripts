import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from _download.enade_download import executa_download_enade
from _download.inep_download import executa_inep_download
from _download.pnade_download import executa_pnad
from _download.enem_download import executa_download_enem
from _download.rais import executa_rais
from _download.rais_estabelecimentos import executa_rais_estabelecimentos


def executa(coll):

    if coll == 'inep':
        executa_inep_download()

    elif coll == 'enade':
        executa_download_enade()

    elif coll == 'pnad':
        executa_pnad()

    elif coll == 'enem':
        executa_download_enem()

    elif coll == 'rais':
        executa_rais()

    elif coll == 'rais_estabelecimentos':
        executa_rais_estabelecimentos()

    else:
        print('digite enade ou inep como parametro')


if __name__ == "__main__":
    try:
        executa(sys.argv[1])
    except IndexError:
        print('Digite a collection como primeiro argumento! No segundo, um ano'
        ' de referencia ou 0 para baixar todos.')
        print('digite enade ou inep como parametro')
