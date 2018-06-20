# -*- coding: utf-8 -*-

# !/usr/bin/python
import sys

sys.path.insert(0, '../../../buscador_scripts/')

import os
import re
from lxml import etree
from bibtexparser.bparser import BibTexParser
from utils import gYear


class BibtoXML(object):
    """ classe gera arquivo xml no formato aceito pelo Solr a partir de um arquivo .bib

gerador = BibGeneratorSolrXML(diretorio)
diretorio = parametro onde os arquivos bib estão localizados

gerador.parse_bib()
    os arquivos bib serão compilados para xml e salvos na pasta xml_out

    """

    limit_docs_in_file = 5000
    file_finish = 0
    path_save_xml = '/var/tmp/wos/transform/'
    tree = []
    xml_filename = 'output'

    def __init__(self, directory, **kwargs):
        self.directory = directory
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
            directory = os.path.dirname(self.path_save_xml)
            if not os.path.exists(directory):
                os.makedirs(directory)
            xml.write(self.path_save_xml + xml_filename, xml_declaration=True, encoding='utf-8')
        else:
            raise ValueError("self.tree is Empty")

    def parse_bib(self):
        docs = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.bib'):
                    with open(self.directory + file) as bibtex_file:
                        bp = BibTexParser()
                        bd = bp.parse_file(bibtex_file, partial=True)
                        bd = bd.entries_dict.items()
                    content = 0
                    for key, item in bd:
                        doc = []
                        article = key

                        try:
                            unique_id = ('id', (item['unique-id'][6:-1]).strip())
                            doc.append(unique_id)

                            # print(unique_id)
                        except KeyError:
                            pass

                        try:
                            unique_id = ('unique-id', (item['unique-id'][1:-1]).strip())
                            doc.append(unique_id)

                            # print(unique_id)
                        except KeyError:
                            pass

                        try:
                            title = ('title', (item['title'][1:-1]).strip())
                            doc.append(title)
                            # print(title)
                        except:
                            pass

                        padrao = ',|\n|\*|;'
                        try:
                            authors = item['author']
                            for author in re.split('\sand\s', authors):
                                name_list = re.split(padrao, author)
                                name_list.reverse()
                                name = ('Author', (' '.join(name_list)).strip())
                                doc.append(name)

                            # docs.append(doc)
                        except KeyError:
                            pass

                        try:
                            publisher = (item['publisher'][1:-1]).strip()
                            journal = (item['journal'][1:-1]).strip()

                            try:
                                volume = item['volume'][1:-1]
                                pub_journal = ('publisher_journal_volume_facet',
                                               "{}|{}|{}".format(publisher.strip(), journal.strip(), volume.strip()))
                                doc.append(pub_journal)
                            except:
                                pub_journal = (
                                    'publisher_journal_volume_facet',
                                    "{}|{}| ".format(publisher.strip(), journal.strip()))
                                doc.append(pub_journal)
                        except KeyError:
                            pass

                        # print(pub_journal)
                        try:

                            year = item['year'][1:-1]
                            group = gYear(int(year))

                        except:
                            continue

                        try:

                            month = item['month'][1:4]
                            year_month = (
                            'Year-Month_facet', '{}|{}|{}'.format(group.strip(), year.strip(), month.strip()))
                            doc.append(year_month)
                        except KeyError:
                            year_month = ('Year-Month_facet', '{}|{}|'.format(group.strip(), year.strip()))
                            doc.append(year_month)
                        # print(year_month)

                        try:
                            abstract = ('abstract', (item['abstract'][1:-1]).strip())
                            doc.append(abstract)
                            # print(abstract)
                        except KeyError:
                            pass

                        try:

                            address = ('address', ((item['address'].split())[-2]).strip())
                            doc.append(address)
                            # print((item['address'].split())[-1][0:-1])
                        except:
                            pass

                        try:

                            tipe = ('type', (item['type'][1:-1]).strip())
                            doc.append(tipe)
                            # print(type)
                        except KeyError:
                            pass

                        try:

                            affiliations = (item['affiliation']).split('\n')
                            for aff in affiliations:
                                affiliation = ('affiliation', aff)
                                doc.append(affiliation)
                                # print(type)
                        except KeyError:
                            pass

                        try:
                            language = ('language', (item['language'][1:-1]).strip())
                            doc.append(language)
                            # print(language)
                        except KeyError:
                            pass

                        try:

                            DOI = ('DOI', (item['doi'][1:-1]).strip())
                            doc.append(DOI)
                        except KeyError:
                            pass

                        # print(DOI)
                        try:
                            ISSN = ('ISSN', (item['issn'][1:-1]).strip())
                            doc.append(ISSN)
                        except KeyError:
                            pass

                        # print(ISSN)

                        try:
                            EISSN = ('EISSN', (item['eissn'][1:-1]).strip())
                            doc.append(EISSN)

                            # print(EISSN)
                        except KeyError:
                            pass

                        try:
                            keywords = re.split(padrao, item['keywords'][1:-1])
                            for k in keywords:
                                if k:
                                    doc.append(('keyword', k.strip()))

                        except KeyError:
                            pass

                        try:
                            keywords_plus = re.split(padrao, (item['keywords-plus'][1:-1]).strip())
                            for k in keywords_plus:
                                if k:
                                    doc.append(('keyword-plus', k.strip()))
                        except KeyError:
                            pass

                        try:

                            research_area = (
                                'research-areas', ((item['research-areas'][1:-1]).replace('; ', '|')).strip())
                            doc.append(research_area)
                            # print(research_area)
                        except KeyError:
                            pass

                        try:
                            web_of_science_categories = (
                                'web-of-science-categories',
                                ((item['web-of-science-categories'][1:-1]).replace('; ', '|')).strip())
                            doc.append(web_of_science_categories)

                            # print(web_of_science_categories)
                        except KeyError:
                            pass

                        try:
                            funding_acknowledgement = (
                                'funding-acknowledgement', (item['funding-acknowledgement'][1:-1]).strip())
                            # print(funding_acknowledgement)
                            doc.append(funding_acknowledgement)
                        except KeyError:
                            pass

                        try:
                            nro_cited_ref = (
                                'number-of-cited-references', (item['number-of-cited-references'][1:-1]).strip())
                            doc.append(nro_cited_ref)

                            # print(nro_cited_ref)
                        except KeyError:
                            pass

                        try:
                            times_cited = ('times-cited', (item['times-cited'][1:-1]).strip())
                            doc.append(times_cited)

                            # print(times_cited)
                        except KeyError:
                            pass

                        try:
                            journal_iso = ('journal-iso', (item['journal-iso'][1:-1]).strip())
                            doc.append(journal_iso)

                            # print(journal_iso)
                        except KeyError:
                            pass

                        docs.append(doc)
                        # content += 1
                        # print(content)
                    print(file)
        for doc in docs:
            self.generateDoc(doc)

        self.save_xml()


if __name__ == '__main__':
    diretorio = '/var/tmp/bibtex/'
    bib_xml = BibtoXML('/var/tmp/bibtex/')
    bib_xml.parse_bib()
