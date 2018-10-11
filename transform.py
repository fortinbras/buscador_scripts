# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')
from _transform.enade import enade_tranform
from _transform.inep_docentes import inep_docentes_tranform
from _transform.inep_alunos import inep_alunos_transform
from _transform.wos import wos_tranform
from _transform.pnade import pnade_tranform
from _transform.enem import enem_transform
from _transform.rais import rais_transform
from _transform.capes_discentes import capes_discentes_transform
#from _transform.capes_docentes import capes_docentes_transform



def executa(coll):
    """
    :param coll: argumento para selecionar collection que será executada ex. "python load.py wos" para webOfScience

    """

    if coll == 'inep_alunos':
        inep_alunos_transform()

    elif coll == 'inep_docentes':
        inep_docentes_tranform()

    elif coll == 'enade':
        enade_tranform()

    elif coll == 'wos':
        wos_tranform()

    elif coll == 'pnad':
        pnade_tranform()

    elif coll == 'enem':
        enem_transform()

    elif coll == 'lattes':
        pass

    elif coll == 'rais':
        rais_transform()

    elif coll == 'capes_discentes':
        capes_discentes_transform()

    elif coll == 'capes_docentes':
        capes_docentes_transform()

    else:
        print('digite collection como parametro')


if __name__ == "__main__":
    try:
        executa(sys.argv[1])
    except IndexError:
        print('digite collection como parametro')
