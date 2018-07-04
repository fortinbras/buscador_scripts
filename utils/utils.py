# coding=utf-8


import os


def gYear(year):
    ini = 1940
    end = 2050
    lista = []
    for a in range(ini, end, 10):
        group = '{}-{}'.format((a - 10), (a - 1))
        lista.append(group)

    for i in lista:
        a = int(i[0:4])
        b = int(i[5:])
        try:
            if int(year) in range(a, (b + 1), 1):
                return i
        except:
            if year in range(a, (b + 1), 1):
                return i


def find_regiao(cod):
    regioes = {'Regiao Norte': [11, 12, 13, 14, 15, 16, 17],
               'Regiao Nordeste': [21, 22, 23, 24, 25, 26, 27, 28, 29],
               'Regiao Sudeste': [31, 32, 33, 35],
               'Regiao Sul': [41, 42, 43],
               'Regiao Centro-Oeste': [50, 51, 52, 53]}
    v = str(cod)[0:2]
    for reg, cod in regioes.iteritems():
        if v in str(cod):
            return reg


def find_zip():
    import requests
    from bs4 import BeautifulSoup

    url = 'http://web.fflch.usp.br/centrodametropole/1148'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    all_hrefs = soup.find_all('a')
    all_links = [link.get('href') for link in all_hrefs]
    zip_files = [dl for dl in all_links if dl and '.7z' in dl]
    for l in zip_files:
        print(l)


def list_output_files(collectiondir, transform):
    PATH_ORIGEM = '/var/tmp/inep'
    try:
        anos = os.listdir(collectiondir)
        anos.sort()
    except OSError:
        print('Nenhuma pasta encontrada')
        raise
    for ano in anos:
        # print(ano)
        var = collectiondir + '/' + ano + '/' + transform
        for root, dirs, files in os.walk(var):
            for file in files:
                if file.endswith(".csv"):
                    print os.path.join(root, file)


def find_zips_pnad():

    from ftplib import FTP

    anos = ['2011','2012','2013','2014','2015']
    ftp = FTP("ftp.ibge.gov.br")
    ftp.login()
    ftp.cwd('Trabalho_e_Rendimento')
    ftp.cwd('Pesquisa_Nacional_por_Amostra_de_Domicilios_anual')
    ftp.cwd('microdados')
    for ano in anos:
        filename = "pnad_"+ano+".zip"
        print ano
        ftp.cwd(ano)
        file_list = ftp.nlst()

        for f in file_list:
            # apply your filters
            if "dados" in f.lower() and any(f.endswith(ext) for ext in '.zip'):
                # download file sending "RETR <name of file>" command
                # open(f, "w").write is executed after RETR suceeds and returns file binary data
                with open(filename, 'wb') as zipfile:
                    print ftp.retrbinary('RETR ' + f, zipfile.write)
        ftp.cwd('../')
    ftp.quit()


