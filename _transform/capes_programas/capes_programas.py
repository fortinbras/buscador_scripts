# -*- coding: utf-8 -*-
import errno
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from utils.utils import *
import pandas as pd
import codecs
import csv
import commands
from datetime import datetime
# Imports para acrescentar ao programas o cadastro das CAPES
#from dicionarios.cod_gei import cod_gei_dic
#from dicionarios.cod_mantenedora import cod_mantenedora_dic
#from dicionarios.cod_oorgani_acad_gei import cod_org_acad_gei_dic
#from dicionarios.cod_tipo_institu import cod_tipo_institu_dic
#from dicionarios.nat_juridica_gei import nat_jurudica_gei_dic


class CapesProgramas(object):

    def __init__(self, arquivo, nome_arquivo):

        self.date = datetime.now()
        self.arquivos = arquivo
        self.nome_arquivo = nome_arquivo
        self.input_lenght = 0
        self.output_length = 0
        self.ies = self.pega_arquivo_cadastro_ies_capes()
        self.colunas = [
            'AN_BASE',
            'ID_PESSOA',
            'NM_DISCENTE',
            'TP_DOCUMENTO_DISCENTE',
            'NR_DOCUMENTO_DISCENTE',
            'SituacaoDiscente',
            'IngressanteAno',
            'GrauAcademico',
            'DT_SITUACAO_DISCENTE',
            'Ano_SITUACAO_DISCENTE',
            'DT_MATRICULA_DISCENTE',
            'Ano_SITUACAO_MATRICULA',
            'DT_TITULACAO',
            'QT_MES_TITULACAO',
            'Casos_excluidos_GeoCapes',
            'Genero',
            'Idade',
            'DS_TIPO_NACIONALIDADE_DISCENTE',
            'NM_PAIS_NACIONALIDADE_DISCENTE',
            'NM_INST_FapespGei',
            'SG_ENTIDADE_ENSINO',
            'NM_ENTIDADE_ENSINO',
            'cat_insti',
            'CS_STATUS_JURIDICO',
            'DS_DEPENDENCIA_ADMINISTRATIVA',
            'CS_Natureza_Juridica',
            'DS_ORGANIZACAO_ACADEMICA_Fapesp',
            'NM_REGIAO',
            'SG_UF_PROGRAMA',
            'NM_MUNICIPIO_PROGRAMA_IES',
            'CD_PROGRAMA_IES',
            'NM_PROGRAMA_IES',
            'NM_GRANDE_AREA_CONHECIMENTO',
            'NM_AREA_CONHECIMENTO',
            'NM_AREA_BASICA',
            'NM_SUBAREA_CONHECIMENTO',
            'NM_ESPECIALIDADE',
            'CD_AREA_AVALIACAO',
            'NM_AREA_AVALIACAO',
            'CD_CONCEITO_PROGRAMA',
            'CD_CONCEITO_CURSO',
            'NM_MODALIDADE_PROGRAMA',
            'NM_GRAU_PROGRAMA',
            'IN_REDE',
            'DS_SITUACAO_PROGRAMA',
            'DT_SITUACAO_PROGRAMA',
            'NM_TESE_DISSERTACAO',
            'NM_ORIENTADOR',
            'ID_ADD_FOTO_PROGRAMA',
            'ID_ADD_FOTO_PROGRAMA_IES'

        ]

    def pega_arquivo_nome(self):

        var = '/var/tmp/solr_front/collections/capes/programas/download/'
        #df_auxiliar = []
        for root, dirs, files in os.walk(var):
            for file in files:
                if file in self.arquivos:
                    print file
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                    self.input_lenght += int(commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l ')[1])
                    print 'Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1)
                    #df_auxiliar.append(pd.read_csv(arquivo, sep=';', low_memory=False, encoding='cp1252'))
                    df_auxiliar = pd.read_csv(arquivo, sep=';', low_memory=False, encoding='latin-1')
                    #df_auxiliar = pd.read_csv(arquivo, sep=';', nrows=1000, chunksize=500, encoding='latin-1', low_memory=False)
                    #df_enade = pd.read_csv(arquivo, sep=';', low_memory=False)
                    #df_enade = df_enade.loc[:, self.colunas]
        #import pdb;pdb.set_trace()  #para testar o código
        #df_concat = pd.concat(df_auxiliar)

        return df_auxiliar # retorna um (pandas.io.parsers.TextFileReader)

    def pega_arquivo_cadastro_ies_capes(self):
        var = '/var/tmp/solr_front/collections/capes/programas/cadastro/'
        for root, dirs, files in os.walk(var):
            for file in files:
                arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                df_cad_temp = pd.read_csv(arquivo, sep=';', low_memory=False, encoding='latin-1')
        # eliminando as colunas vazias do csv.
        df_cad = df_cad_temp.dropna(how = 'all', axis = 'columns')
        df_cad = df_cad.dropna(how = 'all', axis = 'rows')

        return df_cad

    def merge_programas(self, df):
        ''' Colunas que serão agregadas à capes programas, segundo o modelo(excel). Esta função
            recebe um dataframe de parametro e faz o merge dele com os arquivos
            do CAPES Programas.'''

        print 'Fazendo o merge......'
        #df_merged = df.merge(self.ies, how='left')
        df_merged = df.merge(self.ies, on=['SG_ENTIDADE_ENSINO_Capes'])
        #df_merged = df.merge(self.ies, how='left')
        #df_merge = df_merged.loc(colunas_adicionadas)
        #return df_merged[colunas_adicionadas]

        return df_merged



    def resolve_dicionarios(self):

        df = self.pega_arquivo_nome()
        df['SG_ENTIDADE_ENSINO_Capes'] = df['SG_ENTIDADE_ENSINO']

        df = self.merge_programas(df)
        df.columns = df.columns.str.replace(' ', '_')

        parse_dates = ['DT_SITUACAO_PROGRAMA']

        for dt in parse_dates:
            df[dt] = pd.to_datetime(df[dt], infer_datetime_format=False, format='%d%b%Y:%H:%M:%S', errors='coerce')

        # df['ANO_MATRICULA_facet'] = df[df['DT_MATRICULA'].notnull()]['DT_MATRICULA'].dt.year.apply(gYear)
        #df['DT_SITUACAO_PROGRAMA'] = df[df['DT_SITUACAO_PROGRAMA'].dt.year == '2013']['DT_SITUACAO_PROGRAMA'].dt.year.apply(gYear)
        df['AN_BASE_facet'] = df['AN_BASE'].apply(gYear)
        df['NM_REGIAO_facet'] = df['NM_REGIAO'] + '|' + df['SG_UF_PROGRAMA'] + '|' + df['NM_MUNICIPIO_PROGRAMA_IES']
        df['AREA_CONHECIMENTO_facet'] = df['NM_GRANDE_AREA_CONHECIMENTO'] + '|' + df['NM_AREA_CONHECIMENTO'] + '|' + df['NM_SUBAREA_CONHECIMENTO']
        df['ANO_INICIO_PROGRAMA_facet'] = df['ANO_INICIO_PROGRAMA'].apply(gYear)

        df['DT_SITUACAO_PROGRAMA'] = df[dt].dt.strftime('%Y%m%d')
        df['DT_SITUACAO_PROGRAMA'] = df['DT_SITUACAO_PROGRAMA'].astype(str)
        df['DT_SITUACAO_PROGRAMA_facet'] = df['DT_SITUACAO_PROGRAMA'].apply(data_facet)
        df['INSTITUICAO_ENSINO_facet'] =  df['SG_ENTIDADE_ENSINO'] + '|' + df['NM_ENTIDADE_ENSINO']

        df['NM_PROGRAMA_IES_exact'] = df['NM_PROGRAMA_IES']
        df['NM_PROGRAMA_IDIOMA_exact'] = df['NM_PROGRAMA_IDIOMA']
        
        df['Codigo_GEI'] = df['Codigo_GEI'].astype(str)
        df['Codigo_do_Tipo_de_Instituicao_'] = df['Codigo_do_Tipo_de_Instituicao_'].astype(int)
        df['Codigo_Natureza_Juridica_-_GEI'] = df['Codigo_Natureza_Juridica_-_GEI'].astype(int)
        df['CD_ORGANIZACAO_ACADEMICA_-_GEI'] = df['CD_ORGANIZACAO_ACADEMICA_-_GEI'].astype(int)
        df['Codigo_Mantenedora'] = df['Codigo_Mantenedora'].astype(int)


        import pdb; pdb.set_trace()
        return df

    def gera_csv(self):

        df_capes = self.resolve_dicionarios()

        destino_transform = '/var/tmp/solr_front/collections/capes/programas/transform'
        csv_file = '/capes_programas_' + self.nome_arquivo + '.csv'
        log_file = '/capes_programas_' + self.nome_arquivo + '.log'

        try:
            os.makedirs(destino_transform)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        df_capes.to_csv(destino_transform + csv_file, sep=';', index=False, encoding='utf8') #'line_terminator='\n', quoting=csv.QUOTE_ALL)
        self.output_length = commands.getstatusoutput('cat ' + destino_transform + csv_file + ' |wc -l')[1]
        print 'Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1)

        with open(destino_transform + log_file, 'w') as log:
            log.write('Log gerado em {}'.format(self.date.strftime("%Y-%m-%d %H:%M")))
            log.write("\n")
            log.write('Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1))
            log.write("\n")
            log.write('Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1))
        print('Processamento CAPES PROGRAMAS {} finalizado, arquivo de log gerado em {}'.format(self.nome_arquivo, (destino_transform + log_file)))

def capes_programas_transform():

    PATH_ORIGEM = '/var/tmp/solr_front/collections/capes/programas/download'
    try:
        arquivos = os.listdir(PATH_ORIGEM)
        arquivos.sort()
        # tamanho_arquivo = len(arquivos) - 1
        # arquivo_inicial = arquivos[0].split('.')[0]
        # arquivo_final = arquivos[tamanho_arquivo].split('.')[0]
        # nome_arquivo = arquivo_inicial +'_a_'+ arquivo_final
        for arquivo in arquivos:
            nome_arquivo = arquivo.split('.')[0]
            capes_doc = CapesProgramas(arquivo, nome_arquivo)
            capes_doc.gera_csv()
        print('Arquivo {} finalizado!'.format(arquivo))

    except OSError:
        print('Nenhum arquivo encontrado')
        raise
