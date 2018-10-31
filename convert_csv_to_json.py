# -*- coding: utf8 -*-
import errno
import os
import sys
import commands
import pandas as pd
import json


def convert_to_json():
    linhas = 0
    path = '/var/tmp/solr_front/collections/rais_estabelecimento/planilha'

    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(".csv"):
                print(f)
                arquivo = open(os.path.join(root, f), 'r')
                linhas = commands.getstatusoutput('cat ' + os.path.join(root, f) + ' |wc -l')[1]
                print 'Arquivo de entrada possui {} linhas de informacao'.format(int(linhas)-2)
                df = pd.read_csv(arquivo, sep=';', encoding='latin-1', low_memory=False )
                print(df)
                print
                #df2 = pd.DataFrame([df], index=['Valor na Fonte'], columns=['Descricao'])
                df2 = pd.DataFrame(df)

                df_json  = df2.to_json()
                print(df_json)


                exit()
                #df_json  = df.to_json('_transform/rais_estabelecimento',)


convert_to_json()
