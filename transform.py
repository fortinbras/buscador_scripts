# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')
from _transform.enade import enade_tranform
from _transform.inep_docentes import inep_docentes_tranform
from _transform.inep_alunos import inep_alunos_transform
from _transform.wos import wos_tranform


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

    elif coll == 'lattes':
        pass

    else:
        print('digite collection como parametro')


if __name__ == "__main__":
    try:
        executa(sys.argv[1])
    except IndexError:
        print('digite collection como parametro')
