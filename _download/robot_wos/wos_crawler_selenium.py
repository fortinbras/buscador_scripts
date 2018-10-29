from seleniumrequests import Chrome
from seleniumrequests import PhantomJS
from selenium import webdriver
import urllib
import os
base_url = 'https://apps.webofknowledge.com/'
options = webdriver.ChromeOptions()
driver = Chrome(chrome_options=options)#, service_log_path='teste.log')

driver.implicitly_wait(30)
# sess = requests.Session()

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-US;q=0.5,en;q=0.3',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Connection': 'keep-alive'
           }
# sess.headers.update(headers)
FAPESP_ALTERNATIVES = [
    '"fundacao de amparo a pesquisa do estado de sao paulo"',
    'fapesp',
    'FAPESP',
    '"fundacao de amparo a pesquisa do estado de s paulo"',
    '"FUNDACAO DE AMPARO PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE APOIO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DE SAO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA NO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTADO SAO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTADO DE SO PAULO"',
    '"FUNDA AO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AMPAROA PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTADO DE SAO PAOLO"',
    '"FUNDACAO AMPARO A PEQUISA ESTADO SAO PAULO"',
    '"FUNDACAO AMPARO A PESQUISA ESTADO DE SAO PAULO"',
    '"FUNDACAO APOIO A PESQUISA ESTADO SAO PAULO"',
    '"FUNDACAO DE AMPARO E PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUND ACAO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDA AO DE AMPARO A PESQUISA DO ESTADO SAO PAULO"',
    '"FUNDA AO DE AMPARO D PESQUISA DO ESTADO DE SIO PAULO"',
    '"FUNDA DO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDA DO DE APOIO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDA GO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDAAAO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACA O DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACACO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AMPARA A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AMPARO 5 PESQUISA DO ESTADA DE SAO PAULO"',
    '"FUNDACAO DE AMPARO 6 PESQUISA DO ESTADO DE SAO"',
    '"FUNDACAO DE AMPARO A PESQUISA AO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTACLO DE SAO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTADO CLE SAO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTADO CLE SJO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTADO DA SAO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTADO DE SDO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTADO DE SILO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTADO DE SO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA DO ESTRADO DE SAO PAULO"',
    '"FUNDACAO DE AMPARO A PESQUISA ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AMPARO AA PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AMPARO PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AMPAROA A PESQUISA DO ESTADO DAE SO PAULO"',
    '"FUNDACAO DE APARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE ARNPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACAO DE AUXILIO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDACXAO DE AMPARO A PESQUISA NO ESTADO DE SAO PAULO"',
    '"FUNDAEAO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDAGAO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FUNDAGDO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO"',
    '"FOUNDATION FOR THE SUPPORT OF RESEARCH IN THE STATE OF SAO PAULO"',
    '"FOUNDATION FOR RESEARCH SUPPORT OF THE STATE OF SAO PAULO"',
    '"FOUNDATION FOR THE SUPPORT OF RESEARCH OF THE STATE OF SAO PAULO"',
    '"FOUNDATION FOR RESEARCH ASSISTANCE SAO PAULO STATE"',
    '"FOUNDATION FOR RESEARCH SUPPORT OF THE STATE OF SAO PAULO"',
    '"FOUNDATION FOR RESEARCH OF THE STATE OF SAO PAULO"',
    '"FOUNDATION FOR RESEARCH SUPPORT OF SAO PAULO STATE"',
    '"FOUNDATION FOR RESEARCH SUPPORT OF THE SAO PAULO STATE"',
    '"FOUNDATION FOR RESEARCH SUPPORT SAO PAULO"',
    '"FOUNDATION FOR SCIENTIFIC RESEARCH OF SAO PAULO STATE"',
    '"FOUNDATION FOR SUPPORT OF RESEARCH IN THE STATE OF SAO PAULO"',
    '"FOUNDATION OF SUPPORT TO RESEARCH FROM STATE OF SAO PAULO"',
    '"FOUNDATION TO SUPPORT RESEARCH OF THE STATE OF SAO PAULO"',
    '"FOUNDATIONS THAT SUPPORT RESEARCH IN THE STATE OF SAO PAULO"',
    '"Sao Paulo State Research Foundation"',
    '"Sao Paulo State Science Council"',
    '"Sao Paulo Research Foundation"',
    '"Sao Paulo Research Foundation (FAPESP)"',
    '"Fundacao de Pesquisa do Estado de Sao Paulo"',
    '"FAPESP (Fundacao de Amparo a Pesquisa do Estado de Sao Paulo)"'
]
QUERY = 'FO=(%s)' % ' OR '.join(FAPESP_ALTERNATIVES)


def ua_advanced_search_input():
    """
    Requests try to get this page and wos redirects to the right search page.
    """
    # https://apps.webofknowledge.com/WOS_AdvancedSearch_input.do?product=WOS&search_mode=AdvancedSearch
    driver.get(base_url + 'UA_AdvancedSearch_input.do?product=UA&search_mode=AdvancedSearch')


def ua_advanced_search():
    """
    This page contains the main advanced search form.
    """
    url = base_url + 'UA_AdvancedSearch.do'
    sid = driver.get_cookie('SID')

    payload = {
        'product': 'UA',
        'search_mode': 'AdvancedSearch',
        'SID': sid['value'][1:-1],
        'action': 'search',
        'replaceSetId': '',
        'goToPageLoc': 'SearchHistoryTableBanner',
        'value(input1)': QUERY,
        'value(searchOp)': 'search',
        'value(select2)': 'LA',
        'value(input2)': '',
        'value(select3)': 'DT',
        'value(input3)': '',
        'x': '60',
        'y': '19',
        'value(limitCount)': '14',
        'limitStatus': 'collapsed',
        'ss_lemmatization': 'On',
        'ss_spellchecking': 'Suggest',
        'SinceLastVisit_UTC': '',
        'SinceLastVisit_DATE': '',
        'period': 'Range Selection',
        'range': 'ALL',
        'startYear': '1945',
        'endYear': '2018',
        'update_back2search_link_param': 'yes',
        'ss_query_language': '',
        'rs_sort_by': 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A',
    }

    r = driver.request('post', url, data=payload)
    driver.get(r.url)
    count = driver.find_element_by_xpath('//*[@id="set_1_div"]/a').text
    return int(count.replace(',', ''))


def summary():
    """
    Page of partial results
    """
    sid = driver.get_cookie('SID')['value'][1:-1]

    params = {'product': 'UA',
              'doc': '1',
              'qid': '1',
              'SID': sid,
              'search_mode': 'AdvancedSearch',
              'update_back2search_link_param': 'yes',
              }
    params = urllib.urlencode(params)

    url = base_url + 'summary.do?' + params

    r = driver.get(url)


#     print r.text


def mark_records(**kwargs_f_t):
    """
    Mark Records to create
    """
    sid = driver.get_cookie('SID')['value'][1:-1]

    # kwargs_f_t['mark_from']
    params = {'product': 'UA',
              'mark_id': 'UDB',
              'qid': '1',
              'search_mode': 'AdvancedSearch',
              'selectedIds': '',
              'colName': '',
              'mark_from': kwargs_f_t['mark_from'],
              'mark_to': kwargs_f_t['mark_to'],
              'markFrom': kwargs_f_t['mark_from'],
              'markTo': kwargs_f_t['mark_to'],
              'MaxDataSetLimit': '',
              'DataSetsRemaining': '',
              'IsAtMaxLimit': '',
              'viewType': 'summary',
              'value(record_select_type)': 'range',
              'SID': sid,
              '': '',
              '': ''
              }

    params = urllib.urlencode(params)

    url = base_url + 'MarkRecords.do?' + params
    r = driver.get(url)


def view_marked_list():
    sid = driver.get_cookie('SID')['value'][1:-1]

    """
    Navigate to get some paramenters
    """
    params = {'action': 'Search',
              'product': 'WOS',
              'colName': 'WOS',
              'mark_id': 'UDB',
              'search_mode': 'MarkedList',
              'SID': sid,
              'entry_prod': 'WOS'
              }
    params = urllib.urlencode(params)

    url = base_url + 'ViewMarkedList.do?' + params
    r = driver.get(url)
    # print r.text.encode('utf8', 'replace')

    # This is the input field to get the qid value
    # '<input type="hidden" name="qid" value="2" />'
    return driver.find_element_by_xpath('//input[@type="hidden" and @name="qid"]').get_attribute('value')



def outbound_service(qid, **kwargs_f_t):
    """
    Entry page via POST, to get BibTex
    """
    url = base_url + 'OutboundService.do?action=go&&&totalMarked=5'
    sid = driver.get_cookie('SID')['value'][1:-1]


    payload = {'displayCitedRefs': 'true',
               'displayTimesCited': 'true',
               'viewType': 'summary',
               'product': 'WOS',
               'mark_id': 'WOS',
               'colName': 'WOS',
               'search_mode': 'AdvancedSearch',
               'locale': 'en_US',
               'view_name': 'WOS-summary',
               'viewType': 'summary',
               'sortBy': 'PY.D;LD.D;SO.A;VL.D;PG.A;AU.A',
               'mode': 'OpenOutputService',
               'qid': qid,
               'SID': sid,
               'format': 'saveToFile',
               'filters': 'PMID AUTHORSIDENTIFIERS ACCESSION_NUM FUNDING SUBJECT_CATEGORY JCR_CATEGORY LANG IDS PAGEC SABBR CITREFC ISSN PUBINFO KEYWORDS CITTIMES ADDRS CONFERENCE_SPONSORS DOCTYPE ABSTRACT CONFERENCE_INFO SOURCE TITLE AUTHORS',
               'count_new_items_marked': '0',
               'IncitesEntitled': 'yes',
               'save_options': 'bibtex',
               'value(ml_output_options)': 'show',
               'value(record_select_type)': 'range',
               'selectedQOFormat': 'enw',
               'saveToMenu': 'other',
               'value(select_All)': 'checked',
               'fields_selection': 'PMID AUTHORSIDENTIFIERS ACCESSION_NUM FUNDING SUBJECT_CATEGORY JCR_CATEGORY LANG IDS PAGEC SABBR CITREFC ISSN PUBINFO KEYWORDS CITTIMES ADDRS CONFERENCE_SPONSORS DOCTYPE ABSTRACT CONFERENCE_INFO SOURCE TITLE AUTHORS',
               # 'queryNatural':'fo=("fundacao de amparo a pesquisa do estado de sao paulo" OR fapesp OR "fundacao de amparo a pesquisa do estado de s paulo" OR "FUNDACAO DE AMPARO PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO DE APOIO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DE SAO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA NO ESTADO DE SAO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTADO SAO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTADO DE SO PAULO" OR "FUNDA AO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO DE AMPAROA PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTADO DE SAO PAOLO" OR "FUNDACAO AMPARO A PEQUISA ESTADO SAO PAULO" OR "FUNDACAO AMPARO A PESQUISA ESTADO DE SAO PAULO" OR "FUNDACAO APOIO A PESQUISA ESTADO SAO PAULO" OR "FUNDACAO DE AMPARO E PESQUISA DO ESTADO DE SAO PAULO" OR "FUND ACAO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDA AO DE AMPARO A PESQUISA DO ESTADO SAO PAULO" OR "FUNDA AO DE AMPARO D PESQUISA DO ESTADO DE SIO PAULO" OR "FUNDA DO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDA DO DE APOIO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDA GO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDAAAO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACA O DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACACO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO DE AMPARA A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO DE AMPARO 5 PESQUISA DO ESTADA DE SAO PAULO" OR "FUNDACAO DE AMPARO 6 PESQUISA DO ESTADO DE SAO" OR "FUNDACAO DE AMPARO A PESQUISA AO ESTADO DE SAO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTACLO DE SAO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTADO CLE SAO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTADO CLE SJO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTADO DA SAO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTADO DE SDO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTADO DE SILO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTADO DE SO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA DO ESTRADO DE SAO PAULO" OR "FUNDACAO DE AMPARO A PESQUISA ESTADO DE SAO PAULO" OR "FUNDACAO DE AMPARO AA PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO DE AMPARO PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO DE AMPAROA A PESQUISA DO ESTADO DAE SO PAULO" OR "FUNDACAO DE APARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO DE ARNPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACAO DE AUXILIO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDACXAO DE AMPARO A PESQUISA NO ESTADO DE SAO PAULO" OR "FUNDAEAO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDAGAO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FUNDAGDO DE AMPARO A PESQUISA DO ESTADO DE SAO PAULO" OR "FOUNDATION FOR THE SUPPORT OF RESEARCH IN THE STATE OF SAO PAULO" OR "FOUNDATION FOR RESEARCH SUPPORT OF THE STATE OF SAO PAULO" OR "FOUNDATION FOR THE SUPPORT OF RESEARCH OF THE STATE OF SAO PAULO" OR "FOUNDATION FOR RESEARCH ASSISTANCE SAO PAULO STATE" OR "FOUNDATION FOR RESEARCH SUPPORT OF THE STATE OF SAO PAULO" OR "FOUNDATION FOR RESEARCH OF THE STATE OF SAO PAULO" OR "FOUNDATION FOR RESEARCH SUPPORT OF SAO PAULO STATE" OR "FOUNDATION FOR RESEARCH SUPPORT OF THE SAO PAULO STATE" OR "FOUNDATION FOR RESEARCH SUPPORT SAO PAULO" OR "FOUNDATION FOR SCIENTIFIC RESEARCH OF SAO PAULO STATE" OR "FOUNDATION FOR SUPPORT OF RESEARCH IN THE STATE OF SAO PAULO" OR "FOUNDATION OF SUPPORT TO RESEARCH FROM STATE OF SAO PAULO" OR "FOUNDATION TO SUPPORT RESEARCH OF THE STATE OF SAO PAULO" OR "FOUNDATIONS THAT SUPPORT RESEARCH IN THE STATE OF SAO PAULO" OR "Sao Paulo State Research Foundation")',
               'queryNatural': QUERY,

               'use_two_ets': 'false',

               'totalMarked': kwargs_f_t['publ_per_file'],
               'mark_from': '1',
               'mark_to': kwargs_f_t['publ_per_file'],
               'markFrom': '1',
               'markTo': kwargs_f_t['publ_per_file'],
               }

    r = driver.request('post', url, data=payload)
    # driver.get(r.url)

    """
    Alteracao no script em 21/10/2015.
    A partir dessa data, os dados passaram a ser entregue diretamente no response apos o pedido do mesmo.
    Antes era necessario gerar um arquivo e fazer o download. Agora jah vem no r.content.

    """
    diretorio = '/var/tmp/bibtex/'
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)
    output = 'output_' + kwargs_f_t['idx'] + '.bib'
    with open(diretorio+output, 'wb') as handle:
        handle.write(r.content)
    print 'nois'




def cleanup_marked_list(qid):
    """
    Just as the name says, clean the marked list
    """
    sid = driver.get_cookie('SID')['value'][1:-1]
    params = {'search_mode': 'MarkedList',
              'product': 'UA',
              'mark_id': 'UDB',
              'qid': qid,
              'SID': sid
              }
    params = urllib.urlencode(params)

    url = base_url + 'DeleteMarked.do?' + params
    r = driver.get(url)


def get_files(**kwargs_f_t):
    """
    Loop urls functions defined above and get the files
    """
    print 'FROM: ' + kwargs_f_t['mark_from']
    print 'TO: ' + kwargs_f_t['mark_to']

    print 'Summary'
    summary()
    print 'End Summary'

    print 'Mark Records'
    mark_records(**kwargs_f_t)
    print 'End Mark Records'

    print "Get qid"
    qid = view_marked_list()
    print "End Get qid"

    print "Outbound"
    outbound_service(qid, **kwargs_f_t)
    print "End Outbound"

    # print "Get BibTex"
    # ets(qid, **kwargs_f_t)
    # print "End Get BibTex"

    print "Cleanup Marked List"
    cleanup_marked_list(qid)
    print "End Cleanup Marked List"


def loop_the_server(qt_publ):
    """
    Reveices qt of publications, split by 500 and get the bibtex file
    """
    print qt_publ

    # Number of register per BibTex file. Max = 500
    publ_per_file = 500

    times, rest = divmod(qt_publ, publ_per_file)
    print 'TIMES: ' + str(times)
    print 'REST: ' + str(rest)

    idx = 1

    # Controls the publications marked (max = 500)
    mark_from = 1
    mark_to = publ_per_file
    kwargs_f_t = {}

    # times = 2

    while (idx <= times):
        kwargs_f_t = {'mark_from': str(mark_from),
                      'mark_to': str(mark_to),
                      'idx': str(idx),
                      'publ_per_file': str(publ_per_file)
                      }
        get_files(**kwargs_f_t)

        idx += 1
        mark_from += publ_per_file
        mark_to += publ_per_file

    print "\n\n\nEND WHILE"
    # get the rest
    if rest > 0:
        mark_to = mark_from + rest - 1

        kwargs_f_t = {'mark_from': str(mark_from),
                      'mark_to': str(mark_to),
                      'idx': str(idx),
                      'publ_per_file': str(publ_per_file)
                      }
        get_files(**kwargs_f_t)
    print "END REST"


print "Get sid"
ua_advanced_search_input()
print "End Get sid"

print "Post query"
qt_publ = ua_advanced_search()
print "End Post query"

print "Loop the server"
# qt_publ = int('71,326'.replace(",", ""))
loop_the_server(qt_publ)
print "End loop the server"

driver.close()
