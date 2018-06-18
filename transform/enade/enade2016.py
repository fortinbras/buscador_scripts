# coding=utf-8

import pandas as pd
import os, errno
import codecs
from utils.utils import gYear, find_regiao


class Enade(object):

    def __init__(self, ano):
        self.ano = ano
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

    def pega_arquivo_ano(self, ano):

        """ Para cada ano solicitado, retorna dict com o csv de docentes e csv de ies. """
        var = '/var/tmp/enade/' + str(ano) + '/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".txt"):
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                    df_enade = pd.read_csv(arquivo, sep=';', low_memory=False)
                    df_enade = df_enade.loc[:, self.colunas]

        try:
            return df_enade
        except:
            pass

    def resolver_dicionario_2015(self):
        df_enade = self.pega_arquivo_ano(self.ano)
        CO_CATEGAD = {
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
        CO_ORGACAD = {
            '10019': 'Centro Federal de Educação Tecnológica',
            '10020': 'Centro Universitário',
            '10022': 'Faculdade',
            '10026': 'Instituto Federal de Educação, Ciência e Tecnologia',
            '10028': 'Universidade', }
        CO_GRUPO = {'5': 'MEDICINA VETERINÁRIA',
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
        CO_MODALIDADE = {
            '0': 'EAD',
            '1': 'Presencial'}
        QE_I01 = {
            'A': 'Solteiro(a)',
            'B': 'Casado(a)',
            'C': 'Separado(a) judicialmente/divorciado(a)',
            'D': 'Viúvo(a)',
            'E': 'Outro'
        }
        QE_I02 = {
            'A': 'Branca',
            'B': 'Preta',
            'C': 'Amarela',
            'D': 'Parda',
            'E': 'Indígena',
            'F': 'Não quero declarar',
        }
        QE_I08 = {
            'A': 'até R$ 1.320,00',
            'B': 'R$ 1.320,01 a R$ 2.640,00',
            'C': 'R$ 2.640,01 a R$ 3.960,00',
            'D': 'R$ 3.960,01 a R$ 5.280,00',
            'E': 'R$ 5.280,01 a R$ 8.800,00',
            'F': 'R$ 8.800,01 a R$ 26.400,00',
            'G': 'mais que R$ 26.400,00'
        }
        QE_I04 = {
            'A': 'Nenhuma',
            'B': 'Ensino Fundamental: 1º ao 5º ano (1ª a 4ª série)',
            'C': 'Ensino Fundamental: 6º ao 9º ano (5ª a 8ª série)',
            'D': 'Ensino Médio',
            'E': 'Ensino Superior - Graduação',
            'F': 'Pós-graduação',

        }
        QE_I05 = {
            'A': 'Nenhuma',
            'B': 'Ensino fundamental: 1º ao 5º ano (1ª a 4ª série)',
            'C': 'Ensino fundamental: 6º ao 9º ano (5ª a 8ª série)',
            'D': 'Ensino médio',
            'E': 'Ensino Superior - Graduação',
            'F': 'Pós-graduação',
        }
        QE_I06 = {
            'A': 'Em casa ou apartamento, sozinho',
            'B': 'Em casa ou apartamento, com pais e/ou parentes',
            'C': 'Em casa ou apartamento, com cônjuge e/ou filhos',
            'D': 'Em casa ou apartamento, com outras pessoas (incluindo república)',
            'E': 'Em alojamento universitário da própria instituição',
            'F': 'Em outros tipos de habitação individual ou coletiva (hotel, hospedaria, pensão ou outro)',

        }
        QE_I19 = {
            'A': 'Ninguém',
            'B': 'Pais',
            'C': 'Outros membros da família que não os pais',
            'D': 'Professores',
            'E': 'Líder ou representante religioso',
            'F': 'Colegas/Amigos',
            'G': 'Outras pessoas',
        }
        QE_I18 = {
            'A': 'Ensino médio tradicional',
            'B': 'Profissionalizante técnico (eletrônica, contabilidade, agrícola, outro)',
            'C': 'Profissionalizante magistério (Curso Normal)',
            'D': 'Educação de Jovens e Adultos (EJA) e/ou Supletivo',
            'E': 'Outra modalidade',
        }
        QE_I09 = {
            'A': 'Não tenho renda e meus gastos são financiados por programas governamentais',
            'B': 'Não tenho renda e meus gastos são financiados pela minha família ou por outras pessoas',
            'C': 'Tenho renda, mas recebo ajuda da família ou de outras pessoas para financiar meus gastos',
            'D': 'Tenho renda e não preciso de ajuda para financiar meus gastos',
            'E': 'Tenho renda e contribuo com o sustento da família',
            'F': 'Sou o principal responsável pelo sustento da família',
        }
        QE_I10 = {
            'A': 'Não estou trabalhando',
            'B': 'Trabalho eventualmente',
            'C': 'Trabalho até 20 horas semanais',
            'D': 'Trabalho de 21 a 39 horas semanais',
            'E': 'Trabalho 40 horas semanais ou mais',
        }
        QE_I11 = {
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
        QE_I13 = {
            'A': 'Nenhum',
            'B': 'Bolsa de iniciação científica',
            'C': 'Bolsa de extensão',
            'D': 'Bolsa de monitoria/tutoria',
            'E': 'Bolsa PET',
            'F': 'Outro tipo de bolsa acadêmica',
        }
        QE_I14 = {
            'A': 'Não participei',
            'B': 'Sim, Programa Ciência sem Fronteiras',
            'C': 'Sim, programa de intercâmbio financiado pelo Governo Federal (Marca; Brafitec; PLI; outro)',
            'D': 'Sim, programa de intercâmbio financiado pelo Governo Estadual',
            'E': 'Sim, programa de intercâmbio da minha instituição',
            'F': 'Sim, outro intercâmbio não institucional',
        }
        QE_I15 = {
            'A': 'Não',
            'B': 'Sim, por critério étnico-racial',
            'C': 'Sim, por critério de renda',
            'D': 'Sim, por ter estudado em escola pública ou particular com bolsa de estudos',
            'E': 'Sim, por sistema que combina dois ou mais critérios anteriores',
            'F': 'Sim, por sistema diferente dos anteriores',
        }
        QE_I16 = {
            '11': 'Rondônia (RO)',
            '28': 'Sergipe (SE)',
            '12': 'Acre (AC)',
            '29': 'Bahia (BA)',
            '13': 'Amazonas (AM)',
            '31': 'Minas Gerais (MG)',
            '14': 'Roraima (RR)',
            '32': 'Espírito Santo (ES)',
            '15': 'Pará (PA)',
            '33': 'Rio de Janeiro (RJ)',
            '16': 'Amapa (AP)',
            '35': 'São Paulo (SP)',
            '17': 'Tocantins (TO)',
            '41': 'Paraná (PR)',
            '21': 'Maranhão (MA)',
            '42': 'Santa Catarina (SC)',
            '22': 'Piauí (PI)',
            '43': 'Rio Grande do Sul (RS)',
            '23': 'Ceará (CE)',
            '50': 'Mato Grosso do Sul (MS)',
            '24': 'Rio Grande do Norte (RN)',
            '51': 'Mato Grosso (MT)',
            '25': 'Paraíba (PB)',
            '52': 'Goiás (GO)',
            '26': 'Pernambuco (PE)',
            '53': 'Distrito Federal (DF)',
            '27': 'Alagoas (AL)',
            '99': 'Não se aplica',
        }
        QE_I17 = {
            'A': 'Todo em escola pública',
            'B': 'Todo em escola privada (particular)',
            'C': 'Todo no exterior',
            'D': 'A maior parte em escola pública',
            'E': 'A maior parte em escola privada (particular)',
            'F': 'Parte no Brasil e parte no exterior',
        }

        municipios = pd.read_csv('../../lista_municipios.csv', sep=';', dtype={'CÓDIGO DO MUNICÍPIO': 'str'})
        municipios = municipios.rename(columns={'CÓDIGO DO MUNICÍPIO': 'CO_MUNIC_CURSO'})
        municipios['REGIAO'] = municipios['CO_MUNIC_CURSO'].apply(find_regiao)
        df_enade[['MUNIC_CURSO', 'UF_CURSO', 'REGIAO_CURSO']] = pd.merge(df_enade, municipios, how='left', on=[
            'CO_MUNIC_CURSO']).loc[:, ['NOME DO MUNICÍPIO', 'UF', 'REGIAO']]


        df_enade['CO_CATEGAD'] = df_enade['CO_CATEGAD'].astype(str).replace(CO_CATEGAD)
        df_enade['CO_ORGACAD'] = df_enade['CO_ORGACAD'].astype(str).replace(CO_ORGACAD)
        df_enade['CO_GRUPO'] = df_enade['CO_GRUPO'].astype(str).replace(CO_GRUPO)
        df_enade['CO_MODALIDADE'] = df_enade['CO_MODALIDADE'].astype(str).replace(CO_MODALIDADE)
        df_enade['ID'] = ['2014' + '_' + str(i + 1) for i in range(df_enade.index.size)]


        df_enade['ANO_FACET'] = df_enade['NU_ANO'].apply(gYear) + '|' + df_enade['NU_ANO'].astype(str)
        df_enade['ANO_FIM_2G_facet'] = df_enade['ANO_FIM_2G'].apply(gYear) + '|' + df_enade['ANO_FIM_2G'].astype(str)
        df_enade['ANO_IN_GRAD_facet'] = df_enade['ANO_IN_GRAD'].apply(gYear) + '|' + df_enade['ANO_IN_GRAD'].astype(str)
        df_enade['GEOGRAFICO_facet'] = df_enade['REGIAO_CURSO'].astype(str) + '|' + df_enade['UF_CURSO'].astype(
            str) + '|' + df_enade['MUNIC_CURSO'].astype(str)


        # PESSOAIS
        df_enade['ESTADO_CIVIL'] = df_enade['QE_I01'].replace(QE_I01)
        df_enade['ESC_PAI'] = df_enade['QE_I04'].replace(QE_I04)
        df_enade['ESC_MAE'] = df_enade['QE_I05'].replace(QE_I05)
        df_enade['MORADIA'] = df_enade['QE_I06'].replace(QE_I06)
        df_enade['INCENTIVO_GRAD'] = df_enade['QE_I19'].replace(QE_I19)
        df_enade['MODALIDADE_2G'] = df_enade['QE_I18'].replace(QE_I18)

        # SOCIOECONOMICAS
        df_enade['COR_RAÇA'] = df_enade['QE_I02'].replace(QE_I02)
        df_enade['RENDA_FAMILIAR'] = df_enade['QE_I08'].replace(QE_I08)
        df_enade['SIT_FINAN'] = df_enade['QE_I09'].replace(QE_I09)
        df_enade['SIT_TRAB'] = df_enade['QE_I10'].replace(QE_I10)

        # BOLSAS
        df_enade['TIPO_BOLSA'] = df_enade['QE_I11'].replace(QE_I11)
        df_enade['TRAJ_ACAD'] = df_enade['QE_I13'].replace(QE_I13)
        df_enade['EC_EXT'] = df_enade['QE_I14'].replace(QE_I14)
        df_enade['ING_GRAD'] = df_enade['QE_I15'].replace(QE_I15)

        # GEOGRAFICO
        df_enade['UF_2G'] = df_enade['QE_I16'].astype(str).replace(QE_I16)
        df_enade['ESCOLA_2G'] = df_enade['QE_I17'].replace(QE_I17)

        del (df_enade['CO_MUNIC_CURSO'])
        del (df_enade['CO_UF_CURSO'])
        del (df_enade['CO_REGIAO_CURSO'])
        del (df_enade['AMOSTRA'])
        del (df_enade['QE_I01'])
        del (df_enade['QE_I02'])
        del (df_enade['QE_I08'])

        return df_enade

    def resolver_dicionario_2016(self):
        df_enade = self.pega_arquivo_ano(self.ano)
        CO_CATEGAD = {
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
        CO_ORGACAD = {
            '10019': 'Centro Federal de Educação Tecnológica',
            '10020': 'Centro Universitário',
            '10022': 'Faculdade',
            '10026': 'Instituto Federal de Educação, Ciência e Tecnologia',
            '10028': 'Universidade', }
        CO_GRUPO = {'5': 'MEDICINA VETERINÁRIA',
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
        CO_MODALIDADE = {
            '0': 'EAD',
            '1': 'Presencial'}
        QE_I01 = {
            'A': 'Solteiro(a)',
            'B': 'Casado(a)',
            'C': 'Separado(a) judicialmente/divorciado(a)',
            'D': 'Viúvo(a)',
            'E': 'Outro'
        }
        QE_I02 = {
            'A': 'Branca',
            'B': 'Preta',
            'C': 'Amarela',
            'D': 'Parda',
            'E': 'Indígena',
            'F': 'Não quero declarar',
        }

        QE_I08 = {
            'A': 'até R$ 1.320,00',
            'B': 'R$ 1.320,01 a R$ 2.640,00',
            'C': 'R$ 2.640,01 a R$ 3.960,00',
            'D': 'R$ 3.960,01 a R$ 5.280,00',
            'E': 'R$ 5.280,01 a R$ 8.800,00',
            'F': 'R$ 8.800,01 a R$ 26.400,00',
            'G': 'mais que R$ 26.400,00'
        }

        QE_I04 = {
            'A': 'Nenhuma',
            'B': 'Ensino Fundamental: 1º ao 5º ano (1ª a 4ª série)',
            'C': 'Ensino Fundamental: 6º ao 9º ano (5ª a 8ª série)',
            'D': 'Ensino Médio',
            'E': 'Ensino Superior - Graduação',
            'F': 'Pós-graduação',

        }

        QE_I05 = {
            'A': 'Nenhuma',
            'B': 'Ensino fundamental: 1º ao 5º ano (1ª a 4ª série)',
            'C': 'Ensino fundamental: 6º ao 9º ano (5ª a 8ª série)',
            'D': 'Ensino médio',
            'E': 'Ensino Superior - Graduação',
            'F': 'Pós-graduação',
        }

        QE_I06 = {
            'A': 'Em casa ou apartamento, sozinho',
            'B': 'Em casa ou apartamento, com pais e/ou parentes',
            'C': 'Em casa ou apartamento, com cônjuge e/ou filhos',
            'D': 'Em casa ou apartamento, com outras pessoas (incluindo república)',
            'E': 'Em alojamento universitário da própria instituição',
            'F': 'Em outros tipos de habitação individual ou coletiva (hotel, hospedaria, pensão ou outro)',

        }

        QE_I19 = {
            'A': 'Ninguém',
            'B': 'Pais',
            'C': 'Outros membros da família que não os pais',
            'D': 'Professores',
            'E': 'Líder ou representante religioso',
            'F': 'Colegas/Amigos',
            'G': 'Outras pessoas',
        }

        QE_I18 = {
            'A': 'Ensino médio tradicional',
            'B': 'Profissionalizante técnico (eletrônica, contabilidade, agrícola, outro)',
            'C': 'Profissionalizante magistério (Curso Normal)',
            'D': 'Educação de Jovens e Adultos (EJA) e/ou Supletivo',
            'E': 'Outra modalidade',
        }

        QE_I09 = {
            'A': 'Não tenho renda e meus gastos são financiados por programas governamentais',
            'B': 'Não tenho renda e meus gastos são financiados pela minha família ou por outras pessoas',
            'C': 'Tenho renda, mas recebo ajuda da família ou de outras pessoas para financiar meus gastos',
            'D': 'Tenho renda e não preciso de ajuda para financiar meus gastos',
            'E': 'Tenho renda e contribuo com o sustento da família',
            'F': 'Sou o principal responsável pelo sustento da família',
        }

        QE_I10 = {
            'A': 'Não estou trabalhando',
            'B': 'Trabalho eventualmente',
            'C': 'Trabalho até 20 horas semanais',
            'D': 'Trabalho de 21 a 39 horas semanais',
            'E': 'Trabalho 40 horas semanais ou mais',
        }

        QE_I11 = {
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

        QE_I13 = {
            'A': 'Nenhum',
            'B': 'Bolsa de iniciação científica',
            'C': 'Bolsa de extensão',
            'D': 'Bolsa de monitoria/tutoria',
            'E': 'Bolsa PET',
            'F': 'Outro tipo de bolsa acadêmica',
        }

        QE_I14 = {
            'A': 'Não participei',
            'B': 'Sim, Programa Ciência sem Fronteiras',
            'C': 'Sim, programa de intercâmbio financiado pelo Governo Federal (Marca; Brafitec; PLI; outro)',
            'D': 'Sim, programa de intercâmbio financiado pelo Governo Estadual',
            'E': 'Sim, programa de intercâmbio da minha instituição',
            'F': 'Sim, outro intercâmbio não institucional',
        }

        QE_I15 = {
            'A': 'Não',
            'B': 'Sim, por critério étnico-racial',
            'C': 'Sim, por critério de renda',
            'D': 'Sim, por ter estudado em escola pública ou particular com bolsa de estudos',
            'E': 'Sim, por sistema que combina dois ou mais critérios anteriores',
            'F': 'Sim, por sistema diferente dos anteriores',
        }

        QE_I16 = {
            '11': 'Rondônia (RO)',
            '28': 'Sergipe (SE)',
            '12': 'Acre (AC)',
            '29': 'Bahia (BA)',
            '13': 'Amazonas (AM)',
            '31': 'Minas Gerais (MG)',
            '14': 'Roraima (RR)',
            '32': 'Espírito Santo (ES)',
            '15': 'Pará (PA)',
            '33': 'Rio de Janeiro (RJ)',
            '16': 'Amapa (AP)',
            '35': 'São Paulo (SP)',
            '17': 'Tocantins (TO)',
            '41': 'Paraná (PR)',
            '21': 'Maranhão (MA)',
            '42': 'Santa Catarina (SC)',
            '22': 'Piauí (PI)',
            '43': 'Rio Grande do Sul (RS)',
            '23': 'Ceará (CE)',
            '50': 'Mato Grosso do Sul (MS)',
            '24': 'Rio Grande do Norte (RN)',
            '51': 'Mato Grosso (MT)',
            '25': 'Paraíba (PB)',
            '52': 'Goiás (GO)',
            '26': 'Pernambuco (PE)',
            '53': 'Distrito Federal (DF)',
            '27': 'Alagoas (AL)',
            '99': 'Não se aplica',
        }

        QE_I17 = {
            'A': 'Todo em escola pública',
            'B': 'Todo em escola privada (particular)',
            'C': 'Todo no exterior',
            'D': 'A maior parte em escola pública',
            'E': 'A maior parte em escola privada (particular)',
            'F': 'Parte no Brasil e parte no exterior',
        }

        municipios = pd.read_csv('../../lista_municipios.csv', sep=';')
        municipios = municipios.rename(columns={'CÓDIGO DO MUNICÍPIO': 'CO_MUNIC_CURSO'})
        municipios['REGIAO'] = municipios['CO_MUNIC_CURSO'].apply(find_regiao)
        df_enade[['MUNIC_CURSO', 'UF_CURSO', 'REGIAO_CURSO']] = pd.merge(df_enade, municipios, how='left', on=[
            'CO_MUNIC_CURSO']).loc[:, ['NOME DO MUNICÍPIO', 'UF', 'REGIAO']]


        df_enade['CO_CATEGAD'] = df_enade['CO_CATEGAD'].astype(str).replace(CO_CATEGAD)
        df_enade['CO_ORGACAD'] = df_enade['CO_ORGACAD'].astype(str).replace(CO_ORGACAD)
        df_enade['CO_GRUPO'] = df_enade['CO_GRUPO'].astype(str).replace(CO_GRUPO)
        df_enade['CO_MODALIDADE'] = df_enade['CO_MODALIDADE'].astype(str).replace(CO_MODALIDADE)
        df_enade['ID'] = ['2014' + '_' + str(i + 1) for i in range(df_enade.index.size)]


        df_enade['ANO_FACET'] = df_enade['NU_ANO'].apply(gYear) + '|' + df_enade['NU_ANO'].astype(str)
        df_enade['ANO_FIM_2G_facet'] = df_enade['ANO_FIM_2G'].apply(gYear) + '|' + df_enade['ANO_FIM_2G'].astype(str)
        df_enade['ANO_IN_GRAD_facet'] = df_enade['ANO_IN_GRAD'].apply(gYear) + '|' + df_enade['ANO_IN_GRAD'].astype(str)
        df_enade['GEOGRAFICO_facet'] = df_enade['REGIAO_CURSO'].astype(str) + '|' + df_enade['UF_CURSO'].astype(
            str) + '|' + df_enade['MUNIC_CURSO'].astype(str)


        # PESSOAIS
        df_enade['ESTADO_CIVIL'] = df_enade['QE_I01'].replace(QE_I01)
        df_enade['ESC_PAI'] = df_enade['QE_I04'].replace(QE_I04)
        df_enade['ESC_MAE'] = df_enade['QE_I05'].replace(QE_I05)
        df_enade['MORADIA'] = df_enade['QE_I06'].replace(QE_I06)
        df_enade['INCENTIVO_GRAD'] = df_enade['QE_I19'].replace(QE_I19)
        df_enade['MODALIDADE_2G'] = df_enade['QE_I18'].replace(QE_I18)

        # SOCIOECONOMICAS
        df_enade['COR_RAÇA'] = df_enade['QE_I02'].replace(QE_I02)
        df_enade['RENDA_FAMILIAR'] = df_enade['QE_I08'].replace(QE_I08)
        df_enade['SIT_FINAN'] = df_enade['QE_I09'].replace(QE_I09)
        df_enade['SIT_TRAB'] = df_enade['QE_I10'].replace(QE_I10)

        # BOLSAS
        df_enade['TIPO_BOLSA'] = df_enade['QE_I11'].replace(QE_I11)
        df_enade['TRAJ_ACAD'] = df_enade['QE_I13'].replace(QE_I13)
        df_enade['EC_EXT'] = df_enade['QE_I14'].replace(QE_I14)
        df_enade['ING_GRAD'] = df_enade['QE_I15'].replace(QE_I15)

        # GEOGRAFICO
        df_enade['UF_2G'] = df_enade['QE_I16'].astype(str).replace(QE_I16)
        df_enade['ESCOLA_2G'] = df_enade['QE_I17'].replace(QE_I17)

        del (df_enade['CO_MUNIC_CURSO'])
        del (df_enade['CO_UF_CURSO'])
        del (df_enade['CO_REGIAO_CURSO'])
        del (df_enade['AMOSTRA'])
        del (df_enade['QE_I01'])
        del (df_enade['QE_I02'])
        del (df_enade['QE_I08'])

        return df_enade




    def gera_csv(self):
        if str(self.ano) == '2016':
            df_enade = self.resolver_dicionario_2016()
        elif str(self.ano) == '2015':
            df_enade = self.resolver_dicionario_2015()
        else:
            pass
        destino_transform = '/var/tmp/enade/' + str(self.ano) + '/transform'
        csv_file = '/enade_' + str(self.ano) + '.csv'
        try:
            os.makedirs(destino_transform)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        df_enade.to_csv(destino_transform + csv_file, sep=';', index=False, encoding='utf8', line_terminator='\n')


if __name__ == "__main__":

    PATH_ORIGEM = '/var/tmp/enade/'
    anos = os.listdir(PATH_ORIGEM)
    anos.sort()
    for ano in anos:
        print(ano)
        try:
            inep_doc = Enade(ano)
            inep_doc.gera_csv()
            print('Arquivo do ano, {} finalizado'.format(ano))
        except:
            print('Arquivo do ano, {} não encontrado'.format(ano))
            pass
