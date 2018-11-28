# -*- coding" : "utf-8 -*-

def cod_tipo_institu_dic():
    instituicao = {

        "1" : "Instituição de Ensino Superior",
        "2" : "Instituto de Pesquisa",
        "3" : "Instituição de Saúde",
        "9" : "Outras Instituições"

        }

d = {int(k): unicode(v, 'utf8') for k, v in instituicao.items()}
return d
