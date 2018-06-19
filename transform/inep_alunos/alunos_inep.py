# coding=utf-8
import sys

sys.path.insert(0, '../../../buscador_scripts/')

from utils import gYear,find_regiao
import pandas as pd
import os
import errno
import codecs
import shutil
import csv


class InepVincAlunos(object):

    def __init__(self, ano):
        self.ano = ano

    def pega_arquivo_aluno_por_ano(self):
        """ Para cada ano solicitado, retorna dict com o csv de docentes e csv de ies. """
        var = '/var/tmp/inep/' + str(self.ano) + '/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".CSV"):
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')

                    if file == 'DM_ALUNO.CSV':
                        df_alunos = pd.read_csv(arquivo, sep='|', encoding='cp1252',
                                                chunksize=100000)  # , nrows=100000)
        try:
            return df_alunos
        except:
            pass

    def pega_arquivo_ies_por_ano(self):
        """ Para cada ano solicitado, retorna dict com o csv de docentes e csv de ies. """
        var = '/var/tmp/inep/' + str(self.ano) + '/download/'

        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".CSV"):
                    arquivo = codecs.open(os.path.join(root, file), 'r')  # , encoding='latin-1')

                    if file == 'DM_IES.CSV':
                        df_ies = pd.read_csv(arquivo, sep='|', encoding='cp1252')

        try:
            return df_ies
        except:
            pass

    def merge_alunos_ies(self, df_a, df_i):
        df_merged = df_a.merge(df_i)
        del (df_a)
        del (df_i)
        return df_merged

    def manipula_df(self, df):

        df['GEOGRAFICO_IES_facet'] = df['NO_REGIAO_IES'] + '|' + df['SGL_UF_IES'] + '|' + df['NO_MUNICIPIO_IES']

        df['MANT_IES_facet'] = df['NO_MANTENEDORA'] + '|' + df['NO_IES']

        df['ID'] = str(self.ano) + '_' + df['CO_ALUNO'].astype(str)

        df['Data_Nasc_ALUNO_facet'] = df['NU_ANO_ALUNO_NASC'].astype(str) + '|' + df['NU_MES_ALUNO_NASC'].astype(
            str) + '|' + df['NU_DIA_ALUNO_NASC'].astype(str)

        df['ANO_facet'] = gYear(self.ano)

        return df

    def resolve_dicionarios(self, df):

        repetidas = ['CO_CATEGORIA_ADMINISTRATIVA', 'CO_ORGANIZACAO_ACADEMICA', 'CO_CURSO', 'CO_TURNO_ALUNO',
                     'CO_GRAU_ACADEMICO',
                     'CO_MODALIDADE_ENSINO', 'CO_NIVEL_ACADEMICO', 'CO_OCDE', 'CO_OCDE_AREA_GERAL',
                     'CO_OCDE_AREA_ESPECIFICA',
                     'CO_OCDE_AREA_DETALHADA', 'CO_COR_RACA_ALUNO', 'IN_SEXO_ALUNO', 'CO_NACIONALIDADE_ALUNO',
                     'CO_ALUNO_SITUACAO',
                     'CO_MUNICIPIO_IES', 'CO_UF_IES']

        CHAVES_SIM_NAO = ['IN_ING_VESTIBULAR',
                          'IN_ING_ENEM',
                          'IN_ING_AVALIACAO_SERIADA',
                          'IN_ING_SELECAO_SIMPLIFICADA',
                          'IN_ING_SELECAO_VAGA_REMANESC',
                          'IN_ING_SELECAO_VAGA_PROG_ESPEC',
                          'IN_ING_TRANSF_EXOFFICIO',
                          'IN_ING_DECISAO_JUDICIAL',
                          'IN_ING_CONVENIO_PECG',
                          'IN_RESERVA_VAGAS',
                          'IN_RESERVA_ETNICO',
                          'IN_RESERVA_DEFICIENCIA',
                          'IN_RESERVA_ENSINO_PUBLICO',
                          'IN_RESERVA_RENDA_FAMILIAR',
                          'IN_RESERVA_OUTRA',
                          'IN_FINANC_ESTUDANTIL',
                          'IN_FIN_REEMB_FIES',
                          'IN_FIN_REEMB_ESTADUAL',
                          'IN_FIN_REEMB_MUNICIPAL',
                          'IN_FIN_REEMB_PROG_IES',
                          'IN_FIN_REEMB_ENT_EXTERNA',
                          'IN_FIN_REEMB_OUTRA',
                          'IN_FIN_NAOREEMB_PROUNI_INTEGR',
                          'IN_FIN_NAOREEMB_PROUNI_PARCIAL',
                          'IN_FIN_NAOREEMB_ESTADUAL',
                          'IN_FIN_NAOREEMB_MUNICIPAL',
                          'IN_FIN_NAOREEMB_PROG_IES',
                          'IN_FIN_NAOREEMB_ENT_EXTERNA',
                          'IN_FIN_NAOREEMB_OUTRA',
                          'IN_APOIO_SOCIAL',
                          'IN_APOIO_ALIMENTACAO',
                          'IN_APOIO_BOLSA_PERMANENCIA',
                          'IN_APOIO_BOLSA_TRABALHO',
                          'IN_APOIO_MATERIAL_DIDATICO',
                          'IN_APOIO_MORADIA',
                          'IN_APOIO_TRANSPORTE',
                          'IN_ATIVIDADE_EXTRACURRICULAR',
                          'IN_COMPL_ESTAGIO',
                          'IN_COMPL_EXTENSAO',
                          'IN_COMPL_MONITORIA',
                          'IN_COMPL_PESQUISA',
                          'IN_BOLSA_ESTAGIO',
                          'IN_BOLSA_EXTENSAO',
                          'IN_BOLSA_MONITORIA',
                          'IN_BOLSA_PESQUISA',
                          'IN_ALUNO_PARFOR',
                          'IN_MOBILIDADE_ACADEMICA']

        SIM_NAO = {'0': 'Não', '0.0': 'Não', '1': 'Sim', '1.0': 'Sim', 'nan': 'Não Informado'}
        DEFICIENCIA = ['IN_ALUNO_DEF_TGD_SUPER', 'IN_DEF_AUDITIVA', 'IN_DEF_FISICA', 'IN_DEF_INTELECTUAL',
                       'IN_DEF_MULTIPLA', 'IN_DEF_SURDEZ',
                       'IN_DEF_SURDOCEGUEIRA', 'IN_DEF_BAIXA_VISAO', 'IN_DEF_CEGUEIRA',
                       'IN_DEF_SUPERDOTACAO', 'IN_TGD_AUTISMO_INFANTIL',
                       'IN_TGD_SINDROME_ASPERGER',
                       'IN_TGD_SINDROME_RETT', 'IN_TGD_TRANSTOR_DESINTEGRATIVO']
        DEFICIENCIA_FISICA = {'0': 'Não', '1': 'Sim', '2': 'Não dispõe de informação',
                              'nan': 'Não dispõe de informação'}

        CO_TIPO_ESCOLA_ENS_MEDIO = {'0': 'Privada', '1': 'Pública', '2': 'Não dispõe da informação'}

        CO_MOBILIDADE_ACADEMICA = {'0': 'Nacional', '1': 'Internacional', 'nan': 'Não dispõe da informação'}

        CO_SEMESTRE_CONCLUSAO = {'1': '1°', '2': '2°', 'nan': 'Não dispõe da informação'}

        for rep in repetidas:
            del (df[rep])

        for d in DEFICIENCIA:
            df[d] = df[d].astype(str).replace(DEFICIENCIA_FISICA)

        for sn in CHAVES_SIM_NAO:
            df[sn] = df[sn].astype(str).replace(SIM_NAO)

        df['CO_TIPO_ESCOLA_ENS_MEDIO'] = df['CO_TIPO_ESCOLA_ENS_MEDIO'].astype(str).replace(CO_TIPO_ESCOLA_ENS_MEDIO)
        df['CO_MOBILIDADE_ACADEMICA'] = df['CO_MOBILIDADE_ACADEMICA'].astype(str).replace(CO_MOBILIDADE_ACADEMICA)
        df['CO_SEMESTRE_CONCLUSAO'] = df['CO_SEMESTRE_CONCLUSAO'].astype(str).replace(CO_SEMESTRE_CONCLUSAO)

        municipios = pd.read_csv('../../lista_municipios.csv', sep=';')
        municipios['CÓDIGO DO MUNICÍPIO'] = municipios['CÓDIGO DO MUNICÍPIO'].astype(str)
        municipios['Regiao'] = municipios['CÓDIGO DO MUNICÍPIO'].apply(find_regiao)
        municipios.rename(columns={'CÓDIGO DO MUNICÍPIO': 'CO_MUNICIPIO_NASCIMENTO'}, inplace=True)
        municipios['CO_MUNICIPIO_NASCIMENTO'] = municipios['CO_MUNICIPIO_NASCIMENTO'].astype(float)

        df[['MUNICIPIO_NASCIMENTO', 'UF_NASCIMENTO', 'REG_NASCIMENTO']] = pd.merge(df, municipios,
                                                                                   how='left', on=[
                'CO_MUNICIPIO_NASCIMENTO']).loc[:, ['NOME DO MUNICÍPIO', 'UF', 'Regiao']]
        df['UF_NASCIMENTO'].fillna('Não Informado', inplace=True)
        df['MUNICIPIO_NASCIMENTO'].fillna('Não Informado', inplace=True)
        df['REG_NASCIMENTO'].fillna('Não Informado', inplace=True)
        df['GEOGRAFICO_ALUNO_NASC_facet'] = df['REG_NASCIMENTO'] + '|' + df[
            'UF_NASCIMENTO'] + '|' + df['MUNICIPIO_NASCIMENTO']

        return df

    def gera_csv(self, df, control):

        destino_transform = '/var/tmp/inep/' + str(self.ano) + '/transform'
        csv_file = '/alunos_vinculo_ies_' + str(self.ano) + '.csv'

        if os.path.join(destino_transform,csv_file) and control==0:
            shutil.rmtree(os.path.join(destino_transform), ignore_errors=False, onerror=None)

        try:
            os.makedirs(destino_transform)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        if control == 1:

            df.to_csv(destino_transform + csv_file, sep=';', index=False, encoding='utf8', header=0, mode='a',quoting=csv.QUOTE_NONNUMERIC)
        else:
            df.to_csv(destino_transform + csv_file, sep=';', index=False, encoding='utf8', mode='a',quoting=csv.QUOTE_NONNUMERIC)


if __name__ == "__main__":
    PATH_ORIGEM = '/var/tmp/inep/'
    try:
        anos = os.listdir(PATH_ORIGEM)
        anos.sort()
    except OSError:
        print('Nenhuma pasta encontrada')
        raise
    for ano in anos:
        print(ano)
        try:
            inep_al = InepVincAlunos(ano)
            df_ies = inep_al.pega_arquivo_ies_por_ano()
            chunks_a = inep_al.pega_arquivo_aluno_por_ano()
            df_next = next(chunks_a)
            df_merged = inep_al.merge_alunos_ies(df_next, df_ies)
            df_merged = inep_al.manipula_df(df_merged)
            df_merged = inep_al.resolve_dicionarios(df_merged)
            inep_al.gera_csv(df_merged,0)
            for chunk in chunks_a:
                df_merged = inep_al.merge_alunos_ies(chunk, df_ies)
                df_merged = inep_al.manipula_df(df_merged)
                df_merged = inep_al.resolve_dicionarios(df_merged)
                inep_al.gera_csv(df_merged,1)


            print('Arquivo do ano, {} finalizado'.format(ano))
        except:
            print('Arquivo do ano, {} não encontrado'.format(ano))
            raise
