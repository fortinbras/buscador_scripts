# -*- coding: utf8 -*-
import errno
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

from utils import *
import pandas as pd
import csv
import commands
import datetime
from cbo_ocupacoes import cbo_ocup
from cnae_subclasse import cnae2sub_dic
from cnae1 import canae1_dic
from municipios import municipios_dic


# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)

class RaisTransform(object):

    def __init__(self, ano):
        self.horas = datetime.datetime.now()
        self.input_lenght = 0
        self.output_lenght = 0
        self.df = pd.DataFrame()
        self.f = ''
        self.colunas = [u'Causa_Afastamento_1', u'Causa_Afastamento_2', u'Causa_Afastamento_3',
                        u'Motivo_Desligamento', u'CBO_Ocupacao_2002',
                        u'CNAE_95_Classe', u'Vinculo_Ativo_31/12', u'Faixa_Etaria',
                        u'Faixa_Hora_Contrat', u'Faixa_Remun_Dezem_(SM)',
                        u'Faixa_Remun_Media_(SM)', u'Faixa_Tempo_Emprego',
                        u'Escolaridade_apos_2005', u'Qtd_Hora_Contr', u'Idade',
                        u'Ind_CEI_Vinculado', u'Ind_Simples', u'Mes_Admissao',
                        u'Mes_Desligamento', u'Mun_Trab', u'Municipio', u'Nacionalidade',
                        u'Natureza_Juridica', u'Ind_Portador_Defic', u'Qtd_Dias_Afastamento',
                        u'Raca_Cor', u'Vl_Remun_Dezembro_Nom',
                        u'Vl_Remun_Dezembro_(SM)', u'Vl_Remun_Media_Nom',
                        u'Vl_Remun_Media_(SM)', u'CNAE_2.0_Subclasse', u'Sexo_Trabalhador',
                        u'Tamanho_Estabelecimento', u'Tempo_Emprego', u'Tipo_Admissao',
                        u'Tipo_Estab', u'Tipo_Estab.1', u'Tipo_Defic', u'Tipo_Vinculo',
                        u'IBGE_Subsetor', u'Vl_Rem_Janeiro_CC', u'Vl_Rem_Fevereiro_CC',
                        u'Vl_Rem_Marco_CC', u'Vl_Rem_Abril_CC', u'Vl_Rem_Maio_CC',
                        u'Vl_Rem_Junho_CC', u'Vl_Rem_Julho_CC', u'Vl_Rem_Agosto_CC',
                        u'Vl_Rem_Setembro_CC', u'Vl_Rem_Outubro_CC', u'Vl_Rem_Novembro_CC',
                        u'Ano_Chegada_Brasil']
        self.variaveis = {
            u'Causa_Afastamento_1': {10: 'Acidente de trabalho', 20: 'Acidente de trabalho Trajeto',
                                     30: 'Doença relacionada ao trabalho', 40: 'Doença não relacionada ao trabalho',
                                     50: 'Licensa Maternidade', 60: 'Servico Militar', 70: 'Licenca sem vencimento',
                                     99: 'Sem Afastamentos', -1: 'Ignorado'},
            u'Causa_Afastamento_2': {10: 'Acidente de trabalho', 20: 'Acidente de trabalho Trajeto',
                                     30: 'Doença relacionada ao trabalho', 40: 'Doença não relacionada ao trabalho',
                                     50: 'Licensa Maternidade', 60: 'Servico Militar', 70: 'Licenca sem vencimento',
                                     99: 'Sem Afastamentos', -1: 'Ignorado'},
            u'Causa_Afastamento_3': {10: 'Acidente de trabalho', 20: 'Acidente de trabalho Trajeto',
                                     30: 'Doença relacionada ao trabalho', 40: 'Doença não relacionada ao trabalho',
                                     50: 'Licensa Maternidade', 60: 'Servico Militar', 70: 'Licenca sem vencimento',
                                     99: 'Sem Afastamentos', -1: 'Ignorado'},
            u'Vínculo_Ativo_31/12': {0: 'Não', 1: 'Sim'},
            u'Faixa_Etária': {1: '10 A 14 anos', 2: '15 A 17 anos', 3: '18 A 24 anos', 4: '25 A 29 anos',
                              5: '30 A 39 anos', 6: '40 A 49 anos', 7: '50 A 64 anos', 8: '65 anos ou mais',
                              99: 'Sem significado no dicionário oficial'},
            u'Faixa_Hora_Contrat': {1: 'Até 12 horas', 2: '13 a 15 horas', 3: '16 a 20 horas', 4: '21 a 30 horas',
                                    5: '31 a 40 horas', 6: '41 a 44 horas'},
            u'Faixa_Remun_Dezem_(SM)': {0: 'Até 0,50 salários mínimos', 1: 'Até 0,50 salários mínimos',
                                        2: '0,51 a 1,00 salários mínimos', 3: '1,01 a 1,50 salários mínimos',
                                        4: '1,51 a 2,00 salários mínimos', 5: '2,01 a 3,00 salários mínimos',
                                        6: '3,01 a 4,00 salários mínimos', 7: '4,01 a 5,00 salários mínimos',
                                        8: '5,01 a 7,00 salários mínimos', 9: '7,01 a 10,00 salários mínimos',
                                        10: '10,01 a 15,00 salários mínimos', 11: '15,01 a 20,00 salários mínimos',
                                        12: 'Mais de 20,00 salários mínimos'},
            u'Faixa_Remun_Média_(SM)': {0: 'Até 0,50 salários mínimos',
                                        1: '0,51 a 1,00 salários mínimos',
                                        2: '1,01 a 1,50 salários mínimos',
                                        3: '1,51 a 2,00 salários mínimos',
                                        4: '2,01 a 3,00 salários mínimos',
                                        5: '3,01 a 4,00 salários mínimos',
                                        6: '4,01 a 5,00 salários mínimos',
                                        7: '5,01 a 7,00 salários mínimos',
                                        8: '7,01 a 10,00 salários mínimos',
                                        9: '10,01 a 15,00 salários mínimos',
                                        10: '15,01 a 20,00 salários mínimos',
                                        11: 'Mais de 20,00 salários mínimos', },
            u'Faixa_Tempo_Emprego': {1: 'até 2,9 meses',
                                     2: '3,0 a 5,9 meses',
                                     3: '6,0 a 11,9 meses',
                                     4: '12,0 a 23,9 meses',
                                     5: '24,0 a 35,9 meses',
                                     6: '36,0 a 59,9 meses',
                                     7: '60,0 a 119,9 meses',
                                     8: '120,0 ou mais meses', },
            u'Escolaridade_após_2005': {1: u'Analfabeto', 2: u'Até o 5 ano incompleto do ensino fundamental',
                                        3: u'5 ano completo do ensino fundamental',
                                        4: u'Do 6 ao 9 ano incompleto do ensino fundamental',
                                        5: u'Ensino fundamental completo', 6: u'Ensino médio incompleto',
                                        7: u'Ensino médio completo', 8: u'Educacão superior incompleta',
                                        9: u'Educacão superior completa', 10: u'Mestrado completo',
                                        11: u'Doutorado completo', -1: u'Ignorado'},
            u'Ind_CEI_Vinculado': {0: 'Não', 1: 'Sim'},
            u'Ind_Simples': {0: 'Não', 1: 'Sim'},
            u'Nacionalidade': {
                10: "Brasileira",
                20: "Naturalidade Brasileira",
                21: "Argentina",
                22: "Boliviana",
                23: "Chilena",
                24: "Paraguaia",
                25: "Uruguaia",
                26: "Venezuelano",
                27: "Colombiano",
                28: "Peruano",
                29: "Equatoriano",
                30: "Alemã",
                31: "Belga",
                32: "Britânica",
                34: "Canadense",
                35: "Espanhola",
                36: "Norte-Americana",
                37: "Francesa",
                38: "Suíça",
                39: "Italiana",
                40: "Haitiano",
                41: "Japonesa",
                42: "Chinesa",
                43: "Coreana",
                44: "Russo",
                45: "Portuguesa",
                46: "Paquistanês",
                47: "Indiano",
                48: "Outras Latino-Americanas",
                49: "Outras Asiáticas",
                50: "Outras Nacionalidades",
                51: "Outros Europeus",
                59: "Bengalesa",
                60: "Angolano",
                61: "Congolês",
                62: "Sul-Africano",
                63: "Ganesa",
                64: "Senegalesa",
                70: "Outros Africanos",
                80: "Outros",
                -1: "Ignorado"
            },
            u'Natureza_Jurídica': {
                -1: 'IGNORADO',
                1015: 'POD EXEC FE',
                1023: 'POD EXEC ES',
                1031: 'POD EXEC MU',
                1040: 'POD LEG FED',
                1058: 'POD LEG EST',
                1066: 'POD LEG MUN',
                1074: 'POD JUD FED',
                1082: 'POD JUD EST',
                1104: 'AUTARQ FED',
                1112: 'AUTARQ EST',
                1120: 'AUTARQ MUN',
                1139: 'FUNDAC FED',
                1147: 'FUNDAC EST',
                1155: 'FUNDAC MUN',
                1163: 'ORG AUT FED',
                1171: 'ORG AUT EST',
                1180: 'ORG AUT MUN',
                1198: 'COM POLINAC',
                1201: 'FUNDO PUBLIC',
                1210: 'ASSOC PUBLIC',
                2011: 'EMP PUB',
                2038: 'SOC MISTA',
                2046: 'SA ABERTA',
                2054: 'SA FECH',
                2062: 'SOC QT LTDA',
                2070: 'SOC COLETV',
                2076: 'SOC COLETV07',
                2089: 'SOC COMD SM',
                2097: 'SOC COMD AC',
                2100: 'SOC CAP IND',
                2119: 'SOC CIVIL',
                2127: 'SOC CTA PAR',
                2135: 'FRM MER IND',
                2143: 'COOPERATIVA',
                2151: 'CONS EMPRES',
                2160: 'GRUP SOC',
                2178: 'FIL EMP EXT',
                2194: 'FIL ARG-BRA',
                2208: 'ENT ITAIPU',
                2216: 'EMP DOM EXT',
                2224: 'FUN INVEST',
                2232: 'SOC SIMP PUR',
                2240: 'SOC SIMP LTD',
                2259: 'SOC SIMP COL',
                2267: 'SOC SIMP COM',
                2275: 'EMPR BINAC',
                2283: 'CONS EMPREG',
                2291: 'CONS SIMPLES',
                3034: 'CARTORIO',
                3042: 'ORG SOCIAL',
                3050: 'OSCIP',
                3069: 'OUT FUND PR',
                3077: 'SERV SOC AU',
                3085: 'CONDOMIN',
                3093: 'UNID EXEC',
                3107: 'COM CONC',
                3115: 'ENT MED ARB',
                3123: 'PART POLIT',
                3130: 'ENT SOCIAL',
                3131: 'ENT SOCIAL07',
                3204: 'FIL FUN EXT',
                3212: 'FUN DOM EXT',
                3220: 'ORG RELIG',
                3239: 'COMUN INDIG',
                3247: 'FUNDO PRIVAD',
                3999: 'OUTR ORG',
                4014: 'EMP IND IMO',
                4022: 'SEG ESPEC',
                4080: 'CONTR IND',
                4081: 'CONTR IND07',
                4090: 'CAN CARG POL',
                4111: 'LEILOEIRO',
                5002: 'ORG INTERN',
                5010: 'ORG INTERNAC',
                5029: 'REPR DIPL ES',
                5037: 'OUT INST EXT'
            },
            u'Ind_Portador_Defic': {0: 'Não', 1: 'Sim'},
            u'Raça_Cor': {-1: 'Ignorado',
                          1: 'Indígena',
                          2: 'Branca',
                          4: 'Preta',
                          6: 'Amarela',
                          8: 'Parda',
                          9: 'Não identificado',
                          99: 'Sem significado no dicionário oficial'},
            u'Sexo_Trabalhador': {
                1: 'Masculino',
                2: 'Feminino',
                -1: 'Ignorado'
            },
            u'Tamanho_Estabelecimento': {
                -1: 'IGNORADO',
                1: 'ZERO funcionários',
                2: 'até 4 funcionários',
                3: 'de 5 a 9 funcionários',
                4: 'de 10 a 19 funcionários',
                5: 'de 20 a 49 funcionários',
                6: 'de 50 a 99 funcionários',
                7: 'de 100 a 249 funcionários',
                8: 'de 250 a 499 funcionários',
                9: 'de 500 a 999 funcionários',
                10: '1000 ou mais funcionários'},
            u'Tipo_Admissão': {-1: 'IGNORADO',
                               0: 'NAO ADM ANO',
                               1: 'PRIM EMPREGO',
                               2: 'REEMPREGO',
                               3: 'TRANS C/ONUS',
                               4: 'TRANS S/ONUS',
                               5: 'OUTROS',
                               6: 'REINTEGRACAO',
                               7: 'RECONDUCAO',
                               8: 'REVERSAO',
                               9: 'EXERC PROVIS',
                               10: 'REQUISICAO'},
            u'Tipo_Estab': {1: 'CNPJ', 3: 'CEI', 9: 'Não identificado', -1: 'Ignorado'},
            u'Tipo_Defic': {
                -1: 'IGNORADO',
                0: 'NAO DEFIC',
                1: 'FISICA',
                2: 'AUDITIVA',
                3: 'VISUAL',
                4: 'MENTAL',
                5: 'MULTIPLA',
                6: 'REABILITADO'},
            u'Tipo_Vínculo': {-1: 'IGNORADO',
                              10: 'CLT U/PJ IND',
                              15: 'CLT U/PF IND',
                              20: 'CLT R/PJ IND',
                              25: 'CLT R/PF IND',
                              30: 'ESTATUTARIO',
                              31: 'ESTAT RGPS',
                              35: 'ESTAT N/EFET',
                              40: 'AVULSO',
                              50: 'TEMPORARIO',
                              55: 'APREND CONTR',
                              60: 'CLT U/PJ DET',
                              65: 'CLT U/PF DET',
                              70: 'CLT R/PJ DET',
                              75: 'CLT R/PF DET',
                              80: 'DIRETOR',
                              90: 'CONT PRZ DET',
                              95: 'CONT TMP DET',
                              96: 'CONT LEI EST',
                              97: 'CONT LEI MUN'},
            u'Mês_Admissão': {
                0: 'Não admitido no ano',
                1: 'Janeiro',
                2: 'Fevereiro',
                3: 'Março',
                4: 'Abril',
                5: 'Maio',
                6: 'Junho',
                7: 'Julho',
                8: 'Agosto',
                9: 'Setembro',
                10: 'Outubro',
                11: 'Novembro',
                12: 'Dezembro'},

            u'Mês_Desligamento': {
                0: 'Não admitido no ano',
                1: 'Janeiro',
                2: 'Fevereiro',
                3: 'Março',
                4: 'Abril',
                5: 'Maio',
                6: 'Junho',
                7: 'Julho',
                8: 'Agosto',
                9: 'Setembro',
                10: 'Outubro',
                11: 'Novembro',
                12: 'Dezembro'},

            u'Motivo_Desligamento': {10: 'Rescisão com justa causa por iniciativa do empregador ou servidor demitido',
                                     11: 'Rescisão sem justa causa por iniciativa do empregador.',
                                     12: 'Término do contrato de trabalho.',
                                     20: 'Rescisão com justa causa por iniciativa do empregado (rescisão indireta).',
                                     21: 'Rescisão sem justa causa por iniciativa do empregado ou exoneração a pedido',
                                     22: 'Posse em outro cargo inacumulável (específico para servidor público)',
                                     30: 'Transferência de empregado entre estabelecimentos da mesma empresa ou para outra empresa, com ônus para a cedente',
                                     31: 'Transferência de empregado entre estabelecimentos da mesma empresa ou para outra empresa, sem ônus para a cedente',
                                     32: 'Readaptação ou redistribuição (específico para servidor publico)',
                                     33: 'Cessão',
                                     34: 'Redistribuição (específico para servidor publico)',
                                     40: 'Mudança de regime trabalhista.',
                                     50: 'Reforma de militar para a reserva remunerada.',
                                     60: 'Falecimento.',
                                     62: 'Falecimento decorrente de acidente do trabalho típico (que ocorre no exercício de atividades profissionais a serviço da empresa)',
                                     63: 'Falecimento decorrente de acidente do trabalho de trajeto (ocorrido no trajeto residência:trabalho:residência)',
                                     64: 'Falecimento decorrente de doença profissional.',
                                     70: 'Aposentadoria por tempo de serviço, com rescisão contratual.',
                                     71: 'Aposentadoria por tempo de serviço, sem rescisão contratual.',
                                     72: 'Aposentadoria por idade, com rescisão contratual.',
                                     73: 'Aposentadoria por invalidez, decorrente de acidente do trabalho.',
                                     74: 'Aposentadoria por invalidez, decorrente de doença profissional.',
                                     75: 'Aposentadoria compulsória.',
                                     76: 'Aposentadoria por invalidez, exceto a decorrente de doença profissional ou acidente do trabalho.',
                                     78: 'Aposentadoria por idade, sem rescisão contratual.',
                                     79: 'Aposentadoria especial, com rescisão contratual.',
                                     80: 'Aposentadoria especial, sem rescisão contratual.',
                                     0: 'Não desligado no ano'},

            u'IBGE_Subsetor': {
                1: 'Extrativa mineral',
                2: 'Ind\xc3\xbastria de produtos minerais nao met\xc3\xa1licos',
                3: 'Ind\xc3\xbastria metal\xc3\xbargica',
                4: 'Ind\xc3\xbastria mec\xc3\xa2nica',
                5: 'Ind\xc3\xbastria do material el\xc3\xa9trico e de comunica\xc3\xa7oes',
                6: 'Ind\xc3\xbastria do material de transporte',
                7: 'Ind\xc3\xbastria da madeira e do mobili\xc3\xa1rio',
                8: 'Ind\xc3\xbastria do papel, papelao, editorial e gr\xc3\xa1fica',
                9: 'Ind. da borracha, fumo, couros, peles, similares, ind. diversas',
                10: 'Ind. qu\xc3\xadmica de produtos farmac\xc3\xaauticos, veterin\xc3\xa1rios, perfumaria',
                11: 'Ind\xc3\xbastria t\xc3\xaaxtil do vestu\xc3\xa1rio e artefatos de tecidos',
                12: 'Ind\xc3\xbastria de cal\xc3\xa7ados',
                13: 'Ind\xc3\xbastria de produtos aliment\xc3\xadcios, bebidas e \xc3\xa1lcool et\xc3\xadlico',
                14: 'Servi\xc3\xa7os industriais de utilidade p\xc3\xbablica',
                15: 'Constru\xc3\xa7ao civil',
                16: 'Com\xc3\xa9rcio varejista',
                17: 'Com\xc3\xa9rcio atacadista',
                18: 'Institui\xc3\xa7oes de cr\xc3\xa9dito, seguros e capitaliza\xc3\xa7ao',
                19: 'Com. e administra\xc3\xa7ao de im\xc3\xb3veis, valores mobili\xc3\xa1rios, serv. T\xc3\xa9cnico',
                20: 'Transportes e comunica\xc3\xa7oes',
                21: 'Serv. de alojamento, alimenta\xc3\xa7ao, repara\xc3\xa7ao, manuten\xc3\xa7ao, reda\xc3\xa7ao',
                22: 'Servi\xc3\xa7os m\xc3\xa9dicos, odontol\xc3\xb3gicos e veterin\xc3\xa1rios',
                23: 'Ensino',
                24: 'Administra\xc3\xa7ao p\xc3\xbablica direta e aut\xc3\xa1rquica',
                25: 'Agricultura, silvicultura, cria\xc3\xa7ao de animais, extrativismo vegetal'},
            u'CBO_Ocupação_2002': cbo_ocup(),
            u'CNAE_2.0_Subclasse': cnae2sub_dic(),
            u'CNAE_95_Classe': canae1_dic(),
            u'Mun_Trab': municipios_dic(),
            u'Município': municipios_dic(),

        }
        self.ano = ano
        self.avoid = ['Bairros SP', 'Bairros Fortaleza', 'Bairros RJ', 'Distritos SP', u'Regiões Adm DF',
                      'CNAE 2.0 Classe']
        self.destino_transform = '/var/tmp/solr_front/collections/rais/' + str(self.ano) + '/transform/'

    def pega_arquivos_ano(self):
        var = '/var/tmp/solr_front/collections/rais/' + str(self.ano) + '/download/'
        for root, dirs, files in os.walk(var):
            for f in files:
                if f.endswith(".txt") and f.startswith('SP'):
                    self.output_lenght = 0
                    self.f = f.split('.')[0]
                    arquivo = open(os.path.join(root, f), 'r')
                    self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, f) + ' |wc -l')[1]
                    print 'Arquivo {} de entrada possui {} linhas de informacao'.format(f, int(self.input_lenght))
                    iterdf = pd.read_csv(arquivo, sep=';', chunksize=200000, encoding='latin-1', low_memory=False)
                    # iterdf = pd.read_csv(arquivo, sep=';', nrows=1000, chunksize=500, encoding='latin-1')
                    self.c = 0
                    for df in iterdf:
                        nfile = self.destino_transform + self.f + '_' + str(self.c) + '.csv'
                        df = self.resolve_dicionario(df)
                        try:
                            os.makedirs(self.destino_transform)
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                raise
                        df.to_csv(nfile, sep=';', line_terminator='\n', index=False,
                                  encoding='utf8', quoting=csv.QUOTE_ALL, chunksize=100001)
                        self.output_lenght += int(commands.getstatusoutput('cat ' + nfile + ' |wc -l')[1])
                        print 'Arquivo {} de saida foi criado'.format(
                            (self.f + '_' + str(self.c) + '.csv'))
                        self.c += 1

                    with open(self.destino_transform + '_log.txt', 'a') as logfile:
                        logfile.write('################\n')
                        logfile.write('Log gerado em {}\n'.format(self.horas.strftime("%Y-%m-%d %H:%M")))
                        logfile.write(
                            'Arquivo {} de entrada possui {} linhas de informacao\n'.format(f, int(self.input_lenght)))
                        logfile.write('O arquivo de saida possui {} linhas de informacao\n'.format(
                            (int(self.output_lenght) + 1) - self.c))
                        logfile.write('################\n')

                    print 'Arquivo de saida possui {} linhas de informacao'.format(
                        (int(self.output_lenght) + 1) - self.c)
                    print 'FIM'

                    # os.remove(os.path.join(root, f))

    def resolve_dicionario(self, df):

        for item in self.avoid:
            del (df[item])
        df.columns = df.columns.str.replace(' ', '_')

        df['Idade_facet'] = df.Idade.apply(facet_idade)
        df['ID'] = [self.f + '_' + str(self.c) + '_' + str(i + 1) for i in range(df.index.size)]
        df['Regiao_moradia'] = df[u'Município'].apply(find_regiao)
        df['Regiao_trabalho'] = df['Mun_Trab'].apply(find_regiao)
        df.loc[df[u'CBO_Ocupação_2002'] == '0000-1', u'CBO_Ocupação_2002'] = -1  #

        for k, v in self.variaveis.items():
            try:
                df[k] = df[k].astype('int')  #
                df[k] = df[k].map(v).fillna(df[k])
            except KeyError:
                df[k] = 'Não disponivel'

        df['UF_moradia'] = df[u'Município'].str.split('-').str.get(0)
        df[u'Município'] = df[u'Município'].str.split('-').str.get(1)
        df['UF_trabalho'] = df['Mun_Trab'].str.split('-').str.get(0)
        df['Mun_Trab'] = df['Mun_Trab'].str.split('-').str.get(1)
        df['Geografico_moradia_facet'] = df['Regiao_moradia'] + '|' + df['UF_moradia'] + '|' + df[u'Município']
        df['Geografico_trabalho_facet'] = df['Regiao_trabalho'] + '|' + df['UF_trabalho'] + '|' + df['Mun_Trab']
        df['Ano'] = self.ano
        df['Ano_facet'] = gYear(self.ano)
        df['Ano_chegada_facet'] = df['Ano_Chegada_Brasil'].apply(gYear)

        salarios = [u'Vl_Remun_Dezembro_Nom', u'Vl_Remun_Dezembro_(SM)', u'Vl_Remun_Média_Nom', u'Vl_Remun_Média_(SM)',
                    u'Tempo_Emprego', u"Vl_Rem_Janeiro_CC", u"Vl_Rem_Fevereiro_CC", u"Vl_Rem_Abril_CC",
                    u"Vl_Rem_Maio_CC",
                    u"Vl_Rem_Junho_CC", u"Vl_Rem_Julho_CC", u"Vl_Rem_Agosto_CC", u"Vl_Rem_Setembro_CC",
                    u"Vl_Rem_Outubro_CC",
                    u"Vl_Rem_Novembro_CC", u"Vl_Rem_Março_CC"]
        for s in salarios:
            try:
                df[s] = df[s].str.replace(',', '.')
                df[s] = df[s].astype('float')
            except:
                raise

        return df


def rais_transform():
    try:
        PATH_ORIGIN = '/var/tmp/solr_front/collections/rais/'
        anos = [f for f in os.listdir(PATH_ORIGIN) if not f.startswith('.')]
        anos.sort()
        print anos
    except:
        raise
    rais = RaisTransform('2016')
    rais.pega_arquivos_ano()

    # for ano in anos:
    #     rais = RaisTransform(ano)
    #     rais.pega_arquivos_ano()
