# -*- coding: utf-8 -*-


def tamanho_estab_dic():
    tamanho = {
       -1: "IGNORADO",
        1: "ZERO funcionários",
        2: "até 4 funcionários",
        3: "de 5 a 9 funcionários",
        4: "de 10 a 19 funcionários",
        5: "de 20 a 49 funcionários",
        6: "de 50 a 99 funcionários",
        7: "de 100 a 249 funcionários",
        8: "de 250 a 499 funcionários",
        9: "de 500 a 999 funcionários",
        10: "1000 ou mais funcionários"

    }
    d = {int(k): unicode(v, "utf8") for k, v in tamanho.items()}
    return d
