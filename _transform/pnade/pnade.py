# coding=utf-8
import os, errno
import commands, csv
import datetime
import pandas as pd


# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)

class Pnade(object):

    def __init__(self, year):
        self.date = datetime.datetime.now()
        self.ano = year
        self.input_lenght = 0
        self.output_length = 0

    def pega_arquivo_ano(self):
        cols = [x for x in range(0, 60)]
        avoid = ['V0401', 'V0403', 'V0407', 'V0409', 'V0410', 'v0412']
        var = '/var/tmp/pnade/' + str(self.ano) + '/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".csv"):
                    arquivo = open(os.path.join(root, file), 'r')  # , encoding='latin-1')
                    self.input_lenght = commands.getstatusoutput('cat ' + os.path.join(root, file) + ' |wc -l')[1]
                    print 'Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght))
                    df = pd.read_csv(arquivo, sep=';', low_memory=False, usecols=cols)  # , nrows=1000)
                    for item in avoid:
                        del (df[item])

                    return df

    def resolve_dicionario(self):

        df = self.pega_arquivo_ano()
        variaveis = {
            'UF': {11: 'Rondônia', 12: 'Acre', 13: 'Amazonas', 14: 'Roraima',
                   15: 'Pará', 16: 'Amapá', 17: 'Tocantins', 21: 'Maranhão',
                   22: 'Piauí', 23: 'Ceará', 24: 'Rio Grande do Norte', 25: 'Paraíba', 26: 'Pernambuco', 27: 'Alagoas',
                   28: 'Sergipe', 29: 'Bahia', 31: 'Minas Gerais', 32: 'Espírito Santo', 33: 'Rio de Janeiro',
                   35: 'São Paulo', 41: 'Paraná', 42: 'Santa Catarina', 43: 'Rio Grande do Sul',
                   50: 'Mato Grosso do Sul', 51: 'Mato Grosso', 52: 'Goiás', 53: 'Distrito Federal'},
            'V0302': {2: 'Masculino', 4: 'Feminino'},
            'V0402': {1: 'Pessoa de referência', 2: 'Cônjuge', 3: 'Filho', 4: 'Outro parente', 5: 'Agregado',
                      6: 'Pensionista',
                      7: 'Empregado doméstico', 8: 'Parente do empregado doméstico'},
            'V0404': {2: 'Branca', 4: 'Preta', 6: 'Amarela', 8: 'Parda', 0: 'Indigena', 9: 'ND'},
            'V0405': {1: 'Sim', 3: 'Nao', 5: 'Nao sabe'},
            'V0406': {2: 'Sim', 4: 'Nao'},
            'V0408': {2: 'Sim', 4: 'Nao', 6: 'Nao sabe'},
            'V4111': {1: 'Sim', 3: 'Nao, ja viveu antes', 5: 'Nao, nunca viveu antes'},
            'V4112': {1: 'Casamento civil e religioso', 3: 'Só casamento civil',
                      5: 'Só casamento religioso', 7: 'União consensual'},
            'V4011': {1: 'Casado', 3: 'Desquitado(a) ou separado(a) judicialmente',
                      5: 'Divorciado(a)', 7: 'Viuvo', 0: 'Solteiro'},
            'V0501': {1: 'Sim', 3: 'Nao'},
            'V0502': {2: 'Sim', 4: 'Nao'},
            'V5030': {11: 'Rondônia', 12: 'Acre', 13: 'Amazonas', 14: 'Roraima',
                      15: 'Pará', 16: 'Amapá', 17: 'Tocantins', 21: 'Maranhão',
                      22: 'Piauí', 23: 'Ceará', 24: 'Rio Grande do Norte', 25: 'Paraíba', 26: 'Pernambuco',
                      27: 'Alagoas',
                      28: 'Sergipe', 29: 'Bahia', 31: 'Minas Gerais', 32: 'Espírito Santo', 33: 'Rio de Janeiro',
                      35: 'São Paulo', 41: 'Paraná', 42: 'Santa Catarina', 43: 'Rio Grande do Sul',
                      50: 'Mato Grosso do Sul', 51: 'Mato Grosso', 52: 'Goiás', 53: 'Distrito Federal', 88: 'Brasil',
                      98: 'Pais estrangeiro'},
            'V0504': {2: 'Sim', 4: 'Nao'},
            'V0505': {1: 'Sim', 3: 'Nao'},
            'V0601': {1: 'Sim', 3: 'Nao'},
            'V0602': {2: 'Sim', 4: 'Nao'},
            'V6002': {2: 'Publica', 4: 'Privada'},
            'V6020': {2: 'Municipal', 4: 'Estadual', 6: 'Federal'},
            'V6003': {1: 'Regular do ensino fundamental', 2: 'Regular do ensino médio',
                      3: 'Educação de jovens e adultos ou supletivo do ensino fundamental',
                      4: 'Educação de jovens e adultos ou supletivo do ensino médio',
                      5: 'Superior de graduação', 6: 'Alfabetização de jovens e adultos',
                      7: 'Creche', 8: 'Classe de alfabetização - CA',
                      9: 'Maternal, jardim de infância etc.', 10: 'Pré-vestibular',
                      11: 'Mestrado ou doutorado'},
            'V0606': {2: 'Sim', 4: 'Nao'},
        }
        for k, v in variaveis.items():
            df[k].replace(v, inplace=True)

        df['V5030'].fillna(df['UF'], inplace=True)

        return df

    def gera_csv(self):
        df = self.resolve_dicionario()
        destino_transform = '/var/tmp/pnade/' + str(self.ano) + '/transform'
        csv_file = '/pnade_' + str(self.ano) + '.csv'
        log_file = '/pnade_' + str(self.ano) + '.log'
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
            log.write('Arquivo de entrada possui {} linhas de informacao'.format(int(self.input_lenght)))
            log.write("\n")
            log.write('Arquivo de saida possui {} linhas de informacao'.format(int(self.output_length) - 1))
        print('Processamento PNADE {} finalizado, arquivo de log gerado em {}'.format(str(self.ano),
                                                                                      destino_transform + log_file))


def pnade_tranform():
    PATH_ORIGEM = '/var/tmp/pnade/'
    try:
        anos = os.listdir(PATH_ORIGEM)
        anos.sort()
    except OSError:
        print('Nenhuma pasta encontrada')
        raise
    for ano in anos:
        print(ano)
        try:
            pnade = Pnade(ano)
            pnade.gera_csv()
            print('Arquivo do ano, {} finalizado'.format(ano))

        except:
            print 'Arquivo do ano, {} não encontrado'.format(ano)
            raise
        print('Fim!!')
        print('\n')


