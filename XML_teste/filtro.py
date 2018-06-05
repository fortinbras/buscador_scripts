import xml.etree.ElementTree as xee


def filtro(input_file, output_file):
    input_tree = xee.parse(input_file)  # inicializando a arvore do xml de entrada
    input_root = input_tree.getroot()  # obtendendo o elemento raiz do xml de entrada

    output_root = xee.Element('add')  # definindo 'add' para a raiz do arquivo de saida
    output_doc = xee.SubElement(output_root, 'doc')  # definindo 'doc' como sub elemento de 'add' para o arquido saida

    for child in input_root.iter():  # iterando sob os sub elementos do xml de entrada

        # Adiconando atributo (child.attrib) em um sub elemento 'field' se IF for True
        if child.tag == 'DADOS-GERAIS':
            xee.SubElement(output_doc, 'field', name='NOME-COMPLETO').text = child.attrib['NOME-COMPLETO']

        if child.tag == 'RESUMO-CV':
            xee.SubElement(output_doc, 'field', name='TEXTO-RESUMO-CV-RH').text = str(
                child.attrib['TEXTO-RESUMO-CV-RH'])

        if child.tag == 'IDIOMAS':
            xee.SubElement(output_doc, 'field', name='numero_idiomas').text = str(
                len([idioma.attrib for idioma in child.iter('IDIOMA')]))

        if child.tag == 'ARTIGOS-PUBLICADOS':
            xee.SubElement(output_doc, 'field', name='numero_artigos').text = str(
                len([artigo.attrib for artigo in child.iter('ARTIGO-PUBLICADO')]))

    output_tree = xee.ElementTree(output_root)  # definindo arvore para arquivo de saida
    return output_tree.write(output_file, encoding='utf-8') #criando arquivo de saida


input_file = 'cnpq.xml'
output_file = 'output.xml'


filtro(input_file, output_file)
