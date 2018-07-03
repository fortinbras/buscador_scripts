# -*- coding: utf-8 -*-
import sys,os

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

import errno, io
import zipfile

"""
Este script faz o downloa dos arquivos do Pnade e descompacta-os na pasta dos respectivos anos.
Deve-se escolher o ano de inicio e o ano final dos arquivos a serem baixados.
Antes de 2010, a nomenclatura e formato dos arquivos nao batem.
"""


def find_zips_pnad():
    from ftplib import FTP

    anos = ['2013', '2014']
    ftp = FTP("ftp.ibge.gov.br")
    ftp.login()
    ftp.cwd('Trabalho_e_Rendimento')
    ftp.cwd('Pesquisa_Nacional_por_Amostra_de_Domicilios_anual')
    ftp.cwd('microdados')
    for ano in anos:
        dir_destino = '/var/tmp/pnade/' + str(ano) + '/download/'
        ano_str = str(ano)
        nome_arquivo = ano_str + '.zip'
        nome_csv = ano_str + '.csv'
        fullpath = dir_destino + nome_arquivo
        fullpath_csv = dir_destino + nome_csv

        # Criando o diretorio de destino dos arquivos baixados
        try:
            os.makedirs(dir_destino)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        print ano
        ftp.cwd(ano)
        file_list = ftp.nlst()

        for f in file_list:
            # aplicando os filtros
            if "dados" in f.lower() and any(f.endswith(ext) for ext in '.zip'):
                # download file sending "RETR <name of file>" command
                # open(f, "w").write is executed after RETR suceeds and returns file binary data
                with open(fullpath, 'wb') as arq:
                    print ftp.retrbinary('RETR ' + f, arq.write, 8192 * 100)
        ftp.cwd('../')

        archive = zipfile.ZipFile(fullpath, 'r')
        archive.extractall(dir_destino)
        archive.close()
        os.remove(fullpath)

        for root, dirs, files in os.walk(dir_destino):
            for file in files:
                if file.endswith(".txt") and 'PES' in file:
                    main('input.txt', os.path.join(root, file), fullpath_csv)
    ftp.quit()
    print '\nFIM!!'


def get_var(line):
    try:
        # Read
        position, rest = line.split(' ', 1)
        variable, rest = rest.strip().split(' ', 1)
        size, rest = rest.strip().split(' ', 1)
        comment = rest.replace('/*', '').replace('*/', '').strip()

        # Convert
        position = int(position.replace('@', ''))
        variable = variable.strip()
        size = int(float(size.replace('$', '')))

        return {
            'name': variable,
            'position': position,
            'size': size,
            'comment': comment, }
    except:
        print 'erro'


def get_vars(varsfile):
    variables = []
    for line in varsfile:
        if line == '\n':
            pass
        else:
            variable = get_var(line)
            variables.append(variable)
    return variables


def read_var(line, var):
    pos = var['position'] - 1  # 1 index based
    return line[pos: pos + var['size']]


def read_row(line, variables):
    columns = []
    for var in variables:
        value = read_var(line, var)
        columns.append(value.strip())
    return columns


def print_header(variables, separator, output):
    with open(output, 'w+') as fl:
        fl.write(separator.join(x['name'].encode('utf-8') for x in variables))
        # print(separator.join(x['name'].encode('utf-8') for x in variables))


def main(vars_file, data_file, output):
    vars_fp = io.open(vars_file)
    data_fp = io.open(data_file)
    variables = get_vars(vars_fp)
    separator = ';'

    print_header(variables, separator, output)
    for line in data_fp:
        line = read_row(line, variables)
        with open(output, 'a') as fl:
            fl.write('\n' + separator.join(line))
            # print(separator.join(line))

    data_fp.close()
    vars_fp.close()


def executa_pnad():
    find_zips_pnad()
