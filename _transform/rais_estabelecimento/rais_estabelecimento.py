# -*- coding: utf8 -*-
import errno
import os
import sys
import unicodedata
import re

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from utils import *
import pandas as pd
import csv
import commands
from datetime import datetime
from cnae1 import cnae1_dic
from cnae2_subclasse import cnae2subclasse_dic
from natureza_juridica import natureza_juridica_dic
from uf import uf_dic
from tamanho_estabelecimento import tamanho_estab_dic
from ibge_subsetor import ibge_sub_dic
#from distrito_sp import distrito_sp_dic
#from bairro_fort import bairro_fort_dic
#from bairro_rj import bairro_rj_dic
#from bairro_sp import bairro_sp_dic
from regioes_adm_df import regioes_adm_df_dic
from municipios import municipios_dic

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)

class RaisEstabelecimentoTransform(object):

    def __init__(self, ano):
        self.horas = datetime.now()
        self.input_lenght = 0
        self.output_lenght = 0
        self.df = pd.DataFrame()
        self.f = ''
        self.ano = ano
        self.variaveis = {

            u'CNAE 95 Classe': cnae1_dic(),
            u'Ind Atividade Ano': {0: 'Não', 1: 'Sim'},
            u'Ind CEI Vinculado': {0: 'Não', 1: 'Sim'},
            u'Ind Estab Participa PAT': {0: 'Não', 1: 'Sim'},
            u'Ind Rais Negativa': {0: 'Não', 1: 'Sim'},
            u'Ind Simples': {0: 'Não', 1: 'Sim'},
            u'Município': municipios_dic(),
            u'Natureza Jurídica': natureza_juridica_dic(),
            u'Regiões Adm DF': regioes_adm_df_dic(),
            u'CNAE 2.0 Subclasse': cnae2subclasse_dic(),
            u'Tamanho Estabelecimento': tamanho_estab_dic(),
            u'Tipo Estab': {1: 'CNPJ', 3: 'CEI', 9: 'Não identificado', -1: 'Ignorado'},
            u'Tipo Estab.1':{'CNPJ':'CNPJ', 'CEI': 'CEI'},
            u'UF': uf_dic(),
            u'IBGE Subsetor': ibge_sub_dic(),

        }
        self.avoid = ['Bairros SP', 'Bairros Fortaleza', 'Bairros RJ', 'Distritos SP']
        self.destino_transform = '/var/tmp/solr_front/collections/rais_estabelecimento/' + str(self.ano) + '/transform/'

    def pega_arquivos_ano(self):
        var = '/var/tmp/solr_front/collections/rais_estabelecimento/' + str(self.ano) + '/download/'
        for root, dirs, files in os.walk(var):
            for f in files:
                if f.endswith(".txt"):
                    self.output_lenght = 0
                    self.f = f.split('.')[0]
                    arquivo = open(os.path.join(root, f), 'r')
                    self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, f) + ' |wc -l')[1]
                    print 'Arquivo {} de entrada possui {} linhas de informacao'.format(f, int(self.input_lenght))
                    iterdf = pd.read_csv(arquivo, sep=';', chunksize=200000, encoding='latin-1', low_memory=False)
                    #iterdf = pd.read_csv(arquivo, sep=';', nrows=1000, chunksize=500, encoding='latin-1', low_memory=False)
                    self.c = 0

                    for df in iterdf:
                        nfile = self.destino_transform + self.f + '_' + str(self.c)+ '.csv'
                        df = self.resolve_dicionario(df)
                        try:
                            os.makedirs(self.destino_transform)
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise
                        df.to_csv(nfile, sep=';', line_terminator='\n', index=False,
                                  encoding='utf8', quoting=csv.QUOTE_ALL, chunksize=100001)
                        self.output_lenght += int(commands.getstatusoutput('cat ' + nfile + ' |wc -l')[1])
                        print 'Arquivo {} de saida foi criado'.format((self.f + '_' + str(self.c) + '.csv'))
                        self.c += 1

                    with open(self.destino_transform + self.f +'_log.txt', 'a') as logfile:
                        logfile.write('################\n')
                        logfile.write('Log gerado em {}\n'.format(self.horas.strftime("%Y-%m-%d %H:%M")))
                        logfile.write('Arquivo {} de entrada possui {} linhas de informacao\n'.format(f, int(self.input_lenght)))
                        logfile.write('O arquivo de saida possui {} linhas de informacao\n'.format((int(self.output_lenght) + 1) - self.c))
                        logfile.write('################\n')

                    print 'Arquivo de saida possui {} linhas de informacao'.format((int(self.output_lenght) + 1) - self.c)
                    print 'FIM'

                    # os.remove(os.path.join(root, f))

    def resolve_dicionario(self, df):
        # import pdb; pdb.set_trace()
        for item in self.avoid:
            del (df[item])
        #A coluna UF não existe nos arquivos(anos:2010, 2011, 2012), portanto
        #foi feito slice do index de municipio e passado o codigo do Mestrado
        #para o campo UF criado.
        codigo = df[u'Município'].apply(str)
        df[u'UF'] = codigo.str.slice(0,2).astype(int)

        for k, v in self.variaveis.items():
            # import pdb; pdb.set_trace()
            try:
                df[k] = df[k].map(v).fillna(df[k])

            except KeyError:
                df[k] = 'Não disponivel'
        #para não exibir a coluna vazia IBGE setor, que não está no ESTB2013.txt
        if self.ano in ['2010','2011','2012','2013']:
            for col in df.columns:
                if col == 'IBGE Subsetor':
                    del(df[u'IBGE Subsetor'])

        df[u'Município'] = df[u'Município'].str.split('-').str.get(1)
        #df.columns = df.columns.str.replace(' ', '_')
        #df.columns = [remover_acentos(x) for x in list(df.columns)]
        return df


def rais_estabelecimento_transform():
    try:
        path_origem = '/var/tmp/solr_front/collections/rais_estabelecimento/'
        anos = [f for f in os.listdir(path_origem) if not f.startswith('.')]
        anos.sort()
        print anos
    except:
        raise
    #rais_estabelecimento = RaisEstabelecimentoTransform('2010')
    #rais_estabelecimento.pega_arquivos_ano()

    for ano in anos:
        rais = RaisEstabelecimentoTransform(ano)
        rais.pega_arquivos_ano()

def remover_acentos(palavra, codif='utf-8'):

    nfkd = unicodedata.normalize('NFKD', palavra.decode(codif)).encode('ASCII', 'ignore')
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c.decode(codif))])
    palavraSemAcento =  re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)
    return palavraSemAcento.replace(' ','_').replace('__','_').lower()
