# -*- coding: utf-8 -*-
import errno
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from settings import BASE_PATH_DATA
from utils import *
import pandas as pd
import codecs
import csv
import commands
from datetime import datetime


class CapesDiscentes(object):

    def __init__(self, arquivos, nome_arquivo):

        self.date = datetime.now()
        self.arquivos = arquivos
        self.nome_arquivo = nome_arquivo
        self.input_lenght = 0
        self.output_length = 0
        self.ies = self.pega_arquivo_ies_por_ano()
        self.colunas = [
            'AN_BASE',
            'NM_GRANDE_AREA_CONHECIMENTO',
            'CD_AREA_AVALIACAO',
            'NM_AREA_AVALIACAO',
            'SG_ENTIDADE_ENSINO',
            'NM_ENTIDADE_ENSINO',
            'CS_STATUS_JURIDO',
            'DS_DEPENDENCIA_ADMINISTRATIVA',
            'NM_MODALIDADE_PROGRAMA',
            'NM_GRAU_PROGRAMA',
            'CD_PROGRAMA_IES',
            'NM_PROGRAMA_IES',
            'NM_REGIAO',
            'SG_UF_PROGRAMA',
            'NM_MUNICIPIO_PROGRAMA_IES',
            'CD_CONCEITO_PROGRAMA',
            'CD_CONCEITO_CURSO',
            'ID_PESSOA',
            'NM_DISCENTE',
            'NM_PAIS_NASCIONALIDADE_DISCENTE',
            'DS_TIPO_NACIONALIDADE_DISCENTE',
            'TP_SEXO_DISCENTE',
            'DS_FAIXA_ETARIA',
            'DS_GRAU_ACADEMICO_DISCENTE',
            'ST_INGRESSANTE',
            'NM_SITUACAO_DISCENTE',
            'DT_MATRICULA_DISCENTE',
            'DT_SITUACAO_DISCENTE',
            'QT_MES_TITULACAO',
            'NM_TESE_DISSERTACAO',
            'NM_ORIENTADOR',
            'ID_ADD_FOTO_PROGRAMA',
            'ID_ADD_FOTO_PROGRAMA_IES',
            'NR_DOCUMENTO_DISCENTE',
            'TP_DOCUMENTO_DISCENTE',

        ]

    def pega_arquivo_nome(self):

        var = BASE_PATH_DATA + 'capes/discentes/download/'
        df_auxiliar = []
        for root, dirs, files in os.walk(var):
            for file in files:
                if file in self.arquivos:
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                    self.input_lenght += int(commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l ')[1])
                    print 'Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1)
                    #df_auxiliar.append(pd.read_csv(arquivo, sep=';', low_memory=False, encoding='cp1252'))
                    df_auxiliar = pd.read_csv(arquivo, sep=';', nrows=3000, chunksize=3000, encoding='latin-1', low_memory=False)

        # import pdb;pdb.set_trace()  #para testar o código
        df_discentes_concat = pd.concat(df_auxiliar)
        return df_discentes_concat # retornando todos os anos 2013_2015 a 2016_2017


    def pega_arquivo_programas_download(self):
        '''Pega os arquivos do diretorio capes/programas - os anos, para anexar a capes_docentes'''
        var = BASE_PATH_DATA + 'capes/programas/download/'
        df_auxiliar = []
        for root, dirs, files in os.walk(var):
            for file in files:
                if file in self.arquivos:
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                    self.input_lenght += int(
                        commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l ')[1])
                    print 'Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1)
                    df_auxiliar.append(pd.read_csv(arquivo, sep=';', low_memory=False, encoding='cp1252'))
                    #df_auxiliar = pd.read_csv(arquivo, sep=';', nrows=3000, chunksize=3000, encoding='latin-1', low_memory=False)
        #import pdb;pdb.set_trace()  #para testar o código
        df_programas_concat = pd.concat(df_auxiliar)
        return df_programas_concat

    def merge_programas(self, df_p):
        ''' Colunas que serão agregadas aos dicentes, segundo o modelo '''
        colunas_adicionadas = [
            u'AN_BASE',
            u'CD_PROGRAMA_IES',
            u'NM_AREA_CONHECIMENTO',
            u'NM_SUBAREA_CONHECIMENTO',
            u'NM_ESPECIALIDADE',
            u'IN_REDE',
            u'DS_SITUACAO_PROGRAMA',
            u'DT_SITUACAO_PROGRAMA'
        ]

        df_merged = df_p.merge(self.ies, how='left')
        return df_merged[colunas_adicionadas]

    def pega_arquivo_programas(self):
        """ Para cada ano solicitado, retorna dict com o csv de discentes """
        var = BASE_PATH_DATA + '/capes/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".CSV"):
                    arquivo = open(os.path.join(root, file), 'r')

                    if file == 'DM_IES.CSV':
                        df_ies = pd.read_csv(arquivo, sep='|', encoding='cp1252', low_memory=False, engine='c')

        try:
            return df_ies
        except:
            pass


    def resolve_dicionarios(self):
        df = self.pega_arquivo_nome()
        parse_dates = ['DT_SITUACAO_PROGRAMA']

        for dt in parse_dates:
            df[dt] = pd.to_datetime(df[dt], infer_datetime_format=False, format='%d%b%Y:%H:%M:%S', errors='coerce')

        df['DT_SITUACAO_PROGRAMA'] = df[dt].dt.strftime('%Y%m%d')

        # df['ANO_MATRICULA_facet'] = df[df['DT_MATRICULA'].notnull()]['DT_MATRICULA'].dt.year.apply(gYear)
        #df['DT_SITUACAO_PROGRAMA'] = df[df['DT_SITUACAO_PROGRAMA'].dt.year == '2013']['DT_SITUACAO_PROGRAMA'].dt.year.apply(gYear)

        return df


    def gera_csv(self):

        df_capes = self.resolve_dicionarios()

        destino_transform = BASE_PATH_DATA + 'capes/discentes/transform'
        csv_file = '/capes_' + self.nome_arquivo + '.csv'
        log_file = '/capes_' + self.nome_arquivo + '.log'

        try:
            os.makedirs(destino_transform)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        df_capes.to_csv(destino_transform + csv_file, sep=';', index=False, encoding='utf8',
                        line_terminator='\n', quoting=csv.QUOTE_ALL)
        self.output_length = commands.getstatusoutput('cat ' + destino_transform + csv_file + ' |wc -l')[1]
        print 'Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1)

        with open(destino_transform + log_file, 'w') as log:
            log.write('Log gerado em {}'.format(self.date.strftime("%Y-%m-%d %H:%M")))
            log.write("\n")
            log.write('Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1))
            log.write("\n")
            log.write('Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1))
        print('Processamento CAPES {} finalizado, arquivo de log gerado em {}'.format(self.nome_arquivo,
                                                                                      (destino_transform + log_file)))


def capes_discentes_transform():
    PATH_ORIGEM = BASE_PATH_DATA + 'capes/discentes/download'
    try:
        arquivos = os.listdir(PATH_ORIGEM)
        arquivos.sort()
        arquivo_inicial = arquivos[0]
        nome_arquivo = arquivo_inicial.split('_')[0]
        capes_doc = CapesDiscentes(arquivos, nome_arquivo)
        capes_doc.gera_csv()
        print('Arquivo {} finalizado!'.format(nome_arquivo))

    except OSError:
        print('Nenhum arquivo encontrado')
        raise
