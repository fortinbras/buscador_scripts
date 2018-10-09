# coding=utf-8
import errno
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from utils import *
import pandas as pd
import codecs
import csv
import commands
from datetime import datetime


class Capes(object):

    def __init__(self, year):
        self.date = datetime.now()
        self.ano = year
        self.input_lenght = 0
        self.output_length = 0
        self.CO_GRUPO = 0
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
        

    def pega_arquivo_ano(self):

        var = '/var/tmp/solr_front/collections/enade/' + str(self.ano) + '/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".txt"):
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                    self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l ')[1]
                    print 'Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1)
                    df_enade = pd.read_csv(arquivo, sep=';', low_memory=False)
                    df_enade = df_enade.loc[:, self.colunas]
                    # df_enade.fillna('', inplace=True)

        return df_enade

    def resolver_dicionario(self):
        df_enade = self.pega_arquivo_ano()

        municipios = pd.read_csv('lista_municipios.csv', sep=';', dtype={'CÓDIGO DO MUNICÍPIO': 'str'})
        municipios = municipios.rename(columns={'CÓDIGO DO MUNICÍPIO': 'CO_MUNIC_CURSO'})
        municipios['REGIAO'] = municipios['CO_MUNIC_CURSO'].apply(find_regiao)
        df_enade = df_enade.astype('str')
        df_enade[['MUNIC_CURSO', 'UF_CURSO', 'REGIAO_CURSO']] = pd.merge(df_enade, municipios, how='left', on=[
            'CO_MUNIC_CURSO']).loc[:, ['NOME DO MUNICÍPIO', 'UF', 'REGIAO']]
        df_enade['CO_CATEGAD'] = df_enade['CO_CATEGAD'].astype(str).replace(self.CO_CATEGAD)
        df_enade['CO_ORGACAD'] = df_enade['CO_ORGACAD'].astype(str).replace(self.CO_ORGACAD)
        df_enade['CO_GRUPO'] = df_enade['CO_GRUPO'].astype(str).replace(self.CO_GRUPO)
        df_enade['CO_MODALIDADE'] = df_enade['CO_MODALIDADE'].astype(str).replace(self.CO_MODALIDADE)
        df_enade['ID'] = [str(self.ano) + '_' + str(i + 1) for i in range(df_enade.index.size)]

        df_enade['ANO_facet'] = df_enade['NU_ANO'].apply(gYear) + '|' + df_enade['NU_ANO'].astype(str)
        df_enade['ANO_FIM_2G_facet'] = df_enade['ANO_FIM_2G'].apply(gYear)
        df_enade['ANO_IN_GRAD_facet'] = df_enade['ANO_IN_GRAD'].apply(gYear)
        df_enade['GEOGRAFICO_facet'] = df_enade['REGIAO_CURSO'].astype(str) + '|' + df_enade['UF_CURSO'].astype(
            str) + '|' + df_enade['MUNIC_CURSO'].astype(str)

        # PESSOAIS
        df_enade['ESTADO_CIVIL'] = df_enade['QE_I01'].replace(self.QE_I01)
        df_enade['ESC_PAI'] = df_enade['QE_I04'].replace(self.QE_I04)
        df_enade['ESC_MAE'] = df_enade['QE_I05'].replace(self.QE_I05)
        df_enade['MORADIA'] = df_enade['QE_I06'].replace(self.QE_I06)
        df_enade['INCENTIVO_GRAD'] = df_enade['QE_I19'].replace(self.QE_I19)
        df_enade['MODALIDADE_2G'] = df_enade['QE_I18'].replace(self.QE_I18)

        # SOCIOECONOMICAS
        df_enade['COR_RACA'] = df_enade['QE_I02'].replace(self.QE_I02)
        df_enade['RENDA_FAMILIAR'] = df_enade['QE_I08'].replace(self.QE_I08)
        df_enade['SIT_FINAN'] = df_enade['QE_I09'].replace(self.QE_I09)
        df_enade['SIT_TRAB'] = df_enade['QE_I10'].replace(self.QE_I10)

        # BOLSAS
        df_enade['TIPO_BOLSA'] = df_enade['QE_I11'].replace(self.QE_I11)
        df_enade['TRAJ_ACAD'] = df_enade['QE_I13'].replace(self.QE_I13)
        df_enade['EC_EXT'] = df_enade['QE_I14'].replace(self.QE_I14)
        df_enade['ING_GRAD'] = df_enade['QE_I15'].replace(self.QE_I15)

        # GEOGRAFICO
        df_enade['UF_2G'] = df_enade['QE_I16'].astype(str).replace(self.QE_I16)
        df_enade['ESCOLA_2G'] = df_enade['QE_I17'].replace(self.QE_I17)

        del (df_enade['CO_MUNIC_CURSO'])
        del (df_enade['CO_UF_CURSO'])
        del (df_enade['CO_REGIAO_CURSO'])
        del (df_enade['AMOSTRA'])
        del (df_enade['QE_I01'])
        del (df_enade['QE_I02'])
        del (df_enade['QE_I08'])

        return df_enade

    def dicionario_2013(self):
        self.CO_GRUPO = {'5': 'MEDICINA VETERINÁRIA',
                         '6': 'ODONTOLOGIA',
                         '12': 'MEDICINA',
                         '17': 'AGRONOMIA',
                         '19': 'FARMÁCIA',
                         '23': 'ENFERMAGEM',
                         '27': 'FONOAUDIOLOGIA',
                         '28': 'NUTRIÇÃO',
                         '36': 'FISIOTERAPIA',
                         '38': 'SERVIÇO SOCIAL',
                         '51': 'ZOOTECNIA',
                         '55': 'BIOMEDICINA',
                         '69': 'TECNOLOGIA EM RADIOLOGIA',
                         '90': 'TECNOLOGIA EM AGRONEGÓCIOS',
                         '91': 'TECNOLOGIA EM GESTÃO HOSPITALAR',
                         '92': 'TECNOLOGIA EM GESTÃO AMBIENTAL',
                         '95': 'TECNOLOGIA EM ESTÉTICA E COSMÉTICA',
                         '3501': 'EDUCAÇÃO FÍSICA (BACHARELADO)', }
        df_enade = self.resolver_dicionario()
        return df_enade

    def dicionario_2014(self):
        self.CO_GRUPO = {
            '21': 'ARQUITETURA E URBANISMO',
            '72': 'TECNOLOGIA EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
            '73': 'TECNOLOGIA EM AUTOMAÇÃO INDUSTRIAL',
            '76': 'TECNOLOGIA EM GESTÃO DA PRODUÇÃO INDUSTRIAL',
            '79': 'TECNOLOGIA EM REDES DE COMPUTADORES',
            '701': 'MATEMÁTICA (BACHARELADO)',
            '702': 'MATEMÁTICA (LICENCIATURA)',
            '903': 'LETRAS-PORTUGUÊS (BACHARELADO)',
            '904': 'LETRAS-PORTUGUÊS (LICENCIATURA)',
            '905': 'LETRAS-PORTUGUÊS E INGLÊS (LICENCIATURA)',
            '906': 'LETRAS-PORTUGUÊS E ESPANHOL (LICENCIATURA)',
            '1401': 'FÍSICA (BACHARELADO)',
            '1402': 'FÍSICA (LICENCIATURA)',
            '1501': 'QUÍMICA (BACHARELADO)',
            '1502': 'QUÍMICA (LICENCIATURA)',
            '1601': 'CIÊNCIAS BIOLÓGICAS (BACHARELADO)',
            '1602': 'CIÊNCIAS BIOLÓGICAS (LICENCIATURA)',
            '2001': 'PEDAGOGIA (LICENCIATURA)',
            '2401': 'HISTÓRIA (BACHARELADO)',
            '2402': 'HISTÓRIA (LICENCIATURA)',
            '2501': 'ARTES VISUAIS (LICENCIATURA)',
            '3001': 'GEOGRAFIA (BACHARELADO)',
            '3002': 'GEOGRAFIA (LICENCIATURA)',
            '3201': 'FILOSOFIA (BACHARELADO)',
            '3202': 'FILOSOFIA (LICENCIATURA)',
            '3502': 'EDUCAÇÃO FÍSICA (LICENCIATURA)',
            '4004': 'CIÊNCIA DA COMPUTAÇÃO (BACHARELADO)',
            '4005': 'CIÊNCIA DA COMPUTAÇÃO (LICENCIATURA)',
            '4006': 'SISTEMAS DE INFORMAÇÃO',
            '4301': 'MÚSICA (LICENCIATURA)',
            '5401': 'CIÊNCIAS SOCIAIS (BACHARELADO)',
            '5402': 'CIÊNCIAS SOCIAIS (LICENCIATURA)',
            '5710': 'ENGENHARIA CIVIL',
            '5806': 'ENGENHARIA ELÉTRICA',
            '5809': 'ENGENHARIA DE COMPUTAÇÃO',
            '5814': 'ENGENHARIA DE CONTROLE E AUTOMAÇÃO',
            '5902': 'ENGENHARIA MECÂNICA',
            '6008': 'ENGENHARIA QUÍMICA',
            '6009': 'ENGENHARIA DE ALIMENTOS',
            '6208': 'ENGENHARIA DE PRODUÇÃO',
            '6306': 'ENGENHARIA',
            '6307': 'ENGENHARIA AMBIENTAL',
            '6405': 'ENGENHARIA FLORESTAL',

        }
        df_enade = self.resolver_dicionario()
        return df_enade

    def dicionario_2015(self):

        self.CO_GRUPO = {'1': 'ADMINISTRAÇÃO',
                         '2': 'DIREITO',
                         '13': 'CIÊNCIAS ECONÔMICAS',
                         '18': 'PSICOLOGIA',
                         '22': 'CIÊNCIAS CONTÁBEIS',
                         '26': 'DESIGN',
                         '29': 'TURISMO',
                         '67': 'SECRETARIADO EXECUTIVO',
                         '81': 'RELAÇÕES INTERNACIONAIS',
                         '83': 'TECNOLOGIA EM DESIGN DE MODA',
                         '84': 'TECNOLOGIA EM MARKETING',
                         '85': 'TECNOLOGIA EM PROCESSOS GERENCIAIS',
                         '86': 'TECNOLOGIA EM GESTÃO DE RECURSOS HUMANOS',
                         '87': 'TECNOLOGIA EM GESTÃO FINANCEIRA',
                         '88': 'TECNOLOGIA EM GASTRONOMIA',
                         '93': 'TECNOLOGIA EM GESTÃO COMERCIAL',
                         '94': 'TECNOLOGIA EM LOGÍSTICA',
                         '100': 'ADMINISTRAÇÃO PÚBLICA',
                         '101': 'TEOLOGIA',
                         '102': 'TECNOLOGIA EM COMÉRCIO EXTERIOR',
                         '103': 'TECNOLOGIA EM DESIGN DE INTERIORES',
                         '104': 'TECNOLOGIA EM DESIGN GRÁFICO',
                         '105': 'TECNOLOGIA EM GESTÃO DA QUALIDADE',
                         '106': 'TECNOLOGIA EM GESTÃO PÚBLICA',
                         '803': 'JORNALISMO',
                         '804': 'PUBLICIDADE E PROPAGANDA',
                         }
        df_enade = self.resolver_dicionario()
        return df_enade

    def dicionario_2016(self):
        self.CO_GRUPO = {'5': 'MEDICINA VETERINÁRIA',
                         '6': 'ODONTOLOGIA',
                         '12': 'MEDICINA',
                         '17': 'AGRONOMIA',
                         '19': 'FARMÁCIA',
                         '23': 'ENFERMAGEM',
                         '27': 'FONOAUDIOLOGIA',
                         '28': 'NUTRIÇÃO',
                         '36': 'FISIOTERAPIA',
                         '38': 'SERVIÇO SOCIAL',
                         '51': 'ZOOTECNIA',
                         '55': 'BIOMEDICINA',
                         '69': 'TECNOLOGIA EM RADIOLOGIA',
                         '90': 'TECNOLOGIA EM AGRONEGÓCIOS',
                         '91': 'TECNOLOGIA EM GESTÃO HOSPITALAR',
                         '92': 'TECNOLOGIA EM GESTÃO AMBIENTAL',
                         '95': 'TECNOLOGIA EM ESTÉTICA E COSMÉTICA',
                         '3501': 'EDUCAÇÃO FÍSICA (BACHARELADO)', }
        df_enade = self.resolver_dicionario()
        return df_enade

    def gera_csv(self):
        if str(self.ano) == '2016':
            df_enade = self.dicionario_2016()
        elif str(self.ano) == '2015':
            df_enade = self.dicionario_2015()
        elif str(self.ano) == '2014':
            df_enade = self.dicionario_2014()
        elif str(self.ano) == '2013':
            df_enade = self.dicionario_2013()
        else:
            pass
        destino_transform = '/var/tmp/solr_front/collections/enade/' + str(self.ano) + '/transform'
        csv_file = '/enade_' + str(self.ano) + '.csv'
        log_file = '/enade_' + str(self.ano) + '.log'
        try:
            os.makedirs(destino_transform)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        # df_enade = df_enade.astype(str)

        df_enade.to_csv(destino_transform + csv_file, sep=';', index=False, encoding='utf8',
                        line_terminator='\n', quoting=csv.QUOTE_ALL)
        self.output_length = commands.getstatusoutput('cat ' + destino_transform + csv_file + ' |wc -l')[1]
        print 'Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1)

        with open(destino_transform + log_file, 'w') as log:
            log.write('Log gerado em {}'.format(self.date.strftime("%Y-%m-%d %H:%M")))
            log.write("\n")
            log.write('Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght) - 1))
            log.write("\n")
            log.write('Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1))
        print('Processamento ENADE {} finalizado, arquivo de log gerado em {}'.format(str(self.ano),
                                                                                      destino_transform + log_file))


def enade_tranform():
    PATH_ORIGEM = '/var/tmp/solr_front/collections/enade/'
    try:
        anos = os.listdir(PATH_ORIGEM)
        anos.sort()
    except OSError:
        print('Nenhuma pasta encontrada')
        raise
    for ano in anos:
        print(ano)
        try:
            inep_doc = Enade(ano)
            inep_doc.gera_csv()
            print('Arquivo do ano, {} finalizado'.format(ano))

        except:
            print 'Arquivo do ano, {} não encontrado'.format(ano)
            pass
        print('Fim!!')
        print('\n')

# if __name__ == '__main__':
#     PATH_ORIGEM = '/var/tmp/solr_front/collections/enade/'
#     try:
#         anos = os.listdir(PATH_ORIGEM)
#         anos.sort()
#     except OSError:
#         print('Nenhuma pasta encontrada')
#         raise
#     for ano in anos:
#         print(ano)
#         try:
#             inep_doc = Enade(ano)
#             inep_doc.gera_csv()
#             print('Arquivo do ano, {} finalizado'.format(ano))
#
#         except:
#             print 'Arquivo do ano, {} não encontrado'.format(ano)
#             pass
#         print('Fim!!')
#         print('\n')
