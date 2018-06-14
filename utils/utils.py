# coding=utf-8

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

    url = 'http://inep.gov.br/microdados'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    all_hrefs = soup.find_all('a')
    all_links = [link.get('href') for link in all_hrefs]
    zip_files = [dl for dl in all_links if dl and '.zip' in dl]
    for l in zip_files:
        print(l)

