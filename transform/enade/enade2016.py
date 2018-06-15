# coding=utf-8

import pandas as pd
import os, errno
import codecs
from utils.utils import gYear,find_regiao


class Enade(object):

    def __init__(self, ano):
        self.ano = ano

    def pega_arquivo_ano(self, ano):
        colunas = [
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
            'IN_GRAD', 'QE_I01',
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
        """ Para cada ano solicitado, retorna dict com o csv de docentes e csv de ies. """
        var = '/var/tmp/enade/' + str(ano) + '/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".txt"):
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                    df_enade = pd.read_csv(arquivo, sep=';')
                    df_enade = df_enade.loc[:, colunas]

        try:
            return df_enade
        except:
            pass

    def resolver_dicionario_2016(self, ano):
        df_enade = self.pega_arquivo_ano(ano)
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
        municipios = pd.read_csv('../../lista_municipios.csv', sep=';')
        municipios = municipios.rename(columns={'CÓDIGO DO MUNICÍPIO': 'CO_MUNIC_CURSO'})
        municipios['Regiao'] = municipios['CO_MUNIC_CURSO'].apply(find_regiao)
        df_enade['CO_CATEGAD'] = df_enade['CO_CATEGAD'].astype(str).replace(CO_CATEGAD)
        df_enade['CO_ORGACAD'] = df_enade['CO_ORGACAD'].astype(str).replace(CO_ORGACAD)
        df_enade['CO_GRUPO'] = df_enade['CO_GRUPO'].astype(str).replace(CO_GRUPO)
        df_enade['CO_MODALIDADE'] = df_enade['CO_MODALIDADE'].astype(str).replace(CO_MODALIDADE)
        df_enade['ID'] = ['2014' + '_' + str(i + 1) for i in range(df_enade.index.size)]
        df_enade[['MUNIC_CURSO', 'UF_CURSO', 'REGIAO_CURSO']] = pd.merge(df_enade, municipios,
                                                                         how='left', on=[
                'CO_MUNIC_CURSO']).loc[:, ['NOME DO MUNICÍPIO', 'UF', 'Regiao']]
        df_enade['Ano_facet'] = gYear(2016)
        df_enade['GEOGRAFICO_facet'] = df_enade['REGIAO_CURSO'].astype(str) + '|' + df_enade['UF_CURSO'].astype(
            str) + '|' + df_enade['MUNIC_CURSO'].astype(str)
        del (df_enade['CO_MUNIC_CURSO'])
        del (df_enade['CO_UF_CURSO'])
        del (df_enade['CO_REGIAO_CURSO'])
        del (df_enade['AMOSTRA'])

        return df_enade

    def gera_csv(self):
        if self.ano == '2016':
            df_enade = self.resolver_dicionario_2016(self.ano)
        else:
            pass
        destino_transform = '/var/tmp/enade/' + str(ano) + '/transform'
        csv_file = '/enade_' + str(ano) + '.csv'
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
