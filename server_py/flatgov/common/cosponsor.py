import requests
from requests.api import get
import yaml

from bills.models import Committee, Cosponsor
from bills.views import deep_get 
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

def updateLegislators():
    """
    Add legislator data to database. 
    Download and parse YAML for legislators, then add or update fields.
    ** SAMPLE **
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
  ...]}
    """
    legislatorids = getAndParseYAML(LEGISLATORS_URL)
    for legislatorid in legislatorids:
        legislator = legislatorid.get("id")
        name_first = deep_get(legislatorid, "name", "first")
        name_last = deep_get(legislatorid, "name", "last")
        if not name_first:
            name_first = ""
        if not name_last:
            name_last = ""
        name = ", ".join([name_last, name_first])
        Cosponsor.objects.update_or_create(name=name, 
                                    name_full_official=legislator.get("name"),
                                    defaults={
                                        'name_first': name_first, 
                                        'name_last': name_last,
                                        'bioguide_id': legislator.get("bioguide", ""),
                                        'thomas': legislator.get("thomas", ""),
                                        'party': legislatorid.get("party", ""),
                                        'state': legislatorid.get("state", ""),
                                        'type': legislatorid.get("type", ""),
                                        'terms': legislatorid.get("terms", []),
                                    }
                            )

def updateCommittees():
    """
    Add committee data to database. 
    Download and parse YAML for committees, then add or update fields.
    *** SAMPLE ***
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
    committees = getAndParseYAML(COMMITTEES_URL)
    # TODO add committee data to db
    for committee in committees:
        thomas_id = committee.get('thomas_id', '')
        jurisdiction = committee.get('jurisdiction', '')
        if len(jurisdiction) > 250:
            jurisdiction = jurisdiction[:249]
        if not thomas_id:
            continue
        Committee.objects.update_or_create(
        thomas_id = committee.get('thomas_id'), defaults={
            'type': committee.get('type', ''),
            'name': committee.get('name', ''),
            'url': committee.get('url', ''),
            'minority_url': committee.get('minority_url', ''),
            'house_committee_id': committee.get('house_committee_id', ''),
            'jurisdiction': jurisdiction 
        }
        )

#TODO define relationship of historical legislators
# in database
def updateLegislatorsHist():
    legislators_hist = getAndParseYAML(LEGISLATORS_HIST_URL)

# TODO create join table and associate members with committees
def updateCommitteeMembers():
    committee_membership = getAndParseYAML(COMMITTEE_MEMBERSHIP_URL)

"""
SAMPLES

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


"""