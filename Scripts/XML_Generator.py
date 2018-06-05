# -*- coding: utf-8 -*-
import os
from lxml import etree


class GeneratorSolrXML(object):

    """ classe gera arquivo xml no formato aceito pelo Solr
        Exemplo:
        gerador =  GeneratorSolrXML(
                            limit_docs_in_file = 40,
                            path_save_xml= 'absolute/path/savefile/',
                            xml_filename= 'nome_arquivo_de_saida')

        #lista dados é a forma correta para ('lista_dados', [1,2,3])
        doc1 = [ ('nome', 'José'),  ('idade', 34),
                ('cidade', 'São Paulo'), ('lista_de_dados', '1'),
                ('lista_de_dados', '2'), ('lista_de_dados', '3') ]

        #hierarquia_campo contem valor necessario para constuir filtro de multiplos niveis
        doc2 = [ ('nome', 'Paulo'), ('idade', 55), ('cidade', 'São Paulo'), ('hierarquia_campo', 'ANO|MES|DIA') ]

        docs = [doc1, doc2 ...]

        for doc in docs:
            gerador.generateDoc(doc)

        #deve salvar depois do loop
        gerador.save_xml()

    """

    limit_docs_in_file = 5000
    file_finish = 0
    path_save_xml = ''
    tree = []
    xml_filename = 'output'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # cria variveis de todos os atributos passados com chave valor
            setattr(self, key, value)

    def generateDoc(self, listTuple):
        doc = etree.Element('doc')
        for item in listTuple:
            registro = self.generateFieldElement(item)
            if not registro is None:
                doc.append(registro)

        self.tree.append(doc)

        if len(self.tree) >= self.limit_docs_in_file:
            self.save_xml()
            self.file_finish += 1
            self.tree = []

    def generateFieldElement(self, tuple_field):
        if not tuple_field[1] is None:
            element = etree.Element('field')
            element.attrib['name'], element.text = tuple_field
            return element
        else:
            return None

    def save_xml(self):
        if len(self.tree):
            root = etree.Element('add')
            for element in self.tree:
                root.append(element)
            xml_filename = self.xml_filename + '_part_' + str((self.file_finish + 1)) + '.xml'

            xml = etree.ElementTree(root)
            print('Save one more file')
            xml.write(self.path_save_xml + xml_filename, xml_declaration=True, encoding='utf-8')
        else:
            raise ValueError("self.tree is Empty")
