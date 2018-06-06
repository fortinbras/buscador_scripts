from bib_to_xml import BibtoXML
from slor_load_xml import Solr_load_xml

bib = {
    'bib_folder': '/var/tmp/bibtex/',
    'output': '.xml',
    'xml_folder': 'xml_out/',
    'server_folder': 'wos',
    'localhost': '192.168.0.212:8983',
    'content-type': 'text/xml'}

bibxml = BibtoXML('/var/tmp/bibtex/')
bibxml.parse_bib()  # gera XML
print('ok')
#######################################

slorload = Solr_load_xml(bib['xml_folder'], bib['output'], bib['localhost'], bib['server_folder'],
                         bib['content-type'])

slorload.files_load()  # carrega no server
