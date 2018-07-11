# coding=utf-8
import errno
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from utils import *
import pandas as pd
import numpy as np
import csv
import commands
import datetime


# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)


class Enem(object):
    def __init__(self, ano):
        self.date = datetime.datetime.now()
        self.ano = ano
        self.input_lenght = 0
        self.output_length = 0
        self.gano = gYear(ano)

    @staticmethod
    def regiao(num):
        try:
            uf = str(num)[0]
            if int(uf) == 1:
                return 'Norte'
            elif int(uf) == 2:
                return 'Nordeste'
            elif int(uf) == 3:
                return 'Sudeste'
            elif int(uf) == 4:
                return 'Sul'
            elif int(uf) == 5:
                return 'Centro-Oeste'
            elif int(uf) == 8:
                return 'Brasil'
            elif int(uf) == 9:
                return 'Pais estrangeiro'
        except ValueError:
            return ''

    def pega_arquivo_ano(self, ano):
        file_list = ['MICRODADOS_ENEM_2015.csv', 'microdados_enem_2016.csv', 'MICRODADOS_ENEM_2017.csv']

        var = '/var/tmp/enem/' + str(self.ano) + '/download/'
        exclude_prefixes = ('__', '.')
        for root, dirs, files in os.walk(var, topdown=True):
            dirs[:] = [dirname for dirname in dirs if not dirname.startswith(exclude_prefixes)]
            for f in files:
                if f in file_list:
                    arquivo = open(os.path.join(root, f), 'r')  # , encoding='latin-1')
                    # self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, f) + ' |wc -l')[1]
                    # print 'Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1)
                    if ano in ['2014', '2015']:
                        df = pd.read_csv(arquivo, sep=',', low_memory=False, engine='c', encoding='cp1252',
                                         chunksize=500000)  # , )
                    else:
                        df = pd.read_csv(arquivo, sep=';', low_memory=False, engine='c', encoding='cp1252',
                                         chunksize=500000)  # , usecols=cols)

                    return df

    def resolve_dicionario_567(self):

        cols = [u'NU_INSCRICAO', u'NU_ANO', u'CO_MUNICIPIO_RESIDENCIA',
                u'NO_MUNICIPIO_RESIDENCIA', u'CO_UF_RESIDENCIA', u'SG_UF_RESIDENCIA',
                u'NU_IDADE', u'TP_SEXO', u'TP_ESTADO_CIVIL',
                u'TP_COR_RACA', u'TP_NACIONALIDADE', u'CO_MUNICIPIO_NASCIMENTO',
                u'NO_MUNICIPIO_NASCIMENTO', u'CO_UF_NASCIMENTO', u'SG_UF_NASCIMENTO',
                u'TP_ST_CONCLUSAO', u'TP_ANO_CONCLUIU', u'TP_ESCOLA', u'TP_ENSINO', u'IN_TREINEIRO', u'CO_ESCOLA',
                u'CO_MUNICIPIO_ESC',
                u'NO_MUNICIPIO_ESC', u'CO_UF_ESC', u'SG_UF_ESC', u'TP_DEPENDENCIA_ADM_ESC', u'TP_LOCALIZACAO_ESC',
                u'TP_SIT_FUNC_ESC',
                u'IN_BAIXA_VISAO', u'IN_CEGUEIRA', u'IN_SURDEZ', u'IN_DEFICIENCIA_AUDITIVA', u'IN_SURDO_CEGUEIRA',
                u'IN_DEFICIENCIA_FISICA', u'IN_DEFICIENCIA_MENTAL', u'IN_DEFICIT_ATENCAO', u'IN_DISLEXIA',
                u'IN_DISCALCULIA',
                u'IN_AUTISMO', u'IN_VISAO_MONOCULAR', u'IN_OUTRA_DEF', u'IN_GESTANTE', u'IN_LACTANTE', u'IN_IDOSO',
                u'IN_ESTUDA_CLASSE_HOSPITALAR', u'IN_SEM_RECURSO', u'IN_BRAILLE', u'IN_AMPLIADA_24',
                u'IN_AMPLIADA_18', u'IN_LEDOR',
                u'IN_ACESSO', u'IN_TRANSCRICAO', u'IN_LIBRAS', u'IN_LEITURA_LABIAL', u'IN_MESA_CADEIRA_RODAS',
                u'IN_MESA_CADEIRA_SEPARADA', u'IN_APOIO_PERNA', u'IN_GUIA_INTERPRETE', u'IN_COMPUTADOR',
                u'IN_CADEIRA_ESPECIAL',
                u'IN_CADEIRA_CANHOTO', u'IN_CADEIRA_ACOLCHOADA', u'IN_PROVA_DEITADO', u'IN_MOBILIARIO_OBESO',
                u'IN_LAMINA_OVERLAY',
                u'IN_PROTETOR_AURICULAR', u'IN_MEDIDOR_GLICOSE', u'IN_MAQUINA_BRAILE', u'IN_SOROBAN',
                u'IN_MARCA_PASSO', u'IN_SONDA',
                u'IN_MEDICAMENTOS', u'IN_SALA_INDIVIDUAL', u'IN_SALA_ESPECIAL', u'IN_SALA_ACOMPANHANTE',
                u'IN_MOBILIARIO_ESPECIFICO',
                u'IN_NOME_SOCIAL', u'CO_MUNICIPIO_PROVA', u'NO_MUNICIPIO_PROVA', u'CO_UF_PROVA',
                u'SG_UF_PROVA', u'TP_PRESENCA_CN',
                u'TP_PRESENCA_CH', u'TP_PRESENCA_LC', u'TP_PRESENCA_MT', u'CO_PROVA_CN', u'CO_PROVA_CH', u'CO_PROVA_LC',
                u'CO_PROVA_MT', u'NU_NOTA_CN', u'NU_NOTA_CH', u'NU_NOTA_LC', u'NU_NOTA_MT', u'TP_LINGUA',
                u'TP_STATUS_REDACAO', u'NU_NOTA_REDACAO']

        sim_nao = ['IN_BAIXA_VISAO', 'IN_CEGUEIRA', 'IN_SURDEZ',
                   'IN_DEFICIENCIA_AUDITIVA', 'IN_SURDO_CEGUEIRA', 'IN_DEFICIENCIA_FISICA',
                   'IN_DEFICIENCIA_MENTAL', 'IN_DEFICIT_ATENCAO', 'IN_DISLEXIA',
                   'IN_GESTANTE', 'IN_LACTANTE', 'IN_IDOSO', 'IN_AUTISMO', 'IN_BRAILLE',
                   'IN_AMPLIADA_24', 'IN_AMPLIADA_18', 'IN_LEDOR', 'IN_ACESSO', 'IN_TRANSCRICAO',
                   'IN_LIBRAS', 'IN_LEITURA_LABIAL', 'IN_MESA_CADEIRA_RODAS', 'IN_MESA_CADEIRA_SEPARADA',
                   'IN_APOIO_PERNA', 'IN_GUIA_INTERPRETE', 'IN_ESTUDA_CLASSE_HOSPITALAR']

        variaveis = {
            'TP_COR_RACA': {0: 'ND', 1: 'Branca', 2: 'Preta', 3: 'Parda', 4: 'Amarela', 5: 'Indigena'},
            'TP_ESTADO_CIVIL': {0: 'Solteiro', 1: 'Casado/Uniao Estavel', 2: 'Divorciado', 3: 'Viuvo'},
            'TP_LINGUA': {0: 'Ingles', 1: 'Espanhol'},
            'TP_ESCOLA': {1: 'Não Respondeu', 2: 'Publica', 3: 'Privada', 4: 'Exterior'}

        }
        iter_df = self.pega_arquivo_ano(self.ano)
        control = 0
        i = 0
        max_files = 8
        for df in iter_df:

            df = df[cols]

            df['ID'] = str(self.ano) + '_' + df['NU_INSCRICAO'].astype(str)
            df['ANO_facet'] = self.gano + '|' + df['NU_ANO'].astype(str)
            df['REGIAO_RESIDENCIA'] = df['CO_UF_RESIDENCIA'].apply(self.regiao)
            df['REGIAO_NASCIMENTO'] = df['CO_UF_NASCIMENTO'].apply(self.regiao)
            df['REGIAO_PROVA'] = df['CO_UF_PROVA'].apply(self.regiao)
            for k, v in variaveis.items():
                df[k].replace(v, inplace=True)

            for item in sim_nao:
                df[item] = np.where(df[item] == 1, 'Sim', 'Não')

            df['REGIAO_RESIDENCIA_facet'] = df['REGIAO_RESIDENCIA'] + '|' + df['SG_UF_RESIDENCIA'] + '|' + df[
                'NO_MUNICIPIO_RESIDENCIA']
            df['REGIAO_NASCIMENTO_facet'] = df['REGIAO_NASCIMENTO'] + '|' + df['SG_UF_NASCIMENTO'] + '|' + df[
                'NO_MUNICIPIO_NASCIMENTO']
            df['REGIAO_PROVA_facet'] = df['REGIAO_PROVA'] + '|' + df['SG_UF_PROVA'] + '|' + df['NO_MUNICIPIO_PROVA']

            if control == 0:
                # print 'gerando novo csv'
                self.gera_csv(df, i, 'w')
                control += 1
            elif 0 < control <= max_files:
                # print 'append csv'
                self.gera_csv(df, i, 'a')
                control += 1
            elif control > max_files:
                control = 1
                i += 1
                self.gera_csv(df, i, 'w')
            # print control
        return 'FIM'

    def gera_csv(self, df, control, mode, ):
        destino_transform = '/var/tmp/enem/' + str(self.ano) + '/transform/'

        try:
            os.makedirs(destino_transform)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        if mode == 'a':
            header = 0
        else:
            header = True

        # log_file = '/enem_' + str(ano) + '.log'
        csv_file = '/enem_' + str(self.ano) + '_' + str(control) + '.csv'
        df.to_csv(destino_transform + csv_file, sep=';', line_terminator='\n', index=False, header=header,
                  encoding='utf8', quoting=csv.QUOTE_ALL, mode=mode)

    def gera_log(self):
        pass


def enem_transform():
    PATH_ORIGEM = '/var/tmp/enem/'
    try:
        anos = [f for f in os.listdir(PATH_ORIGEM) if not f.startswith('.')]
        anos.sort()
    except OSError:
        print('Nenhuma pasta encontrada')
        raise
    for ano in anos:
        print(ano)
        try:
            inep_doc = Enem(ano)
            inep_doc.resolve_dicionario_567()
            print('Arquivo do ano, {} finalizado'.format(ano))

        except:
            print 'Arquivo do ano, {} não encontrado'.format(ano)
            raise
        print('Fim!!')
        print('\n')
