# coding=utf-8
import errno
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from utils import *
import pandas as pd
import numpy as np
import codecs
import csv
import commands
import datetime


class inepVincDocentes(object):

    def __init__(self, ano):
        self.date = datetime.datetime.now()
        self.ano = ano
        self.input_lenght = 0
        self.output_length = 0

    def pega_arquivo_por_ano(self, ano):
        """ Para cada ano solicitado, retorna dict com o csv de docentes e csv de ies. """
        var = '/var/tmp/inep/' + str(ano) + '/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".CSV"):
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')

                    if file == 'DM_DOCENTE.CSV':
                        df_docentes = pd.read_csv(arquivo, sep='|', encoding='cp1252')
                        self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l')[1]
                        df_docentes.fillna('', inplace=True)
                        print 'Arquivo de entrada possui {} linhas'.format(int(self.input_lenght) - 1)
                    elif file == 'DM_IES.CSV':
                        df_ies = pd.read_csv(arquivo, sep='|', encoding='cp1252')
                        df_ies.fillna('', inplace=True)
        try:
            return {'docentes': df_docentes, 'ies': df_ies}
        except:
            pass

    def merge_docente_ies(self, ano):
        dic = self.pega_arquivo_por_ano(ano)
        df_docentes = dic['docentes']
        df_ies = dic['ies']
        df = df_docentes.merge(df_ies)
        df = df.astype(unicode)
        return df

    def manipula_df(self, ano):
        df = self.merge_docente_ies(ano)

        df['GEOGRAFICO_IES_facet'] = df['NO_REGIAO_IES'] + '|' + df['SGL_UF_IES'] + '|' + df['NO_MUNICIPIO_IES']

        df['MANT_IES_facet'] = df['NO_MANTENEDORA'] + '|' + df['NO_IES']

        df['ID'] = np.where(df['CO_DOCENTE_IES'], (str(ano) + '_' + df['CO_DOCENTE_IES']),
                            (str(ano) + '_' + df['CO_DOCENTE']))

        df['Data_Nasc_Docente_facet'] = df['NU_ANO_DOCENTE_NASC'].astype(str) + '|' + df['NU_MES_DOCENTE_NASC'].astype(
            str) + '|' + df['NU_DIA_DOCENTE_NASC'].astype(str)
        ano_str = str(ano)
        df['ANO_facet'] = gYear(ano_str)

        return df

    def resolve_dicionarios(self, ano):
        df = self.manipula_df(ano)

        CHAVES_SIM_NAO = ['IN_CAPITAL_IES', 'IN_ATU_EAD', 'IN_ATU_POS_EAD', 'IN_ATU_EXTENSAO', 'IN_ATU_GESTAO',
                          'IN_ATU_GRAD_PRESENCIAL',
                          'IN_ATU_GRAD_PRESENCIAL', 'IN_ATU_POS_PRESENCIAL', 'IN_ATU_SEQUENCIAL', 'IN_ATU_PESQUISA',
                          'IN_BOLSA_PESQUISA', 'IN_SUBSTITUTO', 'IN_EXERCICIO_DT_REF', 'IN_VISITANTE']

        DEFICIENCIA = ['IN_DOCENTE_DEFICIENCIA', 'IN_DEF_CEGUEIRA', 'IN_DEF_BAIXA_VISAO', 'IN_DEF_SURDEZ',
                       'IN_DEF_AUDITIVA',
                       'IN_DEF_FISICA', 'IN_DEF_SURDOCEGUEIRA', 'IN_DEF_MULTIPLA', 'IN_DEF_INTELECTUAL', ]

        SIM_NAO = {'0.0': 'Não', '1.0': 'Sim', 'nan': 'Não Informado'}
        ESCOLARIDADE = {'1': 'Sem graduação', '2': 'Graduação', '3': 'Especialização', '4': 'Mestrado',
                        '5': 'Doutorado'}
        DEFICIENCIA_FISICA = {'0': 'Não', '1': 'Sim', '2': 'Não dispõe de informação', 'nan': 'Não'}
        IN_VISITANTE_IFES_VINCULO = {'1.0': 'Em folha', '2.0': 'Bolsista', '0.0': 'Não informado'}

        CO_CATEGORIA_ADMINISTRATIVA = {'1': 'Publica Federal', '2': 'Publica Estadual', '3': 'Publica Municipal',
                                       '4': 'Privada com fins lucrativos', '5': 'Privada sem fins lucrativos',
                                       '7': 'Especial'}

        CO_SITUACAO_DOCENTE = {'1': 'Em exercício', '2': 'Afastado para qualificação',
                               '3': 'Afastado para exercício em outros órgãos/entidades',
                               '4': 'Afastado por outros motivos', '5': 'Afastado para tratamento de saúde'}

        df['CO_ESCOLARIDADE_DOCENTE'] = df['CO_ESCOLARIDADE_DOCENTE'].replace(
            ESCOLARIDADE)
        df['CO_CATEGORIA_ADMINISTRATIVA'] = df['CO_CATEGORIA_ADMINISTRATIVA'].replace(
            CO_CATEGORIA_ADMINISTRATIVA)
        df['CO_SITUACAO_DOCENTE'] = df['CO_SITUACAO_DOCENTE'].replace(
            CO_SITUACAO_DOCENTE)
        df['CO_UF_NASCIMENTO'].fillna(0, inplace=True)
        df['CO_MUNICIPIO_NASCIMENTO'].fillna(0, inplace=True)
        df['IN_VISITANTE_IFES_VINCULO'].fillna(0, inplace=True)
        df['IN_VISITANTE_IFES_VINCULO'] = df['IN_VISITANTE_IFES_VINCULO'].replace(
            IN_VISITANTE_IFES_VINCULO)
        df['IN_CAPITAL_IES'] = np.where(df['IN_CAPITAL_IES'] == 1, 'Sim', 'Não')
        del (df['CO_ORGANIZACAO_ACADEMICA'])
        del (df['IN_SEXO_DOCENTE'])
        del (df['CO_REGIME_TRABALHO'])
        del (df['DS_CATEGORIA_ADMINISTRATIVA'])
        del (df['DS_SITUACAO_DOCENTE'])
        del (df['DS_ESCOLARIDADE_DOCENTE'])
        del (df['CO_NACIONALIDADE_DOCENTE'])

        for d in DEFICIENCIA:
            df[d] = df[d].replace(DEFICIENCIA_FISICA)

        for d in CHAVES_SIM_NAO:
            df[d] = df[d].replace(SIM_NAO)

        municipios = pd.read_csv('lista_municipios.csv', sep=';')
        municipios['CÓDIGO DO MUNICÍPIO'] = municipios['CÓDIGO DO MUNICÍPIO'].astype(str)
        municipios['CÓDIGO DO MUNICÍPIO'] = map(lambda x: x.encode('cp1252', 'strict'),
                                                municipios['CÓDIGO DO MUNICÍPIO'])
        municipios['Regiao'] = municipios['CÓDIGO DO MUNICÍPIO'].apply(find_regiao)
        municipios.rename(columns={'CÓDIGO DO MUNICÍPIO': 'CO_MUNICIPIO_NASCIMENTO'}, inplace=True)

        df[['MUNICIPIO_NASCIMENTO', 'UF_NASCIMENTO', 'REG_NASCIMENTO']] = pd.merge(df, municipios,
                                                                                   how='left', on=[
                'CO_MUNICIPIO_NASCIMENTO']).loc[:, ['NOME DO MUNICÍPIO', 'UF', 'Regiao']]
        df['UF_NASCIMENTO'].fillna('Não Informado', inplace=True)
        df['MUNICIPIO_NASCIMENTO'].fillna('Não Informado', inplace=True)
        df['REG_NASCIMENTO'].fillna('Não Informado', inplace=True)

        df['GEOGRAFICO_DOC_NASC_facet'] = df['REG_NASCIMENTO'] + '|' + df[
            'UF_NASCIMENTO'] + '|' + df['MUNICIPIO_NASCIMENTO']

        return df

    def gera_csv(self):
        df = self.resolve_dicionarios(self.ano)
        destino_transform = '/var/tmp/inep/' + str(ano) + '/transform/docentes'
        csv_file = '/docentes_vinculo_ies_' + str(ano) + '.csv'
        log_file = '/enade_' + str(self.ano) + '.log'
        try:
            os.makedirs(destino_transform)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        df.to_csv(destino_transform + csv_file, sep=';', index=False, encoding='utf8', quoting=csv.QUOTE_NONNUMERIC)
        self.output_length = commands.getstatusoutput('cat ' + destino_transform + csv_file + ' |wc -l')[1]
        print 'Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1)

        with open(destino_transform + log_file, 'w') as log:
            log.write('Log gerado em {}'.format(self.date.strftime("%Y-%m-%d %H:%M")))
            log.write("\n")
            log.write('Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1))
            log.write("\n")
            log.write('Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1))
        print('Processamento ENADE {} finalizado, arquivo de log gerado em {}'.format(self.ano,
                                                                                      destino_transform + log_file))


if __name__ == "__main__":

    PATH_ORIGEM = '/var/tmp/inep/'
    try:
        anos = os.listdir(PATH_ORIGEM)
        anos.sort()
    except OSError:
        print('Nenhuma pasta encontrada')
        raise
    for ano in anos:
        print(ano)
        try:
            inep_doc = inepVincDocentes(ano)
            inep_doc.gera_csv()
            print('Arquivo do ano, {} finalizado'.format(ano))
        except:
            print('Arquivo do ano, {} não encontrado'.format(ano))
            raise
