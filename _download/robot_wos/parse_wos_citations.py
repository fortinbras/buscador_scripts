# -*- coding: utf-8 -*-

import os, sys, re, cPickle



"""
Para ver o citacoes_por_ano de um Documento especifico

documento = Documento.objects.get(id='107405')
print cPickle.loads(str(documento.citacoes_por_ano))
exit(0)
"""


path_dl = '/Users/giusepperosa/PycharmProjects/buscador_scripts/robot_wos/' #PROJECT_PATH + '/tasks/wos/importa_citacoes/downloads/'
nao_pegou = ''

files = []
for root, dirs, files in os.walk(path_dl):
    files = [f for f in files if f.endswith('.txt')]
    break

i = 0
for file in files:
    if file.endswith('.txt'):
        f = open(path_dl + file, 'r')
        citations_content = f.read()
        f.close()
    
    citations_header = []
    achou_title = False
    for line in citations_content.split('\n'):
        if citations_header and line:
            cols = line.split('","')
            cols[0] = cols[0].replace('"', '').strip()
            cols[-1] = cols[-1].replace('"', '').strip()
            
            index_col = citations_header.index(cols[7])
            
            doi = cols[16].strip()
            citations_list = zip( citations_header[index_col:], [int(c) for c in cols[index_col:]] )
            
            #print doi, citations_list
            
#             if doi:
#                 documento = Documento.objects.filter(doi=doi).first()
#             else:
#                 titulo = cols[0].strip()
#                 volume = cols[8].strip()
#                 issue = cols[9].strip()
#                 pagina_inicial = cols[13].strip()
#                 pagina_final = cols[14].strip()
#                 if pagina_final:
#                     paginas = [pagina_inicial + '-' + pagina_final, pagina_inicial + ' - ' + pagina_final]
#                 elif pagina_inicial:
#                     paginas = [pagina_inicial,]
#                 else:
#                     paginas = ['',]
#
#                 # Acrescentando procedencia para pegar somente o que eh da WoS. Senao dah colisao com a Scielo.
#                 documento = Serie_Periodica.objects.filter(titulo__titulo=titulo, volume=volume, numero=issue, paginas__in=paginas,procedencia_id=1)
#                 if len(documento) == 1:
#                     documento = documento[0]
#                 elif len(documento) > 1:
#                     print 'duplicado', ';'.join([str(d.id) for d in documento])
#                     documento = None
#                 else:
#                     documento = None
#
#             if documento:
#                 documento.citacoes_por_ano = cPickle.dumps(citations_list)
#                 documento.save()
#                 i += 1
#             else:
#                 print 'nao pegou:', cols
#                 nao_pegou += str(cols[0]) + "\n"
#
        if line.startswith('"Title"'):
            citations_header = line.split('","')
            citations_header[0] = citations_header[0].replace('"', '').strip()
            citations_header[-1] = citations_header[-1].replace('"', '').strip()
#
#     print "Fim arquivo: %s" % (file)
#
# # os.system('rm %s*.txt' % path_dl)
#
# print 'importados', i
#
# if nao_pegou:
    print nao_pegou
    # send_mail(u'Importação Citações do Web of Science - Não Encontrados', '\n' + nao_pegou, 'cdi2@fapesp.br', ["rmoriya@fapesp.br","lvido@fapesp.br"])
    #send_mail(u'Importação Citações do Web of Science - Não Encontrados', '\n' + nao_pegou, 'cdi2@fapesp.br', ["rmoriya@fapesp.br"])
