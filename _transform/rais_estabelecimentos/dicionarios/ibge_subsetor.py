# -*- coding": utf-8 -*-


def ibge_sub_dic():
    ibge = {
        "01": "Extrativa mineral",
        "02": "Ind\xc3\xbastria de produtos minerais nao met\xc3\xa1licos",
        "03": "Ind\xc3\xbastria metal\xc3\xbargica",
        "04": "Ind\xc3\xbastria mec\xc3\xa2nica",
        "05": "Ind\xc3\xbastria do material el\xc3\xa9trico e de comunica\xc3\xa7oes",
        "06": "Ind\xc3\xbastria do material de transporte",
        "07": "Ind\xc3\xbastria da madeira e do mobili\xc3\xa1rio",
        "08": "Ind\xc3\xbastria do papel, papelao, editorial e gr\xc3\xa1fica",
        "09": "Ind. da borracha, fumo, couros, peles, similares, ind. diversas",
        "10": "Ind. qu\xc3\xadmica de produtos farmac\xc3\xaauticos, veterin\xc3\xa1rios, perfumaria",
        "11": "Ind\xc3\xbastria t\xc3\xaaxtil do vestu\xc3\xa1rio e artefatos de tecidos",
        "12": "Ind\xc3\xbastria de cal\xc3\xa7ados",
        "13": "Ind\xc3\xbastria de produtos aliment\xc3\xadcios, bebidas e \xc3\xa1lcool et\xc3\xadlico",
        "14": "Servi\xc3\xa7os industriais de utilidade p\xc3\xbablica",
        "15": "Constru\xc3\xa7ao civil",
        "16": "Com\xc3\xa9rcio varejista",
        "17": "Com\xc3\xa9rcio atacadista",
        "18": "Institui\xc3\xa7oes de cr\xc3\xa9dito, seguros e capitaliza\xc3\xa7ao",
        "19": "Com. e administra\xc3\xa7ao de im\xc3\xb3veis, valores mobili\xc3\xa1rios, serv. T\xc3\xa9cnico",
        "20": "Transportes e comunica\xc3\xa7oes",
        "21": "Serv. de alojamento, alimenta\xc3\xa7ao, repara\xc3\xa7ao, manuten\xc3\xa7ao, reda\xc3\xa7ao",
        "22": "Servi\xc3\xa7os m\xc3\xa9dicos, odontol\xc3\xb3gicos e veterin\xc3\xa1rios",
        "23": "Ensino",
        "24": "Administra\xc3\xa7ao p\xc3\xbablica direta e aut\xc3\xa1rquica",
        "25": "Agricultura, silvicultura, cria\xc3\xa7ao de animais, extrativismo vegetal",
        #"\x7b\xc3\xb1\x7d": "Ignorado"

    }
    d = {int(k): unicode(v, 'utf8') for k, v in ibge.items()}
    return d
