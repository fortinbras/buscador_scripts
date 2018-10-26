# -*- coding":  utf-8 -*-


def regioes_adm_df_dic():
    regioes = {
        "1": "Bras\xc3\xadlia",
        "2": "Cruzeiro",
        "3": "Guar\xc3\xa1",
        "4": "Lago Norte",
        "5": "Parano\xc3\xa1",
        "6": "Lago Sul",
        "7": "S\xc3\xa3o Sebasti\xc3\xa3o",
        "8": "N\xc3\xbacleo Bandeirante",
        "9": "Candangol\xc3\xa2ndia",
        "10": "Riacho Fundo",
        "11": "Taguatinga",
        "12": "Ceil\xc3\xa2ndia",
        "13": "Samambaia",
        "14": "Gama",
        "15": "Santa Maria",
        "16": "Recanto das Emas",
        "17": "Brazlandia",
        "18": "Sobradinho",
        "19": "Planaltina",
        " 0": "Fora do Distrito Federal",
        "-1": "Ignorado"
    }

    d = {int(k):  unicode(v, 'utf8') for k, v in regioes.items()}
    return d
