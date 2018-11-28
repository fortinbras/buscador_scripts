# -*- coding" : "utf-8 -*-

def cod_org_acad_gei_dic():
    academico = {

        "1" : "Universidade",
        "2" : "Centro Universitário",
        "3" : "Faculdade",
        "4" : "IFECT ou CFET",
        "9" : "Não se aplica"
        }

d = {int(k): unicode(v, 'utf8') for k, v in academico.items()}
return d
