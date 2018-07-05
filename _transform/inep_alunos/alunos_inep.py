# coding=utf-8
import sys
import os

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from utils import *
import pandas as pd
import numpy as np
import errno
import codecs
import shutil
import csv
import commands
import datetime


class InepVincAlunos(object):

    def __init__(self, ano):
        self.ano = ano
        self.date = datetime.datetime.now()
        self.input_lenght = 0
        self.output_length = 0
        self.destino_transform = '/var/tmp/inep/' + str(self.ano) + '/transform/alunos'
        self.log_file = '/alunos_vinculo_ies_' + str(self.ano) + '.log'
        self.csv_file = '/alunos_vinculo_ies_' + str(self.ano) + '.csv'

    def pega_arquivo_aluno_por_ano(self):
        """ Para cada ano solicitado, retorna dict com o csv de docentes e csv de ies. """
        var = '/var/tmp/inep/' + str(self.ano) + '/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".CSV"):
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')

                    if file == 'DM_ALUNO.CSV':
                        self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l')[1]
                        print 'Arquivo de entrada possui {} linhas'.format(int(self.input_lenght) - 1)
                        df_alunos = pd.read_csv(arquivo, sep='|', encoding='cp1252',
                                                chunksize=500000, low_memory=False, engine='c')
        try:
            return df_alunos
        except:
            pass

    def pega_arquivo_ies_por_ano(self):
        """ Para cada ano solicitado, retorna dict com o csv de docentes e csv de ies. """
        var = '/var/tmp/inep/' + str(self.ano) + '/_download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".CSV"):
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')

                    if file == 'DM_IES.CSV':
                        df_ies = pd.read_csv(arquivo, sep='|', encoding='cp1252', low_memory=False, engine='c')

        try:
            return df_ies
        except:
            pass

    def merge_alunos_ies(self, df_a, df_i):

        colunas = [u'CO_IES', u'NO_IES', u'DS_CATEGORIA_ADMINISTRATIVA', u'DS_ORGANIZACAO_ACADEMICA',
                   u'NO_CURSO', u'CO_CURSO_POLO',
                   u'CO_TURNO_ALUNO', u'CO_GRAU_ACADEMICO', u'CO_MODALIDADE_ENSINO',
                   u'CO_NIVEL_ACADEMICO', u'CO_ALUNO_CURSO', u'CO_ALUNO',
                   u'DS_COR_RACA_ALUNO', u'DS_SEXO_ALUNO', u'NU_ANO_ALUNO_NASC', u'NU_MES_ALUNO_NASC',
                   u'NU_DIA_ALUNO_NASC', u'NU_IDADE_ALUNO', u'CO_NACIONALIDADE_ALUNO',
                   u'CO_UF_NASCIMENTO', u'CO_MUNICIPIO_NASCIMENTO',
                   u'IN_DEF_AUDITIVA', u'IN_DEF_FISICA', u'IN_DEF_INTELECTUAL',
                   u'IN_DEF_MULTIPLA', u'IN_DEF_SURDEZ', u'IN_DEF_SURDOCEGUEIRA',
                   u'IN_DEF_BAIXA_VISAO', u'IN_DEF_CEGUEIRA', u'CO_ALUNO_SITUACAO',
                   u'DT_INGRESSO_CURSO', u'IN_ING_VESTIBULAR', u'IN_ING_ENEM',
                   u'IN_ING_CONVENIO_PECG', u'IN_RESERVA_VAGAS', u'IN_RESERVA_ETNICO',
                   u'IN_RESERVA_DEFICIENCIA', u'IN_RESERVA_ENSINO_PUBLICO', u'IN_RESERVA_RENDA_FAMILIAR',
                   u'IN_FINANC_ESTUDANTIL', u'IN_FIN_REEMB_FIES', u'IN_FIN_REEMB_ESTADUAL',
                   u'IN_FIN_REEMB_MUNICIPAL', u'IN_FIN_REEMB_PROG_IES', u'IN_FIN_REEMB_ENT_EXTERNA',
                   u'IN_FIN_NAOREEMB_PROUNI_INTEGR', u'IN_FIN_NAOREEMB_PROUNI_PARCIAL',
                   u'IN_FIN_NAOREEMB_ESTADUAL', u'IN_FIN_NAOREEMB_MUNICIPAL', u'IN_FIN_NAOREEMB_PROG_IES',
                   u'IN_FIN_NAOREEMB_ENT_EXTERNA', u'IN_APOIO_SOCIAL',
                   u'IN_APOIO_ALIMENTACAO', u'IN_APOIO_BOLSA_PERMANENCIA', u'IN_APOIO_BOLSA_TRABALHO',
                   u'IN_APOIO_MATERIAL_DIDATICO', u'IN_APOIO_MORADIA', u'IN_APOIO_TRANSPORTE',
                   u'IN_COMPL_ESTAGIO', u'IN_COMPL_EXTENSAO', u'IN_COMPL_MONITORIA',
                   u'IN_COMPL_PESQUISA', u'IN_BOLSA_ESTAGIO', u'IN_BOLSA_EXTENSAO',
                   u'IN_BOLSA_MONITORIA', u'IN_BOLSA_PESQUISA', u'IN_MATRICULA',
                   u'IN_CONCLUINTE', u'ANO_INGRESSO',
                   u'NO_MANTENEDORA', u'CO_MUNICIPIO_IES', u'NO_MUNICIPIO_IES',
                   u'CO_UF_IES', u'SGL_UF_IES', u'NO_REGIAO_IES',
                   u'IN_CAPITAL_IES', u'QT_TEC_TOTAL', u'QT_TEC_FUND_INCOMP_FEM',
                   u'QT_TEC_FUND_INCOMP_MASC', u'QT_TEC_FUND_COMP_FEM', u'QT_TEC_FUND_COMP_MASC',
                   u'QT_TEC_MEDIO_FEM', u'QT_TEC_MEDIO_MASC', u'QT_TEC_SUPERIOR_FEM',
                   u'QT_TEC_SUPERIOR_MASC', u'QT_TEC_ESPECIALIZACAO_FEM', u'QT_TEC_ESPECIALIZACAO_MASC',
                   u'QT_TEC_MESTRADO_FEM', u'QT_TEC_MESTRADO_MASC', u'QT_TEC_DOUTORADO_FEM',
                   u'QT_TEC_DOUTORADO_MASC', u'IN_ACESSO_PORTAL_CAPES', u'IN_ACESSO_OUTRAS_BASES',
                   u'IN_REFERENTE', u'VL_RECEITA_PROPRIA', u'VL_TRANSFERENCIA',
                   u'VL_OUTRA_RECEITA', u'VL_DES_PESSOAL_REM_DOCENTE', u'VL_DES_PESSOAL_REM_TECNICO',
                   u'VL_DES_PESSOAL_ENCARGO', u'VL_DES_CUSTEIO', u'VL_DES_INVESTIMENTO',
                   u'VL_DES_PESQUISA', u'VL_DES_OUTRAS']

        df_merged = df_a.merge(df_i, how='left')
        return df_merged[colunas]

    def resolve_dicionarios(self, df):

        CHAVES_SIM_NAO = ['IN_ING_VESTIBULAR',
                          'IN_ING_ENEM',
                          'IN_ING_CONVENIO_PECG',
                          'IN_RESERVA_VAGAS',
                          'IN_RESERVA_ETNICO',
                          'IN_RESERVA_DEFICIENCIA',
                          'IN_RESERVA_ENSINO_PUBLICO',
                          'IN_RESERVA_RENDA_FAMILIAR',
                          'IN_FINANC_ESTUDANTIL',
                          'IN_FIN_REEMB_FIES',
                          'IN_FIN_REEMB_ESTADUAL',
                          'IN_FIN_REEMB_MUNICIPAL',
                          'IN_FIN_REEMB_PROG_IES',
                          'IN_FIN_REEMB_ENT_EXTERNA',
                          'IN_FIN_NAOREEMB_PROUNI_INTEGR',
                          'IN_FIN_NAOREEMB_PROUNI_PARCIAL',
                          'IN_FIN_NAOREEMB_ESTADUAL',
                          'IN_FIN_NAOREEMB_MUNICIPAL',
                          'IN_FIN_NAOREEMB_PROG_IES',
                          'IN_FIN_NAOREEMB_ENT_EXTERNA',
                          'IN_APOIO_SOCIAL',
                          'IN_APOIO_ALIMENTACAO',
                          'IN_APOIO_BOLSA_PERMANENCIA',
                          'IN_APOIO_BOLSA_TRABALHO',
                          'IN_APOIO_MATERIAL_DIDATICO',
                          'IN_APOIO_MORADIA',
                          'IN_APOIO_TRANSPORTE',
                          'IN_COMPL_ESTAGIO',
                          'IN_COMPL_EXTENSAO',
                          'IN_COMPL_MONITORIA',
                          'IN_COMPL_PESQUISA',
                          'IN_BOLSA_ESTAGIO',
                          'IN_BOLSA_EXTENSAO',
                          'IN_BOLSA_MONITORIA',
                          'IN_BOLSA_PESQUISA',
                          'IN_ACESSO_PORTAL_CAPES', 'IN_ACESSO_OUTRAS_BASES']

        SIM_NAO = {'0': 'Não', '0.0': 'Não', '1': 'Sim', '1.0': 'Sim', 'nan': 'Não Informado'}
        DEFICIENCIA = ['IN_DEF_AUDITIVA', 'IN_DEF_FISICA', 'IN_DEF_INTELECTUAL',
                       'IN_DEF_MULTIPLA', 'IN_DEF_SURDEZ',
                       'IN_DEF_SURDOCEGUEIRA', 'IN_DEF_BAIXA_VISAO', 'IN_DEF_CEGUEIRA']
        DEFICIENCIA_FISICA = {'0': 'Não', '1': 'Sim', '2': 'Não dispõe de informação',
                              'nan': 'Não'}

        CO_NACIONALIDADE_ALUNO = {
            '1': 'Brasileira',
            '2': 'Brasileira - nascido no exterior ou naturalizado',
            '3': 'Estrangeira'}

        CO_TURNO_ALUNO = {
            1: 'Matutino',
            2: 'Vespertino',
            3: 'Noturno',
            4: 'Integral', }

        CO_GRAU_ACADEMICO = {
            1: 'Bacharelado',
            2: 'Licenciatura',
            3: 'Tecnológico'}

        CO_MODALIDADE_ENSINO = {
            1: 'Presencial',
            2: 'Curso a distância'
        }

        CO_NIVEL_ACADEMICO = {
            1: 'Graduação',
            2: 'Seqüencial de Formação Específica'}
        IN_REFERENTE = {
            1: 'Mantenedora',
            2: 'Instituicao'}

        for d in DEFICIENCIA:
            df[d] = df[d].astype(str).replace(DEFICIENCIA_FISICA)

        for sn in CHAVES_SIM_NAO:
            df[sn] = df[sn].astype(str).replace(SIM_NAO)

        municipios = pd.read_csv('lista_municipios.csv', sep=';')
        municipios['CÓDIGO DO MUNICÍPIO'] = municipios['CÓDIGO DO MUNICÍPIO'].astype(str)
        municipios['Regiao'] = municipios['CÓDIGO DO MUNICÍPIO'].apply(utils.find_regiao)
        municipios.rename(columns={'CÓDIGO DO MUNICÍPIO': 'CO_MUNICIPIO_NASCIMENTO'}, inplace=True)
        municipios['CO_MUNICIPIO_NASCIMENTO'] = municipios['CO_MUNICIPIO_NASCIMENTO'].astype(float)

        df[['MUNICIPIO_NASCIMENTO', 'UF_NASCIMENTO', 'REG_NASCIMENTO']] = pd.merge(df, municipios,
                                                                                   how='left', on=[
                'CO_MUNICIPIO_NASCIMENTO']).loc[:, ['NOME DO MUNICÍPIO', 'UF', 'Regiao']]
        df['CO_NACIONALIDADE_ALUNO'] = df['CO_NACIONALIDADE_ALUNO'].astype(str).replace(CO_NACIONALIDADE_ALUNO)
        df['CO_TURNO_ALUNO'] = df['CO_TURNO_ALUNO'].replace(CO_TURNO_ALUNO)
        df['CO_GRAU_ACADEMICO'] = df['CO_GRAU_ACADEMICO'].replace(CO_GRAU_ACADEMICO)
        df['CO_MODALIDADE_ENSINO'] = df['CO_MODALIDADE_ENSINO'].replace(CO_MODALIDADE_ENSINO)
        df['CO_NIVEL_ACADEMICO'] = df['CO_NIVEL_ACADEMICO'].replace(CO_NIVEL_ACADEMICO)
        df['IN_REFERENTE'] = df['IN_REFERENTE'].replace(IN_REFERENTE)

        df['GEOGRAFICO_ALUNO_NASC_facet'] = df['REG_NASCIMENTO'] + '|' + df[
            'UF_NASCIMENTO'] + '|' + df['MUNICIPIO_NASCIMENTO']
        df['GEOGRAFICO_IES_facet'] = df['NO_REGIAO_IES'] + '|' + df['SGL_UF_IES'] + '|' + df['NO_MUNICIPIO_IES']
        df['ANO_facet'] = gYear(self.ano)
        df['IN_CAPITAL_IES'] = np.where(df['IN_CAPITAL_IES'].astype(str) == '1', 'Sim', 'Não')
        df['Data_Nasc_Aluno_facet'] = df['NU_ANO_ALUNO_NASC'].astype(str) + '|' + df['NU_MES_ALUNO_NASC'].astype(
            str) + '|' + df['NU_DIA_ALUNO_NASC'].astype(str)

        return df

    def gera_csv(self, df, control):

        if os.path.join(self.destino_transform, self.csv_file) and control == 0:
            shutil.rmtree(os.path.join(self.destino_transform), ignore_errors=True, onerror=None)

        try:
            os.makedirs(self.destino_transform)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        if control == 1:

            df.to_csv(self.destino_transform + self.csv_file, sep=';', index=False, encoding='utf8', header=0, mode='a',
                      quoting=csv.QUOTE_ALL, chunksize=500000)
        else:
            df.to_csv(self.destino_transform + self.csv_file, sep=';', index=False, encoding='utf8', mode='a',
                      quoting=csv.QUOTE_ALL, chunksize=500000)

def inep_alunos_transform():
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
            inep_al = InepVincAlunos(ano)
            df_ies = inep_al.pega_arquivo_ies_por_ano()
            chunks_a = inep_al.pega_arquivo_aluno_por_ano()
            df_next = next(chunks_a)
            df_merged = inep_al.merge_alunos_ies(df_next, df_ies)
            # df_merged = inep_al.manipula_df(df_merged)
            df_merged = inep_al.resolve_dicionarios(df_merged)
            inep_al.gera_csv(df_merged, 0)
            for chunk in chunks_a:
                df_merged = inep_al.merge_alunos_ies(chunk, df_ies)
                # df_merged = inep_al.manipula_df(df_merged)
                df_merged = inep_al.resolve_dicionarios(df_merged)
                inep_al.gera_csv(df_merged, 1)

            output_length = commands.getstatusoutput('cat ' + inep_al.destino_transform + inep_al.csv_file + ' |wc -l')[
                1]
            print 'Arquivo de saida possui {} linhas de informacao'.format(int(output_length) - 1)

            with open(inep_al.destino_transform + inep_al.log_file, 'w') as log:
                log.write('Log gerado em {}'.format(inep_al.date.strftime("%Y-%m-%d %H:%M")))
                log.write("\n")
                log.write('Arquivo de entrada possui {} linhas de informacao'.format(int(inep_al.input_lenght) - 1))
                log.write("\n")
                log.write('Arquivo de saida possui {} linhas de informacao'.format(int(output_length) - 1))
            print('Processamento ENADE {} finalizado, arquivo de log gerado em {}'.format(inep_al.ano,
                                                                                          inep_al.destino_transform + inep_al.log_file))
            print('Arquivo do ano, {} finalizado'.format(ano))
        except:
            print('Arquivo do ano, {} não encontrado'.format(ano))
            raise

9565484
# if __name__ == "__main__":
#     PATH_ORIGEM = '/var/tmp/inep/'
#     try:
#         anos = os.listdir(PATH_ORIGEM)
#         anos.sort()
#     except OSError:
#         print('Nenhuma pasta encontrada')
#         raise
#     for ano in anos:
#         print(ano)
#         try:
#             inep_al = InepVincAlunos(ano)
#             df_ies = inep_al.pega_arquivo_ies_por_ano()
#             chunks_a = inep_al.pega_arquivo_aluno_por_ano()
#             df_next = next(chunks_a)
#             df_merged = inep_al.merge_alunos_ies(df_next, df_ies)
#             # df_merged = inep_al.manipula_df(df_merged)
#             df_merged = inep_al.resolve_dicionarios(df_merged)
#             inep_al.gera_csv(df_merged, 0)
#             for chunk in chunks_a:
#                 df_merged = inep_al.merge_alunos_ies(chunk, df_ies)
#                 # df_merged = inep_al.manipula_df(df_merged)
#                 df_merged = inep_al.resolve_dicionarios(df_merged)
#                 inep_al.gera_csv(df_merged, 1)
#
#             output_length = commands.getstatusoutput('cat ' + inep_al.destino_transform + inep_al.csv_file + ' |wc -l')[
#                 1]
#             print 'Arquivo de saida possui {} linhas de informacao'.format(int(output_length) - 1)
#
#             with open(inep_al.destino_transform + inep_al.log_file, 'w') as log:
#                 log.write('Log gerado em {}'.format(inep_al.date.strftime("%Y-%m-%d %H:%M")))
#                 log.write("\n")
#                 log.write('Arquivo de entrada possui {} linhas de informacao'.format(int(inep_al.input_lenght) - 1))
#                 log.write("\n")
#                 log.write('Arquivo de saida possui {} linhas de informacao'.format(int(inep_al.output_length) - 1))
#             print('Processamento ENADE {} finalizado, arquivo de log gerado em {}'.format(inep_al.ano,
#                                                                                           inep_al.destino_transform + inep_al.log_file))
#             print('Arquivo do ano, {} finalizado'.format(ano))
#         except:
#             print('Arquivo do ano, {} não encontrado'.format(ano))
#             raise
