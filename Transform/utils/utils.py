# coding=utf-8
# funçoes utilitarias

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
        if year in range(a,(b+1),1):
             return i


