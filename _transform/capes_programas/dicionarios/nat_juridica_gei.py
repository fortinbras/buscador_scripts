# -*- coding" : "utf-8 -*-

def nat_jurudica_gei_dic():
    juridico = {

        "1" : "Pública Federal",
        "2" : "Pública Estadual",
        "3" : "Pública Municipal",
        "4" : "Privada com fins lucrativos",
        "5" : "Privada sem fins lucrativos",
        "7" : "Pública Municipal"
    }

d = {int(k): unicode(v, 'utf8') for k, v in juridico.items()}
return d
