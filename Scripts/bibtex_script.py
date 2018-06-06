# -*- coding: utf-8 -*-

# !/usr/bin/python
import sys
import re
import bibtexparser as bp
from lxml import etree


def bibTOxml(bibfile, outfile):
    with open(bibfile) as bibtex_file:
        bd = bp.load(bibtex_file)
        bd = bd.entries_dict.items()
    docs = []
    for key, item in bd:
        doc = []
        article = key

        try:
            unique_id = ('id', item['unique-id'][6:-1])
            doc.append(unique_id)

            # print(unique_id)
        except KeyError:
            pass

        try:
            unique_id = ('unique-id', item['unique-id'][1:-1])
            doc.append(unique_id)

            # print(unique_id)
        except KeyError:
            pass

        title = ('title', item['title'][1:-1])
        doc.append(title)
        # print(title)

        padrao = ',|\n|\*|;'
        authors = item['author']
        for author in re.split('\sand\s', authors):
            name_list = re.split(padrao, author)
            name_list.reverse()
            name = ('Author', (' '.join(name_list)).strip())
            doc.append(name)

        docs.append(doc)

        publisher = item['publisher'][1:-1]
        journal = item['journal'][1:-1]
        volume = item['volume'][1:-1]
        pub_journal = ('publisher_journal_volume', "{}|{}|{}".format(publisher, journal, volume))
        doc.append(pub_journal)

        # print(pub_journal)

        year = item['year'][1:-1]
        if 1990 <= int(year) <= 1999:
            group = '1990-1999'
        elif 2000 <= int(year) <= 2009:
            group = '2000-2009'
        elif 2010 <= int(year) <= 2019:
            group = '2010-2019'
        month = item['month'][1:5]
        year_month = ('Year-Month', '{}|{}|{}'.format(group.strip(), year.strip(), month.strip()))
        doc.append(year_month)
        # print(year_month)

        abstract = ('abstract', item['abstract'][1:-1])
        doc.append(abstract)
        # print(abstract)

        address = ('address', item['address'].split()[-2])
        doc.append(address)
        # print(address)

        type = ('type', item['type'][1:-1])
        doc.append(type)
        # print(type)

        language = ('language', item['language'][1:-1])
        doc.append(language)
        # print(language)

        DOI = ('DOI', item['doi'][1:-1])
        doc.append(DOI)

        # print(DOI)

        ISSN = ('ISSN', item['issn'][1:-1])
        doc.append(ISSN)

        # print(ISSN)

        try:
            EISSN = ('EISSN', item['eissn'][1:-1])
            doc.append(EISSN)

            # print(EISSN)
        except KeyError:
            pass

        try:
            keywords = re.split(padrao, item['keywords'][1:-1])
            for k in keywords:
                if k:
                    doc.append(('keyword', k))

        except KeyError:
            pass

        try:
            keywords_plus = re.split(padrao, (item['keywords-plus'][1:-1]).strip())
            for k in keywords_plus:
                if k:
                    doc.append(('keyword-plus', k))
        except KeyError:
            pass

        try:
            research_area = ('research-areas', item['research-areas'][1:-1])
            doc.append(research_area)

            # print(research_area)
        except KeyError:
            pass

        try:
            web_of_science_categories = ('web-of-science-categories', item['web-of-science-categories'][1:-1])
            doc.append(web_of_science_categories)

            # print(web_of_science_categories)
        except KeyError:
            pass

        try:
            funding_acknowledgement = ('funding-acknowledgement', item['funding-acknowledgement'][1:-1])
            # print(funding_acknowledgement)
        except KeyError:
            pass

        try:
            nro_cited_ref = ('number-of-cited-references', item['number-of-cited-references'][1:-1])
            doc.append(nro_cited_ref)

            # print(nro_cited_ref)
        except KeyError:
            pass

        try:
            times_cited = ('times-cited', item['times-cited'][1:-1])
            doc.append(times_cited)

            # print(times_cited)
        except KeyError:
            pass

        try:
            journal_iso = ('journal-iso', item['journal-iso'][1:-1])
            doc.append(journal_iso)

            # print(journal_iso)
        except KeyError:
            pass

        print("#######################")

    # print(len(docs))

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
            for key, value in kwargs.iteritems():
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

    gerador = GeneratorSolrXML(limit_docs_in_file=40,
                               path_save_xml='',
                               xml_filename=outfile)

    for doc in docs:
        gerador.generateDoc(doc)
    gerador.save_xml()


bibTOxml('../data/sample.bib', 'outputz')
