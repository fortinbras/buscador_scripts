# coding=utf8
import pandas as pd
import os
from settings import BASE_PATH_DATA
import csv
import commands
import datetime
import errno
import re
from utils import gYear


# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
def norm_keyword(palavras):
    if not isinstance(palavras, (unicode, str)):
        return palavras
    palavras = palavras.encode('utf8')
    palavras = re.sub(r'\d.', '', palavras)
    palavras = palavras.replace(';', ',').replace('.', ',').replace('¿', 'E').replace('[', '').replace(']', '')
    return palavras.split(',')


class CapesTeses(object):
    def __init__(self, year):
        self.date = datetime.datetime.now()
        self.ano = year
        self.input_lenght = 0
        self.output_length = 0

    def pega_arquivo_ano(self):
        var = BASE_PATH_DATA + 'capes_teses/' + str(self.ano) + '/download/'
        exclude_prefixes = ('__', '.')
        for root, dirs, files in os.walk(var, topdown=True):
            dirs[:] = [dirname for dirname in dirs if not dirname.startswith(exclude_prefixes)]
            for f in files:
                if f.endswith('.csv'):
                    arquivo = open(os.path.join(root, f), 'r')
                    self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, f) + ' |wc -l')[1]
                    print 'Arquivo {} de entrada possui {} linhas de informacao'.format(f, int(self.input_lenght) - 1)
                    df = pd.read_csv(arquivo, sep=';', low_memory=False, engine='c', encoding='latin1', )

                    return df

    def resolve_dicionarios(self):
        df = self.pega_arquivo_ano()
        parse_dates = ['DT_MATRICULA', 'DH_INICIO_AREA_CONC', 'DH_FIM_AREA_CONC',
                       'DH_INICIO_LINHA', 'DH_FIM_LINHA', 'DT_TITULACAO']

        for dt in parse_dates:
            if self.ano == '2017':
                df[dt] = pd.to_datetime(df[dt], infer_datetime_format=False, format='%d%b%Y %H:%M:%S', errors='coerce')
            else:
                df[dt] = pd.to_datetime(df[dt], infer_datetime_format=False, format='%d%b%Y:%H:%M:%S', errors='coerce')

        df['AN_BASE'] = df['AN_BASE'].fillna(self.ano).astype(int)
        df['ID_ADD_PRODUCAO_INTELECTUAL'] = df['ID_ADD_PRODUCAO_INTELECTUAL'].fillna(0).astype(int)
        df['ID_PRODUCAO_INTELECTUAL'] = df['ID_PRODUCAO_INTELECTUAL'].fillna(0).astype(int)
        df['ID_SUBTIPO_PRODUCAO'] = df['ID_SUBTIPO_PRODUCAO'].fillna(0).astype(int)
        df['IN_ORIENT_PARTICIPOU_BANCA'] = df['IN_ORIENT_PARTICIPOU_BANCA'].fillna(0).astype(int)
        df['ID_PESSOA_DISCENTE'] = df['ID_PESSOA_DISCENTE'].fillna(0).astype(int)
        df['ID_GRAU_ACADEMICO'] = df['ID_GRAU_ACADEMICO'].fillna(0).astype(int)
        df['CD_GRANDE_AREA_CONHECIMENTO'] = df['CD_GRANDE_AREA_CONHECIMENTO'].fillna(0).astype(int)
        df['CD_AREA_CONHECIMENTO'] = df['CD_AREA_CONHECIMENTO'].fillna(0).astype(int)
        df['NR_PAGINAS'] = df['NR_PAGINAS'].fillna(0).astype(int)

        df['AN_BASE_facet'] = gYear(self.ano)
        df['ANO_MATRICULA_facet'] = df[df['DT_MATRICULA'].notnull()]['DT_MATRICULA'].dt.year.apply(gYear)
        df['ANO_TITULACAO_facet'] = df['DT_TITULACAO'].dt.year.apply(gYear)
        df['ANO_INICIO_LINHA_facet'] = df['DH_INICIO_LINHA'].dt.year.apply(gYear)
        df['ANO_FIM_LINHA_facet'] = df['DH_FIM_LINHA'].dt.year.apply(gYear)
        df['GEOGRAFICO_IES_facet'] = df['NM_REGIAO'] + '|' + df['NM_UF_IES'] + '-' + df['SG_UF_IES']
        df['AREA_CONHECIMENTO_facet'] = df['NM_GRANDE_AREA_CONHECIMENTO'] + '|' + df[
            'NM_AREA_CONHECIMENTO']
        df['DS_PALAVRA_CHAVE_exact'] = df['DS_PALAVRA_CHAVE'].apply(norm_keyword)
        df['DS_KEYWORD_exact'] = df['DS_KEYWORD'].apply(norm_keyword)

        df['TITULO_RESUMO'] = df['NM_PRODUCAO'] + '\n' + df['DS_RESUMO']

        return df

    def gera_csv(self):
        df = self.resolve_dicionarios()
        destino_transform = BASE_PATH_DATA + 'capes_teses/' + str(self.ano) + '/transform'
        csv_file = '/capes_teses_' + str(self.ano) + '.csv'
        log_file = '/capes_teses_' + str(self.ano) + '.log'
        try:
            os.makedirs(destino_transform)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        df.to_csv(destino_transform + csv_file, sep=';', index=False, encoding='utf8',
                  line_terminator='\n', quoting=csv.QUOTE_ALL)
        self.output_length = commands.getstatusoutput('cat ' + destino_transform + csv_file + ' |wc -l')[1]
        print 'Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1)

        with open(destino_transform + log_file, 'w') as log:
            log.write('Log gerado em {}'.format(self.date.strftime("%Y-%m-%d %H:%M")))
            log.write("\n")
            log.write('Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1))
            log.write("\n")
            log.write('Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1))
        print('Processamento CAPES TESES {} finalizado, arquivo de log gerado em {}'.format(str(self.ano),
                                                                                            destino_transform + log_file))


def capes_teses_tranform():
    PATH_ORIGEM = BASE_PATH_DATA + 'capes_teses/'
    try:
        anos = os.listdir(PATH_ORIGEM)
        anos.sort()
    except OSError:
        print('Nenhuma pasta encontrada')
        raise
    for ano in anos:
        print(ano)
        try:
            capes_teses = CapesTeses(ano)
            capes_teses.gera_csv()
            print('Arquivo do ano, {} finalizado'.format(ano))

        except:
            print u'Arquivo do ano, {} não encontrado'.format(ano)
            raise
        print('Fim!!')
        print('\n')
