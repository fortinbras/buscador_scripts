# coding=utf-8
# TODO ano inicio , termino facet
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
import datetime


class Enade(object):

    def __init__(self, year):
        self.date = datetime.datetime.now()
        self.ano = year
        self.input_lenght = 0
        self.output_length = 0
        self.CO_GRUPO = 0
        self.colunas = [
            'NU_ANO',
            'CO_IES',
            'CO_CATEGAD',
            'CO_ORGACAD',
            'CO_GRUPO',
            'CO_CURSO',
            'CO_MODALIDADE',
            'CO_MUNIC_CURSO',
            'CO_UF_CURSO',
            'CO_REGIAO_CURSO',
            'NU_IDADE',
            'TP_SEXO',
            'ANO_FIM_2G',
            'ANO_IN_GRAD',
            'TP_SEMESTRE',
            'IN_MATUT',
            'IN_VESPER',
            'IN_NOTURNO',
            'ID_STATUS',
            'AMOSTRA',
            'QE_I01',
            'QE_I02',
            'QE_I03',
            'QE_I04',
            'QE_I05',
            'QE_I06',
            'QE_I07',
            'QE_I08',
            'QE_I09',
            'QE_I10',
            'QE_I11',
            'QE_I12',
            'QE_I13',
            'QE_I14',
            'QE_I15',
            'QE_I16',
            'QE_I17',
            'QE_I18',
            'QE_I19',
            'QE_I20',
            'QE_I21',
            'QE_I22',
            'QE_I23',
            'QE_I24',
            'QE_I25',
            'QE_I26',
        ]
        self.CO_CATEGAD = {
            '93': 'Pessoa Jurídica de Direito Público - Federal',
            '115': 'Pessoa Jurídica de Direito Público - Estadual',
            '116': 'Pessoa Jurídica de Direito Público - Municipal',
            '118': 'Pessoa Jurídica de Direito Privado - Com fins lucrativos - Sociedade Civil',
            '121': 'Pessoa Jurídica de Direito Privado - Sem fins lucrativos - Fundação',
            '10001': 'Pessoa Jurídica de Direito Público - Estadual',
            '10002': 'Pessoa Jurídica de Direito Público - Federal',
            '10003': 'Pessoa Jurídica de Direito Público - Municipal',
            '10004': 'Pessoa Jurídica de Direito Privado - Com fins lucrativos - Associação de Utilidade Pública',
            '10005': 'Privada com fins lucrativos',
            '10006': 'Pessoa Jurídica de Direito Privado - Com fins lucrativos - Sociedade Mercantil ou Comercial',
            '10007': 'Pessoa Jurídica de Direito Privado - Sem fins lucrativos - Associação de Utilidade Pública',
            '10008': 'Privada sem fins lucrativos',
            '10009': 'Pessoa Jurídica de Direito Privado - Sem fins lucrativos - Sociedade',
            '17634': 'Fundação Pública de Direito Privado Municípal', }
        self.CO_ORGACAD = {
            '10019': 'Centro Federal de Educação Tecnológica',
            '10020': 'Centro Universitário',
            '10022': 'Faculdade',
            '10026': 'Instituto Federal de Educação, Ciência e Tecnologia',
            '10028': 'Universidade', }
        self.CO_MODALIDADE = {
            '0': 'EAD',
            '1': 'Presencial'}
        self.QE_I01 = {
            'A': 'Solteiro(a)',
            'B': 'Casado(a)',
            'C': 'Separado(a) judicialmente/divorciado(a)',
            'D': 'Viúvo(a)',
            'E': 'Outro'
        }
        self.QE_I02 = {
            'A': 'Branca',
            'B': 'Preta',
            'C': 'Amarela',
            'D': 'Parda',
            'E': 'Indígena',
            'F': 'Não quero declarar',
        }
        self.QE_I08 = {
            'A': 'até R$ 1.320,00',
            'B': 'R$ 1.320,01 a R$ 2.640,00',
            'C': 'R$ 2.640,01 a R$ 3.960,00',
            'D': 'R$ 3.960,01 a R$ 5.280,00',
            'E': 'R$ 5.280,01 a R$ 8.800,00',
            'F': 'R$ 8.800,01 a R$ 26.400,00',
            'G': 'mais que R$ 26.400,00'
        }
        self.QE_I04 = {
            'A': 'Nenhuma',
            'B': 'Ensino Fundamental: 1º ao 5º ano (1ª a 4ª série)',
            'C': 'Ensino Fundamental: 6º ao 9º ano (5ª a 8ª série)',
            'D': 'Ensino Médio',
            'E': 'Ensino Superior - Graduação',
            'F': 'Pós-graduação',

        }
        self.QE_I05 = {
            'A': 'Nenhuma',
            'B': 'Ensino fundamental: 1º ao 5º ano (1ª a 4ª série)',
            'C': 'Ensino fundamental: 6º ao 9º ano (5ª a 8ª série)',
            'D': 'Ensino médio',
            'E': 'Ensino Superior - Graduação',
            'F': 'Pós-graduação',
        }
        self.QE_I06 = {
            'A': 'Em casa ou apartamento, sozinho',
            'B': 'Em casa ou apartamento, com pais e/ou parentes',
            'C': 'Em casa ou apartamento, com cônjuge e/ou filhos',
            'D': 'Em casa ou apartamento, com outras pessoas (incluindo república)',
            'E': 'Em alojamento universitário da própria instituição',
            'F': 'Em outros tipos de habitação individual ou coletiva (hotel, hospedaria, pensão ou outro)',

        }
        self.QE_I19 = {
            'A': 'Ninguém',
            'B': 'Pais',
            'C': 'Outros membros da família que não os pais',
            'D': 'Professores',
            'E': 'Líder ou representante religioso',
            'F': 'Colegas/Amigos',
            'G': 'Outras pessoas',
        }
        self.QE_I18 = {
            'A': 'Ensino médio tradicional',
            'B': 'Profissionalizante técnico (eletrônica, contabilidade, agrícola, outro)',
            'C': 'Profissionalizante magistério (Curso Normal)',
            'D': 'Educação de Jovens e Adultos (EJA) e/ou Supletivo',
            'E': 'Outra modalidade',
        }
        self.QE_I09 = {
            'A': 'Não tenho renda e meus gastos são financiados por programas governamentais',
            'B': 'Não tenho renda e meus gastos são financiados pela minha família ou por outras pessoas',
            'C': 'Tenho renda, mas recebo ajuda da família ou de outras pessoas para financiar meus gastos',
            'D': 'Tenho renda e não preciso de ajuda para financiar meus gastos',
            'E': 'Tenho renda e contribuo com o sustento da família',
            'F': 'Sou o principal responsável pelo sustento da família',
        }
        self.QE_I10 = {
            'A': 'Não estou trabalhando',
            'B': 'Trabalho eventualmente',
            'C': 'Trabalho até 20 horas semanais',
            'D': 'Trabalho de 21 a 39 horas semanais',
            'E': 'Trabalho 40 horas semanais ou mais',
        }
        self.QE_I11 = {
            'A': 'Nenhum, pois meu curso é gratuito',
            'B': 'Nenhum, embora meu curso não seja gratuito',
            'C': 'ProUni integral',
            'D': 'ProUni parcial, apenas',
            'E': 'FIES, apenas',
            'F': 'ProUni Parcial e FIES',
            'G': 'Bolsa oferecida por governo estadual, distrital ou municipal',
            'H': 'Bolsa oferecida pela própria instituição',
            'I': 'Bolsa oferecida por outra entidade (empresa, ONG, outra)',
            'J': 'Financiamento oferecido pela própria instituição',
            'K': 'Financiamento bancário',
        }
        self.QE_I13 = {
            'A': 'Nenhum',
            'B': 'Bolsa de iniciação científica',
            'C': 'Bolsa de extensão',
            'D': 'Bolsa de monitoria/tutoria',
            'E': 'Bolsa PET',
            'F': 'Outro tipo de bolsa acadêmica',
        }
        self.QE_I14 = {
            'A': 'Não participei',
            'B': 'Sim, Programa Ciência sem Fronteiras',
            'C': 'Sim, programa de intercâmbio financiado pelo Governo Federal (Marca; Brafitec; PLI; outro)',
            'D': 'Sim, programa de intercâmbio financiado pelo Governo Estadual',
            'E': 'Sim, programa de intercâmbio da minha instituição',
            'F': 'Sim, outro intercâmbio não institucional',
        }
        self.QE_I15 = {
            'A': 'Não',
            'B': 'Sim, por critério étnico-racial',
            'C': 'Sim, por critério de renda',
            'D': 'Sim, por ter estudado em escola pública ou particular com bolsa de estudos',
            'E': 'Sim, por sistema que combina dois ou mais critérios anteriores',
            'F': 'Sim, por sistema diferente dos anteriores',
        }
        self.QE_I16 = {
            '11.0': 'Rondônia (RO)',
            '28.0': 'Sergipe (SE)',
            '12.0': 'Acre (AC)',
            '29.0': 'Bahia (BA)',
            '13.0': 'Amazonas (AM)',
            '31.0': 'Minas Gerais (MG)',
            '14.0': 'Roraima (RR)',
            '32.0': 'Espírito Santo (ES)',
            '15.0': 'Pará (PA)',
            '33.0': 'Rio de Janeiro (RJ)',
            '16.0': 'Amapa (AP)',
            '35.0': 'São Paulo (SP)',
            '17.0': 'Tocantins (TO)',
            '41.0': 'Paraná (PR)',
            '21.0': 'Maranhão (MA)',
            '42.0': 'Santa Catarina (SC)',
            '22.0': 'Piauí (PI)',
            '43.0': 'Rio Grande do Sul (RS)',
            '23.0': 'Ceará (CE)',
            '50.0': 'Mato Grosso do Sul (MS)',
            '24.0': 'Rio Grande do Norte (RN)',
            '51.0': 'Mato Grosso (MT)',
            '25.0': 'Paraíba (PB)',
            '52.0': 'Goiás (GO)',
            '26.0': 'Pernambuco (PE)',
            '53.0': 'Distrito Federal (DF)',
            '27.0': 'Alagoas (AL)',
            '99.0': 'Não se aplica',
        }
        self.QE_I17 = {
            'A': 'Todo em escola pública',
            'B': 'Todo em escola privada (particular)',
            'C': 'Todo no exterior',
            'D': 'A maior parte em escola pública',
            'E': 'A maior parte em escola privada (particular)',
            'F': 'Parte no Brasil e parte no exterior',
        }

    def pega_arquivo_ano(self):

        var = '/var/tmp/enade/' + str(self.ano) + '/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".txt"):
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                    self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l')[1]
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
        df_enade['ID'] = ['2014' + '_' + str(i + 1) for i in range(df_enade.index.size)]

        df_enade['ANO_facet'] = df_enade['NU_ANO'].apply(gYear) + '|' + df_enade['NU_ANO'].astype(str)
        df_enade['ANO_FIM_2G_facet'] = df_enade['ANO_FIM_2G'].apply(gYear) + '|' + df_enade['ANO_FIM_2G'].astype(str)
        df_enade['ANO_IN_GRAD_facet'] = df_enade['ANO_IN_GRAD'].apply(gYear) + '|' + df_enade['ANO_IN_GRAD'].astype(str)
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
        destino_transform = '/var/tmp/enade/' + str(self.ano) + '/transform'
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
    PATH_ORIGEM = '/var/tmp/enade/'
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
#     PATH_ORIGEM = '/var/tmp/enade/'
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
