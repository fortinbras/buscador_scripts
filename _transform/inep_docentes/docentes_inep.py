# coding=utf-8
import errno
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from settings import BASE_PATH_DATA
from utils import *
import pandas as pd
import numpy as np
import codecs
import csv
import commands
import datetime


class inepVincDocentes():

    def __init__(self, ano):
        self.date = datetime.datetime.now()
        self.ano = ano
        self.input_lenght = 0
        self.output_length = 0

    def pega_arquivo_por_ano(self, ano):
        """ Para cada ano solicitado, retorna dict com o csv de docentes e csv de ies. """
        var = BASE_PATH_DATA + 'inep/' + str(ano) + '/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".CSV"):
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')

                    if file == 'DM_DOCENTE.CSV':
                        df_docentes = pd.read_csv(arquivo, sep='|', encoding='cp1252', low_memory=False)
                        self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l')[1]
                        # df_docentes.fillna('', inplace=True)
                        print 'Arquivo de entrada possui {} linhas'.format(int(self.input_lenght) - 1)
                    elif file == 'DM_IES.CSV':
                        df_ies = pd.read_csv(arquivo, sep='|', encoding='cp1252', low_memory=False)
                        # df_ies.fillna('', inplace=True)
        try:
            return {'docentes': df_docentes, 'ies': df_ies}
        except:
            pass

    def merge_docente_ies(self, ano):
        columns = [u'CO_IES', u'NO_IES', u'CO_CATEGORIA_ADMINISTRATIVA',
                   u'DS_CATEGORIA_ADMINISTRATIVA',
                   u'DS_ORGANIZACAO_ACADEMICA', u'CO_DOCENTE_IES', u'CO_DOCENTE',
                   u'CO_SITUACAO_DOCENTE',
                   u'DS_ESCOLARIDADE_DOCENTE',
                   u'DS_REGIME_TRABALHO', u'DS_SEXO_DOCENTE',
                   u'NU_ANO_DOCENTE_NASC', u'NU_MES_DOCENTE_NASC', u'NU_DIA_DOCENTE_NASC',
                   u'DS_COR_RACA_DOCENTE', u'CO_NACIONALIDADE_DOCENTE', u'CO_UF_NASCIMENTO',
                   u'CO_MUNICIPIO_NASCIMENTO', u'IN_DOCENTE_DEFICIENCIA', u'IN_ATU_EAD',
                   u'IN_ATU_EXTENSAO', u'IN_ATU_GESTAO', u'IN_ATU_GRAD_PRESENCIAL',
                   u'IN_ATU_POS_EAD', u'IN_ATU_POS_PRESENCIAL', u'IN_ATU_SEQUENCIAL',
                   u'IN_ATU_PESQUISA', u'IN_BOLSA_PESQUISA', u'IN_SUBSTITUTO',
                   u'IN_EXERCICIO_DT_REF', u'IN_VISITANTE', u'IN_VISITANTE_IFES_VINCULO',
                   u'CO_MANTENEDORA', u'NO_MANTENEDORA', u'CO_MUNICIPIO_IES',
                   u'NO_MUNICIPIO_IES', u'CO_UF_IES', u'SGL_UF_IES', u'NO_REGIAO_IES',
                   u'IN_CAPITAL_IES', u'QT_TEC_TOTAL', u'QT_TEC_FUND_INCOMP_FEM',
                   u'QT_TEC_FUND_INCOMP_MASC', u'QT_TEC_FUND_COMP_FEM',
                   u'QT_TEC_FUND_COMP_MASC', u'QT_TEC_MEDIO_FEM', u'QT_TEC_MEDIO_MASC',
                   u'QT_TEC_SUPERIOR_FEM', u'QT_TEC_SUPERIOR_MASC',
                   u'QT_TEC_ESPECIALIZACAO_FEM', u'QT_TEC_ESPECIALIZACAO_MASC',
                   u'QT_TEC_MESTRADO_FEM', u'QT_TEC_MESTRADO_MASC',
                   u'QT_TEC_DOUTORADO_FEM', u'QT_TEC_DOUTORADO_MASC',
                   u'IN_ACESSO_PORTAL_CAPES', u'IN_ACESSO_OUTRAS_BASES', u'IN_REFERENTE',
                   u'VL_RECEITA_PROPRIA', u'VL_TRANSFERENCIA', u'VL_OUTRA_RECEITA',
                   u'VL_DES_PESSOAL_REM_DOCENTE', u'VL_DES_PESSOAL_REM_TECNICO',
                   u'VL_DES_PESSOAL_ENCARGO', u'VL_DES_CUSTEIO', u'VL_DES_INVESTIMENTO',
                   u'VL_DES_PESQUISA', u'VL_DES_OUTRAS']
        dic = self.pega_arquivo_por_ano(ano)
        df_docentes = dic['docentes']
        df_ies = dic['ies']
        df = df_docentes.merge(df_ies, how='left')
        # df = df.astype(unicode)
        return df[columns]

    def manipula_df(self, ano):
        df = self.merge_docente_ies(ano)

        df['GEOGRAFICO_IES_facet'] = df['NO_REGIAO_IES'] + '|' + df['SGL_UF_IES'] + '|' + df['NO_MUNICIPIO_IES']
        df['GEOGRAFICO_IES_facet'] = df['NO_REGIAO_IES'] + '|' + df['SGL_UF_IES'] + '|' + df['NO_MUNICIPIO_IES']

        df['MANT_IES_facet'] = df['NO_MANTENEDORA'] + '|' + df['NO_IES']

        df['ID'] = np.where(df['CO_DOCENTE_IES'], (str(ano) + '_' + df['CO_DOCENTE_IES'].astype(str)),
                            (str(ano) + '_' + df['CO_DOCENTE'].astype(str)))

        df['Data_Nasc_Docente_facet'] = df['NU_ANO_DOCENTE_NASC'].astype(str) + '|' + df['NU_MES_DOCENTE_NASC'].astype(
            str) + '|' + df['NU_DIA_DOCENTE_NASC'].astype(str)
        ano_str = str(ano)
        df['ANO_facet'] = gYear(ano_str)
        municipios = pd.read_csv('lista_municipios.csv', sep=';')
        municipios.rename(columns={'CÓDIGO DO MUNICÍPIO': 'CO_MUNICIPIO_NASCIMENTO'}, inplace=True)
        municipios['Regiao'] = municipios['CO_MUNICIPIO_NASCIMENTO'].apply(find_regiao)
        df[['MUNICIPIO_NASCIMENTO', 'UF_NASCIMENTO', 'REG_NASCIMENTO']] = pd.merge(df, municipios,
                                                                                   how='left', on=[
                'CO_MUNICIPIO_NASCIMENTO']).loc[:, ['NOME DO MUNICÍPIO', 'UF', 'Regiao']]
        df['GEOGRAFICO_DOC_NASC_facet'] = df['REG_NASCIMENTO'] + '|' + df[
            'UF_NASCIMENTO'] + '|' + df['MUNICIPIO_NASCIMENTO']

        return df

    def resolve_dicionarios(self):
        df = self.manipula_df(self.ano)

        CHAVES_SIM_NAO = ['IN_CAPITAL_IES', 'IN_ATU_EAD', 'IN_ATU_POS_EAD', 'IN_ATU_EXTENSAO', 'IN_ATU_GESTAO',
                          'IN_ATU_GRAD_PRESENCIAL',
                          'IN_ATU_GRAD_PRESENCIAL', 'IN_ATU_POS_PRESENCIAL', 'IN_ATU_SEQUENCIAL', 'IN_ATU_PESQUISA',
                          'IN_BOLSA_PESQUISA', 'IN_SUBSTITUTO', 'IN_EXERCICIO_DT_REF', 'IN_VISITANTE']

        DEFICIENCIA = ['IN_DOCENTE_DEFICIENCIA']

        SIM_NAO = {'0.0': 'Não', '1.0': 'Sim', 'nan': 'Não Informado'}
        DEFICIENCIA_FISICA = {'0': 'Não', '1': 'Sim', '2': 'Não dispõe de informação', 'nan': 'Não'}
        IN_VISITANTE_IFES_VINCULO = {1: 'Em folha', 2: 'Bolsista'}

        CO_CATEGORIA_ADMINISTRATIVA = {'1': 'Publica Federal', '2': 'Publica Estadual', '3': 'Publica Municipal',
                                       '4': 'Privada com fins lucrativos', '5': 'Privada sem fins lucrativos',
                                       '7': 'Especial'}

        CO_SITUACAO_DOCENTE = {'1': 'Em exercício', '2': 'Afastado para qualificação',
                               '3': 'Afastado para exercício em outros órgãos/entidades',
                               '4': 'Afastado por outros motivos', '5': 'Afastado para tratamento de saúde'}

        CO_NACIONALIDADE_DOCENTE = {
            '1': 'Brasileira',
            '2': 'Brasileira - nascido no exterior ou naturalizado',
            '3': 'Estrangeira'}

        df['CO_CATEGORIA_ADMINISTRATIVA'] = df['CO_CATEGORIA_ADMINISTRATIVA'].astype(str).replace(
            CO_CATEGORIA_ADMINISTRATIVA)
        df['CO_SITUACAO_DOCENTE'] = df['CO_SITUACAO_DOCENTE'].astype(str).replace(
            CO_SITUACAO_DOCENTE)
        df['CO_NACIONALIDADE_DOCENTE'] = df['CO_NACIONALIDADE_DOCENTE'].astype(str).replace(CO_NACIONALIDADE_DOCENTE)
        df['IN_DOCENTE_DEFICIENCIA'] = df['IN_DOCENTE_DEFICIENCIA'].astype(str).replace(DEFICIENCIA_FISICA)
        df['IN_VISITANTE_IFES_VINCULO'] = df['IN_VISITANTE_IFES_VINCULO'].replace(IN_VISITANTE_IFES_VINCULO)
        df['IN_CAPITAL_IES'] = np.where(df['IN_CAPITAL_IES'].astype(str) == '1', 'Sim', 'Não')

        for d in CHAVES_SIM_NAO:
            df[d] = df[d].astype(str).replace(SIM_NAO)

        return df

    def gera_csv(self):
        df = self.resolve_dicionarios()
        destino_transform = BASE_PATH_DATA + 'inep/' + str(self.ano) + '/transform/docentes'
        csv_file = '/docentes_vinculo_ies_' + str(self.ano) + '.csv'
        log_file = '/docentes_vinculo_ies_' + str(self.ano) + '.log'
        try:
            os.makedirs(destino_transform)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        print 'gerando arquivo csv'
        df.to_csv(destino_transform + csv_file, sep=';', chunksize=1000000, index=False, encoding='utf8',
                  quoting=csv.QUOTE_ALL)
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


def inep_docentes_tranform():
    PATH_ORIGEM = BASE_PATH_DATA + 'inep/'
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
            print('\n')
        except:
            print('Arquivo do ano, {} não encontrado'.format(ano))
            raise
    print('Fim!!')
    print('\n')

# if __name__ == "__main__":
#
#     PATH_ORIGEM = '/var/tmp/solr_front/collections/inep/'
#     try:
#         anos = os.listdir(PATH_ORIGEM)
#         anos.sort()
#     except OSError:
#         print('Nenhuma pasta encontrada')
#         raise
#     for ano in anos:
#         print(ano)
#         try:
#             inep_doc = inepVincDocentes(ano)
#             inep_doc.gera_csv()
#             print('Arquivo do ano, {} finalizado'.format(ano))
#             print('\n')
#         except:
#             print('Arquivo do ano, {} não encontrado'.format(ano))
#             pass
#     print('Fim!!')
#     print('\n')
