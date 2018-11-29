# -*- coding: utf-8 -*-
import errno
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from settings import BASE_PATH_DATA
from utils.utils import *
import pandas as pd
import codecs
import csv
import commands
import datetime

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)


class CapesDiscentes(object):

    def __init__(self, arquivos, nome_arquivo):

        self.date = datetime.datetime.now()
        self.arquivos = arquivos
        self.nome_arquivo = nome_arquivo
        self.input_lenght = 0
        self.output_length = 0
        self.ies = self.pega_arquivo_programas_download()
        self.cadastro = self.pega_arquivo_cadastro_ies_capes()
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
        ''' Pega os arquivos em discentes/download em Discentes, faz um append deles e os retorna'''

        var = BASE_PATH_DATA + 'capes/discentes/download/'
        df_auxiliar = []

        print 'Lendo os arquivos CAPES Discentes......'
        for root, dirs, files in os.walk(var):
            for file in files:
                if file in self.arquivos:
                    print file
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                    self.input_lenght += int(commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l ')[1])
                    print 'Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1)
                    df_auxiliar.append(pd.read_csv(arquivo, sep=';', low_memory=False, encoding='cp1252'))
                    #df_auxiliar = pd.read_csv(arquivo, sep=';', nrows=10000, chunksize=1000, encoding='cp1252', low_memory=False)

        df_discentes_concat = pd.concat(df_auxiliar, sort=False)

        return df_discentes_concat # retornando todos os anos 2013_2015 a 2016_2017


    def pega_arquivo_cadastro_ies_capes(self):
        '''pega os arquivos de cadastro CAPES IES que serão agregados aos Discentes'''

        var = '/var/tmp/solr_front/collections/capes/programas/cadastro/'
        for root, dirs, files in os.walk(var):
            for file in files:
                arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                df_cad_temp = pd.read_csv(arquivo, sep=';', low_memory=False, encoding='latin-1')
        # eliminando as colunas vazias do csv.
        df_cad = df_cad_temp.dropna(how = 'all', axis = 'columns')
        df_cad = df_cad.dropna(how = 'all', axis = 'rows')

        return df_cad


    def pega_arquivo_programas_download(self):
        '''Pega os arquivos do diretorio capes/programas, faz um append deles e os retorna'''

        var = BASE_PATH_DATA + 'capes/programas/download/'
        df_auxiliar = []
        print 'Lendo os arquivos do CAPES programas....'
        for root, dirs, files in os.walk(var):

            for file in files:
                print file
                arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                self.input_lenght += int(commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l ')[1])
                print 'Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1)
                df_auxiliar.append(pd.read_csv(arquivo, sep=';', low_memory=False, encoding='cp1252'))
                #df_auxiliar = pd.read_csv(arquivo, sep=';', nrows=10000, chunksize=1000, encoding='cp1252', low_memory=False)

        df_programas_concat = pd.concat(df_auxiliar, sort=False)

        return df_programas_concat

    def merge_programas(self, df):
        ''' Colunas que serão agregadas aos Discentes, segundo o modelo. Esta função
            recebe um dataframe de parametro e faz o merge dele com os arquivos
            do CAPES Programas.'''

        colunas_adicionadas = [

            u'AN_BASE',
            u'NM_GRANDE_AREA_CONHECIMENTO',
            u'NM_AREA_CONHECIMENTO',
            u'NM_AREA_BASICA',
            u'NM_SUBAREA_CONHECIMENTO',
            u'NM_ESPECIALIDADE',
            u'CD_AREA_AVALIACAO',
            u'NM_AREA_AVALIACAO',
            u'SG_ENTIDADE_ENSINO',
            u'NM_ENTIDADE_ENSINO',
            u'CS_STATUS_JURIDICO',
            u'DS_DEPENDENCIA_ADMINISTRATIVA',
            u'DS_ORGANIZACAO_ACADEMICA',
            u'NM_REGIAO',
            u'SG_UF_PROGRAMA',
            u'NM_MUNICIPIO_PROGRAMA_IES',
            u'NM_MODALIDADE_PROGRAMA',
            u'CD_PROGRAMA_IES',
            u'NM_PROGRAMA_IES',
            u'NM_PROGRAMA_IDIOMA',
            u'NM_GRAU_PROGRAMA',
            u'CD_CONCEITO_PROGRAMA',
            u'ANO_INICIO_PROGRAMA',
            u'AN_INICIO_CURSO',
            u'IN_REDE',
            u'SG_ENTIDADE_ENSINO_REDE',
            u'DS_SITUACAO_PROGRAMA',
            u'DT_SITUACAO_PROGRAMA',
            u'ID_ADD_FOTO_PROGRAMA_IES',
            u'ID_ADD_FOTO_PROGRAMA'

        ]
        print 'Fazendo o merge......'
        df_merged = df.merge(self.ies, on=['AN_BASE', 'CD_PROGRAMA_IES'])
        #df_merged = df.merge(self.ies, how='left')
        #df_merge = df_merged.loc(colunas_adicionadas)
        #return df_merged[colunas_adicionadas]

        return df_merged


    def resolve_dicionarios(self):

        df = self.pega_arquivo_nome()
        df = self.merge_programas(df)

        df['SG_ENTIDADE_ENSINO_Capes'] = df['SG_ENTIDADE_ENSINO_x']
        import pdb; pdb.set_trace()
        df = df.merge(self.cadastro, on=['SG_ENTIDADE_ENSINO_Capes'])
        import pdb; pdb.set_trace()
        #print df[u'DT_SITUACAO_PROGRAMA'][0]
        parse_dates = ['DT_SITUACAO_PROGRAMA', 'DT_MATRICULA_DISCENTE', 'DT_SITUACAO_DISCENTE' ]

        for dt in parse_dates:
            df[dt] = pd.to_datetime(df[dt], infer_datetime_format=False, format='%d%b%Y:%H:%M:%S', errors='coerce')

        df['AN_INICIO_CURSO'] = df['AN_INICIO_CURSO'].astype(str)
        #df['ANO_INICIO_PROGRAMA'] = df[df['ANO_INICIO_PROGRAMA'].notnull()]['ANO_INICIO_PROGRAMA'].astype(str)

        #df['ANO_MATRICULA_facet'] = df[df['DT_MATRICULA'].notnull()]['DT_MATRICULA'].dt.year.apply(gYear)
        #df['DT_SITUACAO_PROGRAMA'] = df[df['DT_SITUACAO_PROGRAMA'].dt.year == '2013']['DT_SITUACAO_PROGRAMA'].dt.year.apply(gYear)

        # Criação dos campos facets
        df['AN_BASE_facet'] = df['AN_BASE'].apply(gYear)
        df['NM_REGIAO_facet'] = df['NM_REGIAO_x'] + '|' + df['SG_UF_PROGRAMA_x'] + '|' + df['NM_MUNICIPIO_PROGRAMA_IES_x']
        df['AREA_CONHECIMENTO_facet'] = df['NM_GRANDE_AREA_CONHECIMENTO_x'] + '|' + df['NM_AREA_CONHECIMENTO'] + '|' + df['NM_SUBAREA_CONHECIMENTO']
        #df['NM_SUBAREA_CONHECIMENTO_facet'] = df['AREA_CONHECIMENTO_facet'] + '|' + df['NM_SUBAREA_CONHECIMENTO']
        #df['DT_SITUACAO_PROGRAMA_facet'] = df['DT_SITUACAO_PROGRAMA'].dt.year.apply(gYear)
        df['ANO_INICIO_PROGRAMA_facet'] = df['ANO_INICIO_PROGRAMA'].apply(gYear)
        #df['AN_INICIO_CURSO_facet'] = df['AN_INICIO_CURSO'].apply(gYear)

        df['DT_SITUACAO_PROGRAMA'] = df[dt].dt.strftime('%Y%m%d')
        df['DT_SITUACAO_PROGRAMA'] = df['DT_SITUACAO_PROGRAMA'].astype(str)
        df['DT_SITUACAO_PROGRAMA_facet'] = df['DT_SITUACAO_PROGRAMA'].apply(data_facet)
        df['INSTITUICAO_ENSINO_facet'] =  df['SG_ENTIDADE_ENSINO_x'] + '|' + df['NM_ENTIDADE_ENSINO_x']

        df['NM_PROGRAMA_IES_exact'] = df['NM_PROGRAMA_IES_x']
        df['NM_PROGRAMA_IDIOMA_exact'] = df['NM_PROGRAMA_IDIOMA']
        df[u'NM_TESE_DISSERTACAO_exact'] = df[u'NM_TESE_DISSERTACAO'].apply(norm_keyword)

        import pdb; pdb.set_trace()
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
