# -*- coding: utf8 -*-
import errno
import os
import sys
import unicodedata
import re
import pandas as pd
import csv
import commands
from datetime import datetime
from utils.utils import *

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from dicionarios.cnae1 import cnae1_dic
from dicionarios.cnae2_subclasse import cnae2subclasse_dic
from dicionarios.natureza_juridica import natureza_juridica_dic
from dicionarios.uf import uf_dic
from dicionarios.tamanho_estabelecimento import tamanho_estab_dic
from dicionarios.ibge_subsetor import ibge_sub_dic
#from dicionarios.distrito_sp import distrito_sp_dic
#from dicionarios.bairro_fort import bairro_fort_dic
#from dicionarios.bairro_rj import bairro_rj_dic
#from dicionarios.bairro_sp import bairro_sp_dic
from dicionarios.regioes_adm_df import regioes_adm_df_dic
from dicionarios.municipios import municipios_dic

# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)

class RaisEstabelecimentosTransform(object):
    """
    A classe RaisEstabelecimentosTransform é responsável pela transformaçao da base de dados(Collection - rais_estabelecimentos),
    faz parte do processo de ETL(Extração, Transformação e Carga).

    Atributos:
        horas               (date): data de execução deste arquivo.
        input_lenght        (int): Variável que irá guardar a quantidade de linhas do arquivo de entrada(download).
        output_length       (int): Variável que irá guardar a quantidade de linhas do arquivo de saída(transform).
        f                   (str): Variável para armazenar o nome dos arquivos contidos no diretório download da rais estabelecimentos.
        variáveis           (dic): Dicionário das colunas do arquivo csv, para serem resolvidos de acordo com sua chave.
        avoid               (list): Lista com os campos/colunas que não farão parte do arquivo .csv gerado para a carga no solr.
        destino_transform   (str): Path de destino do arquivo .csv gerado para a carga no solr.

    """

    def __init__(self, ano):
        """
        Construtor da classe RaisEstabelecimentosTransform, recebe de 1 parâmetro:
        ano    (str): Nome dos diretórios na pasta BASE_PATH_DATA + 'rais_estabelecimentos/'.

        """
        self.horas = datetime.datetime.now()
        self.input_lenght = 0
        self.output_lenght = 0
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
            u'Tipo Estab.1':{'cnpj':'CNPJ', 'cei': 'CEI'},
            u'UF': uf_dic(),
            u'IBGE Subsetor': ibge_sub_dic()

        }
        self.avoid = ['Bairros SP', 'Bairros Fortaleza', 'Bairros RJ', 'Distritos SP']
        self.destino_transform = '/var/tmp/solr_front/collections/rais_estabelecimentos/' + str(self.ano) + '/transform/'

    def pega_arquivos_ano(self):
        '''
        Pega o arquivo em "rais_estabelecimentos/self.ano/download/", conta as linhas de entrada do arquivo,
        faz um chunck de 200.000 linhas, atribui ao iterdf - que é um TextFileReader e o Percorre
        gerando um dataframe que é passado ao método resolve_dicionário. Cria um contador - self.c
        que será agregado ao nome final do arquivo, recebe o dataframe final do método resolve_dicionário,
        cria o .csv e o .log e os salva no diretório destino_transform.

        '''
        var = '/var/tmp/solr_front/collections/rais_estabelecimentos/' + str(self.ano) + '/download/'
        for root, dirs, files in os.walk(var):
            for f in files:
                if f.endswith(".txt"):
                    self.output_lenght = 0
                    self.f = f.split('.')[0]
                    arquivo = open(os.path.join(root, f), 'r')
                    self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, f) + ' |wc -l')[1]
                    print 'Arquivo {} de entrada possui {} linhas de informacao'.format(f, int(self.input_lenght))
                    iterdf = pd.read_csv(arquivo, sep=';', chunksize=200000, encoding='latin-1', low_memory=False)
                    # iterdf aqui é o pandas.io.parsers.TextFileReader
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
        """
        Pega o Dataframe da iteração do iterdf do método pega_arquivos_ano, remove as colunas
        da lista - self.avoid, adiciona a coluna UF ao dataframe - pegando os códigos do município,
        resolve os dicionários em self.variaveis pegando as chaves e retornando os valores,
        deleta a coluna IBGE subsetor dos anos que não a contém, resolve os campos para facet, busca e nuvem de palavras,
        substitui o espaço vazio dos nomes das colunas por underline e os retorna.

        """

        for item in self.avoid:
            del (df[item])
        #A coluna UF não existe nos arquivos(anos:2010, 2011, 2012), portanto
        #foi feito slice do index de municipio e passado o codigo do estado
        #para o campo UF criado.
        codigo = df[u'Município'].apply(str)

        df[u'UF'] = codigo.str.slice(0,2).astype(int)
        # df[u'CNAE 2.0 Classe'] = df[u'CNAE 2.0 Classe'].astype(str)
        # df[u'CNAE 2.0 Subclasse'] = df[u'CNAE 2.0 Subclasse']

        for k, v in self.variaveis.items():

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
        df[u'REGIAO_facet'] = codigo.str.slice(0,2).astype(int).apply(find_regiao)
        df[u'REGIAO_facet'] = df['REGIAO_facet'] + '|' + df[u'UF'] + '|' + df[u'Município']
        # df[u'CNAE_2.0'] = df[u'CNAE 2.0 Classe']
        # df[u'CNAE_2.0_Subclasse'] = df[u'CNAE 2.0 Subclasse']
        df[u'Tipo Estab.1'] = df[u'Tipo Estab.1'].str.strip()
        df[u'PALAVRAS_CNAE95_exact'] = df[u'CNAE 95 Classe'].apply(norm_keyword)
        df[u'PALAVRA_CNAE20_exact'] = df[u'CNAE 2.0 Subclasse']
        # import pdb; pdb.set_trace()
        # df[u'CNAE_2.0_facet'] = df[u'CNAE 2.0 Classe'] + '|' + df[u'CNAE 2.0 Subclasse']

        df.columns = df.columns.str.replace(' ', '_')
        #df.columns = [remover_acentos(x) for x in list(df.columns)]
        #import pdb; pdb.set_trace()
        return df


def rais_estabelecimentos_transform():
    """
    Função chamada em transform.py para ajustar os dados da Rais estabelecimentos e prepará-los
    para a carga no indexador. Seta o diretorio onde os arquivos a serem transformados/ajustados estão,
    passa o parâmetro - ano para a classe RaisEstabelecimentosTransform.

    """
    try:
        path_origem = '/var/tmp/solr_front/collections/rais_estabelecimentos/'
        anos = [f for f in os.listdir(path_origem) if not f.startswith('.')]
        anos.sort()
        print anos

    except:
        raise
    #rais_estabelecimento = RaisEstabelecimentoTransform('2010')
    #rais_estabelecimento.pega_arquivos_ano()

    for ano in anos:
        rais = RaisEstabelecimentosTransform(ano)
        rais.pega_arquivos_ano()

# função para remover acentos - não usada pq gera um erro devido a codificação do arquivo de origem
def remover_acentos(palavra, codif='utf-8'):

    nfkd = unicodedata.normalize('NFKD', palavra.decode(codif)).encode('ASCII', 'ignore')
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c.decode(codif))])
    palavraSemAcento =  re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)
    return palavraSemAcento.replace(' ','_').replace('__','_').lower()
