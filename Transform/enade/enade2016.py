# coding=utf-8

import pandas as pd
import os

from Transform.utils import gYear


def catg_adm_inst(cod):
    if cod == 93:
        value = 'Pessoa Jurídica de Direito Público - Federal'
    elif cod == 115:
        value = 'Pessoa Jurídica de Direito Público - Estadual'
    elif cod == 116:
        value = 'Pessoa Jurídica de Direito Público - Municipal'
    elif cod == 118:
        value = 'Pessoa Jurídica de Direito Privado - Com fins lucrativos - Sociedade Civil'
    elif cod == 121:
        value = 'Pessoa Jurídica de Direito Privado - Sem fins lucrativos - Fundação'
    elif cod == 10001:
        value = 'Pessoa Jurídica de Direito Público - Estadual'
    elif cod == 10002:
        value = 'Pessoa Jurídica de Direito Público - Federal'
    elif cod == 10003:
        value = 'Pessoa Jurídica de Direito Público - Municipal'
    elif cod == 10004:
        value = 'Pessoa Jurídica de Direito Privado - Com fins lucrativos - Associação de Utilidade Pública'
    elif cod == 10005:
        value = 'Privada com fins lucrativos'
    elif cod == 10006:
        value = 'Pessoa Jurídica de Direito Privado - Com fins lucrativos - Sociedade Mercantil ou Comercial'
    elif cod == 10007:
        value = 'Pessoa Jurídica de Direito Privado - Sem fins lucrativos - Associação de Utilidade Pública'
    elif cod == 10008:
        value = 'Privada sem fins lucrativos'
    elif cod == 10009:
        value = 'Pessoa Jurídica de Direito Privado - Sem fins lucrativos - Sociedade'
    elif cod == 17634:
        value = 'Fundação Pública de Direito Privado Municípal'
    else:
        value = cod
    return value


def catg_acad_inst(cod):
    if cod == 10019:
        value = 'Centro Federal de Educação Tecnológica'
    elif cod == 10020:
        value = 'Centro Universitário'
    elif cod == 10022:
        value = 'Faculdade'
    elif cod == 10026:
        value = 'Instituto Federal de Educação, Ciência e Tecnologia'
    elif cod == 10028:
        value = 'Universidade'
    else:
        value = cod
    return value


def area_enquad(cod):
    if cod == 5:
        value = 'MEDICINA VETERINÁRIA'
    elif cod == 6:
        value = 'ODONTOLOGIA'
    elif cod == 12:
        value = 'MEDICINA'
    elif cod == 17:
        value = 'AGRONOMIA'
    elif cod == 19:
        value = 'FARMÁCIA'
    elif cod == 23:
        value = 'ENFERMAGEM'
    elif cod == 27:
        value = 'FONOAUDIOLOGIA'
    elif cod == 28:
        value = 'NUTRIÇÃO'
    elif cod == 36:
        value = 'FISIOTERAPIA'
    elif cod == 38:
        value = "SERVIÇO SOCIAL"
    elif cod == 51:
        value = 'ZOOTECNIA'
    elif cod == 55:
        value = 'BIOMEDICINA'
    elif cod == 69:
        value = 'TECNOLOGIA EM RADIOLOGIA'
    elif cod == 90:
        value = 'TECNOLOGIA EM AGRONEGÓCIOS'
    elif cod == 91:
        value = 'TECNOLOGIA EM GESTÃO HOSPITALAR'
    elif cod == 92:
        value = 'TECNOLOGIA EM GESTÃO AMBIENTAL'
    elif cod == 95:
        value = 'TECNOLOGIA EM ESTÉTICA E COSMÉTICA'
    elif cod == 3501:
        value = 'EDUCAÇÃO FÍSICA (BACHARELADO)'
    else:
        value = cod
    return value


def cod_moda(cod):
    if cod == 0:
        value = 'EAD'
    elif cod == 1:
        value = 'Presencial'
    else:
        value = cod
    return value


def generate_csv(input,output,lista_municipios):
    colunas = [
        'NU_ANO',
        'CO_IES',
        'CO_CATEGAD',
        'CO_ORGACAD',
        'CO_GRUPO',
        'CO_CURSO',
        'CO_MODALIDADE',
        'CO_MUNIC_CURSO',
        'CO_UF_CURSO',
        # 'CO_REGIAO_CURSO',
        'NU_IDADE',
        'TP_SEXO',
        'ANO_FIM_2G',
        'ANO_IN_GRAD',
        # 'TP_SEMESTRE',
        # 'IN_MATUT',
        # 'IN_VESPER',
        # 'IN_NOTURNO',
        # 'ID_STATUS',
        # 'AMOSTRA',
        # 'IN_GRAD'
    ]

    df = pd.read_csv(input, sep=';')
    df1 = df.loc[:, colunas]

    df1.CO_CATEGAD = df1.loc[:, 'CO_CATEGAD'].apply(catg_adm_inst)
    df1.CO_ORGACAD = df1.loc[:, 'CO_ORGACAD'].apply(catg_acad_inst)
    df1.CO_GRUPO = df1.loc[:, 'CO_GRUPO'].apply(area_enquad)
    df1.CO_MODALIDADE = df1.loc[:, 'CO_MODALIDADE'].apply(cod_moda)

    municipios = pd.read_csv(lista_municipios, sep=';')
    municipios = municipios.rename(columns={'CÓDIGO DO MUNICÍPIO': 'CO_MUNIC_CURSO'})
    df1[['CO_MUNIC_CURSO', 'CO_UF_CURSO']] = pd.merge(df1, municipios, on=['CO_MUNIC_CURSO']).loc[:,
                                             ['NOME DO MUNICÍPIO', 'UF']]

    df1['CO_MUNIC_CURSO'] = df1['CO_MUNIC_CURSO'].astype(str) + ';' + df1['CO_UF_CURSO'].astype(str)
    df1.rename(columns={'CO_MUNIC_CURSO': 'Cidade;Estado'})
    del (df1['CO_UF_CURSO'])
    df1['GRUPO_ANO'] = gYear(2016)

    outdir = './enade2016_out'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    fullname = os.path.join(outdir, output)


    df1.to_csv(fullname, sep='|', index=False)
