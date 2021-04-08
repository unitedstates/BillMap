import requests
from requests.api import get
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Download and process data from:
LEGISLATORS_URL = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml'
LEGISLATORS_HIST_URL = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-historical.yaml'
COMMITTEE_MEMBERSHIP_URL = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/committee-membership-current.yaml'
COMMITTEES_URL = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/committees-current.yaml'

def getAndParseYAML(url):
    response = requests.get(url, allow_redirects=True)
    return yaml.load(response.content, Loader=Loader)

legislators = getAndParseYAML(LEGISLATORS_URL)
legislators_hist = getAndParseYAML(LEGISLATORS_HIST_URL)
committee_membership = getAndParseYAML(COMMITTEE_MEMBERSHIP_URL)
committees = getAndParseYAML(COMMITTEES_URL)

"""
SAMPLES

legislators[0]
{'id': {'bioguide': 'B000944',
  'thomas': '00136',
  'lis': 'S307',
  'govtrack': 400050,
  'opensecrets': 'N00003535',
  'votesmart': 27018,
  'fec': ['H2OH13033', 'S6OH00163'],
  'cspan': 5051,
  'wikipedia': 'Sherrod Brown',
  'house_history': 9996,
  'ballotpedia': 'Sherrod Brown',
  'maplight': 168,
  'icpsr': 29389,
  'wikidata': 'Q381880',
  'google_entity_id': 'kg:/m/034s80'},
 'name': {'first': 'Sherrod',
  'last': 'Brown',
  'official_full': 'Sherrod Brown'},
 'bio': {'birthday': '1952-11-09', 'gender': 'M'},
 'terms': [{'type': 'rep',
   'start': '1993-01-05',
   'end': '1995-01-03',
   'state': 'OH',
   'district': 13,
   'party': 'Democrat'},
  {'type': 'rep',
   'start': '1995-01-04',
   'end': '1997-01-03',
   'state': 'OH',
   'district': 13,
   'party': 'Democrat'},
  {'type': 'rep',
   'start': '1997-01-07',
   'end': '1999-01-03',
   'state': 'OH',
   'district': 13,
   'party': 'Democrat'},
  {'type': 'rep',
   'start': '1999-01-06',
   'end': '2001-01-03',
   'state': 'OH',
   'district': 13,
   'party': 'Democrat'},
  {'type': 'rep',
   'start': '2001-01-03',
   'end': '2003-01-03',
   'state': 'OH',
   'district': 13,
   'party': 'Democrat'},
  {'type': 'rep',
   'start': '2003-01-07',
   'end': '2005-01-03',
   'state': 'OH',
   'district': 13,
   'party': 'Democrat',
   'url': 'http://www.house.gov/sherrodbrown'},
  {'type': 'rep',
   'start': '2005-01-04',
   'end': '2007-01-03',
   'state': 'OH',
   'district': 13,
   'party': 'Democrat',
   'url': 'http://www.house.gov/sherrodbrown'},
  {'type': 'sen',
   'start': '2007-01-04',
   'end': '2013-01-03',
   'state': 'OH',
   'class': 1,
   'party': 'Democrat',
   'url': 'http://brown.senate.gov/',
   'address': '713 HART SENATE OFFICE BUILDING WASHINGTON DC 20510',
   'phone': '202-224-2315',
   'fax': '202-228-6321',
   'contact_form': 'http://www.brown.senate.gov/contact/',
   'office': '713 Hart Senate Office Building'},
  {'type': 'sen',
   'start': '2013-01-03',
   'end': '2019-01-03',
   'state': 'OH',
   'party': 'Democrat',
   'class': 1,
   'url': 'https://www.brown.senate.gov',
   'address': '713 Hart Senate Office Building Washington DC 20510',
   'phone': '202-224-2315',
   'fax': '202-228-6321',
   'contact_form': 'http://www.brown.senate.gov/contact/',
   'office': '713 Hart Senate Office Building',
   'state_rank': 'senior',
   'rss_url': 'http://www.brown.senate.gov/rss/feeds/?type=all&amp;'},
  {'type': 'sen',
   'start': '2019-01-03',
   'end': '2025-01-03',
   'state': 'OH',
   'class': 1,
   'party': 'Democrat',
   'state_rank': 'senior',
   'url': 'https://www.brown.senate.gov',
   'rss_url': 'http://www.brown.senate.gov/rss/feeds/?type=all&amp;',
   'contact_form': 'http://www.brown.senate.gov/contact/',
   'address': '503 Hart Senate Office Building Washington DC 20510',
   'office': '503 Hart Senate Office Building',
   'phone': '202-224-2315'}]}

   ===

legislators_hist[0] 
{'id': {'bioguide': 'B000226',
  'govtrack': 401222,
  'icpsr': 507,
  'wikipedia': 'Richard Bassett (Delaware politician)',
  'wikidata': 'Q518823',
  'google_entity_id': 'kg:/m/02pz46'},
 'name': {'first': 'Richard', 'last': 'Bassett'},
 'bio': {'birthday': '1745-04-02', 'gender': 'M'},
 'terms': [{'type': 'sen',
   'start': '1789-03-04',
   'end': '1793-03-03',
   'state': 'DE',
   'class': 2,
   'party': 'Anti-Administration'}]}

   ===
committee_membership.keys()
dict_keys(['SSAF', 'SSAF13', 'SSAF14', 'SSAF17', 'SSAF16', 'SSAF15', 'SSAP', 'SSAP01', 'SSAP16', 'SSAP02', 'SSAP14', 'SSAP17', 'SSAP18', 'SSAP22', 'SSAP23', 'SSAP08', 'SSAP19', 'SSAP20', 'SSAP24', 'SSAS', 'SSAS14', 'SSAS21', 'SSAS20', 'SSAS17', 'SSAS15', 'SSAS13', 'SSAS16', 'SSBK', 'SSBK12', 'SSBK08', 'SSBK09', 'SSBK05', 'SSBK04', 'SSCM', 'SSCM28', 'SSCM26', 'SSCM29', 'SSCM30', 'SSCM31', 'SSCM32', 'SSEG', 'SSEG01', 'SSEG04', 'SSEG03', 'SSEG07', 'SSEV', 'SSEV10', 'SSEV15', 'SSEV09', 'SSEV08', 'SSFI', 'SSFI12', 'SSFI14', 'SSFI10', 'SSFI13', 'SSFI02', 'SSFI11', 'SSFR', 'SSFR09', 'SSFR02', 'SSFR01', 'SSFR15', 'SSFR07', 'SSFR14', 'SSFR06', 'SSHR', 'SSHR09', 'SSHR11', 'SSHR12', 'SSGA', 'SSGA20', 'SSGA22', 'SSGA01', 'SLIA', 'SSRA', 'SSSB', 'SSBU', 'SSJU', 'SSJU01', 'SSJU04', 'SSJU22', 'SSJU26', 'SSJU25', 'SSJU21', 'SSVA', 'JSPR', 'JSTX', 'JSLC', 'JSEC', 'SLET', 'SLIN', 'SPAG', 'SCNC', 'JCSE', 'HSAG', 'HSAP', 'HSAS', 'HSBA', 'HSBU', 'HSCN', 'HSED', 'HSFA', 'HSGO', 'HSHA', 'HSHM', 'HSIF', 'HLIG', 'HSII', 'HSJU', 'HSMH', 'HSPW', 'HSRU', 'HSSM', 'HSSO', 'HSSY', 'HSVR', 'HSWM'])
   ===

committees[0]
{'type': 'house',
 'name': 'House Committee on Agriculture',
 'url': 'https://agriculture.house.gov/',
 'minority_url': 'https://republicans-agriculture.house.gov',
 'thomas_id': 'HSAG',
 'house_committee_id': 'AG',
 'subcommittees': [{'name': 'Conservation and Forestry',
   'thomas_id': '15',
   'address': '1301 LHOB; Washington, DC 20515',
   'phone': '(202) 225-2171'},
  {'name': 'Commodity Exchanges, Energy, and Credit',
   'thomas_id': '22',
   'address': '1301 LHOB; Washington, DC 20515',
   'phone': '(202) 225-2171'},
  {'name': 'General Farm Commodities and Risk Management',
   'thomas_id': '16',
   'address': '1301 LHOB; Washington, DC 20515',
   'phone': '(202) 225-2171'},
  {'name': 'Livestock and Foreign Agriculture',
   'thomas_id': '29',
   'address': '1301 LHOB; Washington, DC 20515',
   'phone': '(202) 225-2171'},
  {'name': 'Biotechnology, Horticulture, and Research',
   'thomas_id': '14',
   'address': '1301 LHOB; Washington, DC 20515',
   'phone': '(202) 225-2171'},
  {'name': 'Nutrition, Oversight, and Department Operations',
   'thomas_id': '03',
   'address': '1301 LHOB; Washington, DC 20515',
   'phone': '(202) 225-2171'}],
 'address': '1301 LHOB; Washington, DC 20515-6001',
 'phone': '(202) 225-2171',
 'rss_url': 'https://agriculture.house.gov/Rss.aspx?GroupID=1',
 'jurisdiction': 'The House Committee on Agriculture has legislative jurisdiction over agriculture, food, rural development, and forestry.'}
"""