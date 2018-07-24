# -*- coding: utf-8 -*-

# !/usr/bin/python
import sys
import os

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, '../../../buscador_scripts/')

import re
from lxml import etree
from utils import gYear
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import datetime
import time

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
        self.date = datetime.datetime.now()
        self.log_file = 'wos_transform.log'
        self.total_entries = 0
        self.total_saved = 0
        self.directory = directory
        self.error = []
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
            print('Salvando XML {}'.format(xml_filename))
            directory = os.path.dirname(self.path_save_xml)
            if not os.path.exists(directory):
                os.makedirs(directory)
            xml.write(self.path_save_xml + xml_filename, xml_declaration=True, encoding='utf-8')
        else:
            raise ValueError("self.tree is Empty")

    @staticmethod
    def remove_chaves(texto):
        """
        :type texto: str

        """
        if texto == '':
            return ''
        str = texto.replace('{', '').replace('}', '')
        return str

    def parse_bib(self):
        # docs = []
        content_saved = 0
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.bib'):
                    with open(self.directory + file) as bibtex_file:
                        try:
                            parser = BibTexParser()
                            bibtex_str = bibtex_file.read()
                            st = bibtex_str.replace("Web of Science-Category", "Web-of-Science-Category").replace("\{",
                                                                                                                  "[").replace(
                                "\}", "]").replace("\{", "[").replace("\%", "%").replace("\\", '')
                            st = st.replace('Early Access Date', 'month').replace('Early Access Year',
                                                                                  'year')#.replace('\n', ' ')
                            # parser.ignore_nonstandard_types = False
                            # parser.customization = convert_to_unicode
                            # parser.homogenize_fields = True
                            bib_database = bibtexparser.loads(st,parser=parser)
                        except:
                            self.error.append(file)
                            continue

                    content_entries = len(bib_database.entries)
                    self.total_entries += content_entries
                    print 'O arquivo ' + file + ' tem: ' + str(content_entries) + ' registros'
                    for key, item in bib_database.entries_dict.items():
                        doc = []
                        # article = key


                        id = ('id', str(content_saved+1))
                        doc.append(id)

                        try:
                            unique_id = ('unique-id', (self.remove_chaves(item['unique-id'])).strip())
                            doc.append(unique_id)

                            # print(unique_id)
                        except KeyError:
                            pass

                        try:
                            title = ('title', (self.remove_chaves(item['title'])).strip())
                            doc.append(title)
                            # print(title)
                        except KeyError:
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
                            publisher = (item['publisher']).strip()
                            publisher_add = ('publisher',publisher)
                            doc.append(publisher_add)
                            journal = (item['journal']).strip()

                            try:
                                volume = item['volume']
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

                            year = item['year']
                            group = gYear(int(year))

                        except:
                            year = ''
                            group = ''

                        try:

                            month = item['month'][0:4]
                            year_month = (
                                'Year-Month_facet', '{}|{}|{}'.format(group.strip(), year.strip(), month.strip()))
                            doc.append(year_month)
                        except KeyError:
                            year_month = ('Year-Month_facet', '{}|{}|'.format(group.strip(), year.strip()))
                            doc.append(year_month)
                        # print(year_month)

                        try:
                            abstract = ('abstract', self.remove_chaves(item['abstract']))
                            doc.append(abstract)
                            # print(abstract)
                        except KeyError:
                            pass

                        try:
                            if (item['address'].split(',')[-1]).split(' ') < 2:
                                address = ('address', (item['address'].split(',')[-1]).strip())
                            else:
                                address = (
                                    'address', (item['address'].split(',')[-1].split(' ')[-1]).strip())
                            doc.append(address)
                            # print((item['address'].split())[-1][0:-1])
                        except:
                            pass

                        try:

                            tipe = ('type', (item['type']).strip())
                            doc.append(tipe)
                            # print(type)
                        except KeyError:
                            pass

                        try:

                            affiliations = (self.remove_chaves(item['affiliation'])).split('\n')
                            for aff in affiliations:
                                affiliation = ('affiliation', aff)
                                # c = aff.split(',')[-1].replace('.','')
                                country_aff = ('affiliation_country',aff.split(',')[-1].split(' ')[-1].replace('.',''))
                                print country_aff
                                doc.append(affiliation)
                                doc.append(country_aff)

                                # print(type)
                        except KeyError:
                            pass

                        try:
                            language = ('language', (self.remove_chaves(item['language'])).strip())
                            doc.append(language)
                            # print(language)
                        except KeyError:
                            pass

                        try:

                            DOI = ('DOI', (self.remove_chaves(item['doi'])).strip())
                            doc.append(DOI)
                        except KeyError:
                            pass

                        # print(DOI)
                        try:
                            ISSN = ('ISSN', (item['issn']).strip())
                            doc.append(ISSN)
                        except KeyError:
                            pass

                        # print(ISSN)

                        try:
                            EISSN = ('EISSN', (item['eissn']).strip())
                            doc.append(EISSN)

                            # print(EISSN)
                        except KeyError:
                            pass

                        try:
                            keywords = re.split(padrao, self.remove_chaves(item['keywords']))
                            for k in keywords:
                                if k:
                                    doc.append(('keyword', k.strip()))

                        except KeyError:
                            pass

                        try:
                            keywords_plus = re.split(padrao, (item['keywords-plus']).strip())
                            for k in keywords_plus:
                                if k:
                                    doc.append(('keyword-plus', k.strip()))
                        except KeyError:
                            pass

                        try:

                            research_area = (
                                'research-areas', ((item['research-areas']).replace('; ', '|')).strip())
                            doc.append(research_area)
                            # print(research_area)
                        except KeyError:
                            pass

                        try:
                            web_of_science_categories = (
                                'web-of-science-categories',
                                ((item['web-of-science-categories']).replace('; ', '|')).strip())
                            doc.append(web_of_science_categories)

                            # print(web_of_science_categories)
                        except KeyError:
                            pass

                        try:
                            funding_acknowledgement = (
                                'funding-acknowledgement', (item['funding-acknowledgement']).strip())
                            # print(funding_acknowledgement)
                            doc.append(funding_acknowledgement)
                        except KeyError:
                            pass

                        try:
                            nro_cited_ref = (
                                'number-of-cited-references', (item['number-of-cited-references']).strip())
                            doc.append(nro_cited_ref)

                            # print(nro_cited_ref)
                        except KeyError:
                            pass

                        try:
                            times_cited = ('times-cited', (item['times-cited']).strip())
                            doc.append(times_cited)

                            # print(times_cited)
                        except KeyError:
                            pass

                        try:
                            journal_iso = ('journal-iso', (item['journal-iso']).strip())
                            doc.append(journal_iso)

                            # print(journal_iso)
                        except KeyError:
                            pass

                        # docs.append(doc)
                        self.generateDoc(doc)
                        content_saved += 1
                    # print("{} arquivos salvos".format(content))
                    #print(file)
        # for doc in docs:
        #     self.generateDoc(doc)

        self.save_xml()
        self.total_saved = content_saved
        self.logger()

    def logger(self):
        directory = '/var/tmp/wos/transform/'
        log_file = self.log_file
        logging = directory+log_file
        with open(logging, 'a') as log:
            log.write("\n")
            log.write('############ TASK WOS ###############')
            log.write("\n")
            log.write('Log gerado em {}'.format(self.date.strftime("%Y-%m-%d %H:%M")))
            log.write("\n")
            log.write('Arquivo de entrada possui {} registros'.format(self.total_entries))
            print('Arquivo de entrada possui {} registros'.format(self.total_entries))
            log.write("\n")
            log.write('Foram salvos {} registros'.format(self.total_saved))
            print('Foram salvos {} registros'.format(self.total_saved))
            if len(self.error) > 0:
                log.write("\n")
                log.write('Os arquivos {} estao com erro'.format(self.error))
                print('Os arquivos {} estao com erro'.format(self.error))
            log.write("\n")
            log.write('############ END TASK WOS ###############')


def wos_tranform():
    wos_xml = BibtoXML('/var/tmp/bibtex/')
    wos_xml.parse_bib()


if __name__ == '__main__':
    diretorio = '/var/tmp/bibtex/'
    bib_xml = BibtoXML('/var/tmp/bibtex/')
    bib_xml.parse_bib()
