# -*- coding":  utf-8 -*-


def uf_dic():
    uf = {
        "11": "Rond\xc3\xb4nia",
        "12": "Acre",
        "13": "Amazonas",
        "14": "Roraima",
        "15": "Par\xc3\xa1",
        "16": "Amap\xc3\xa1",
        "17": "Tocantins",
        "21": "Maranh\xc3\xa3o",
        "22": "Piau\xc3\xad",
        "23": "Cear\xc3\xa1",
        "24": "Rio Grande do Norte",
        "25": "Para\xc3\xadba",
        "26": "Pernambuco",
        "27": "Alagoas",
        "28": "Sergipe",
        "29": "Bahia",
        "31": "Minas Gerais",
        "32": "Esp\xc3\xadrito Santo",
        "33": "Rio de Janeiro",
        "35": "S\xc3\xa3o Paulo",
        "41": "Paran\xc3\xa1",
        "42": "Santa Catarina",
        "43": "Rio Grande do Sul",
        "50": "Mato Grosso do Sul",
        "51": "Mato Grosso",
        "52": "Goi\xc3\xa1s",
        "53": "Distrito Federal"
    }
    d = {int(k):  unicode(v, 'utf8') for k, v in uf.items()}
    return d
