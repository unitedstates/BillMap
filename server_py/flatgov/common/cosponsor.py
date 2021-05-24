import requests
from requests.api import get
import yaml

from bills.models import Committee, Cosponsor, Bill
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

  LEADERSHIP SAMPLE:
  - id:
    bioguide: P000197
    thomas: '00905'
    govtrack: 400314
    opensecrets: N00007360
    votesmart: 26732
    icpsr: 15448
    fec:
    - H8CA05035
    cspan: 6153
    wikipedia: Nancy Pelosi
    house_history: 19519
    ballotpedia: Nancy Pelosi
    maplight: 408
    wikidata: Q170581
    google_entity_id: kg:/m/012v1t
  name:
    first: Nancy
    last: Pelosi
    official_full: Nancy Pelosi
  bio:
    birthday: '1940-03-26'
    gender: F
  leadership_roles:
  - title: House Minority Leader
    chamber: house
    start: '2011-01-05'
    end: '2013-01-03'
  - title: House Minority Leader
    chamber: house
    start: '2013-01-03'
    end: '2015-01-03'
  - title: House Minority Leader
    chamber: house
    start: '2015-01-06'
    end: '2017-01-03'
  - title: House Minority Leader
    chamber: house
    start: '2017-01-03'
    end: '2019-01-03'
  - title: Speaker of the House
    chamber: house
    start: '2019-01-03'
    end: '2021-01-03'
  - title: Speaker of the House
    chamber: house
    start: '2021-01-03'
    """
    legislatorids = getAndParseYAML(LEGISLATORS_URL)
    for legislator in legislatorids:
        legislatorid = legislator.get("id")
        name_first = deep_get(legislator, "name", "first")
        name_last = deep_get(legislator, "name", "last")
        if not name_first:
            name_first = ""
        if not name_last:
            name_last = ""
        name = ", ".join([name_last, name_first])
        full_official = deep_get(legislator, "name", "official_full")
        terms = legislator.get("terms", [])
        terms.reverse()
        if terms and len(terms) > 0:
            type = terms[0].get('type', '')
            party = terms[0].get('party', '')
            state = terms[0].get('state', '')
        else:
            type = ""
            party = ""
            state = ""
        leadership = legislator.get('leadership_roles', [])
        updateData = {'name_first': name_first, 
                      'name_last': name_last,
                      'bioguide_id': legislatorid.get("bioguide", ""),
                      'thomas': legislatorid.get("thomas", ""),
                      'party': party, 
                      'state': state,
                      'type': type, 
                      'terms': terms,
                                    }
        if leadership:
            #print('{0}\n'.format(full_official))
            #print(leadership)
            # Reorder so that most current is first
            leadership.reverse()
            updateData['leadership'] = leadership
        #else:
        #    print('No leadership roles for: {0}\n'.format(full_official))
        

        if not full_official:
          continue
        print('Updating legislator: {0}'.format(full_official))
        Cosponsor.objects.update_or_create(name=name, 
                                    name_full_official=full_official,
                                    defaults=updateData
                            )

def updateCommittees():
    """
    add committee data to database. 
    download and parse yaml for committees, then add or update fields.
    *** sample ***
{'type': 'house',
 'name': 'house committee on agriculture',
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
    """
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
    """
    legislators_hist = getAndParseYAML(LEGISLATORS_HIST_URL)

def updateCommitteeMembers():
    """
     c.get('HSGO')
[{'name': 'Carolyn B. Maloney',
  'party': 'majority',
  'rank': 1,
  'title': 'Chairman',
  'bioguide': 'M000087'},
 {'name': 'James Comer',
  'party': 'minority',
  'rank': 1,
  'title': 'Ranking Member',
  'bioguide': 'C001108'},
 {'name': 'Eleanor Holmes Norton',
  'party': 'majority',
  'rank': 2,
  'bioguide': 'N000147'},
 {'name': 'Jim Jordan', 'party': 'minority', 'rank': 2, 'bioguide': 'J000289'},
 {'name': 'Stephen F. Lynch',
  'party': 'majority',
  'rank': 3,
  'bioguide': 'L000562'},...
  ]
    """
    committee_membership = getAndParseYAML(COMMITTEE_MEMBERSHIP_URL)
    for committee_thomas_id, cosponsor_items in committee_membership.items():
        print('Committee id: {0}'.format(committee_thomas_id))
        try:
            committee_item = Committee.objects.get(thomas_id=committee_thomas_id)
        except Exception as err:
            print(err)
            continue
        if committee_item:
            for cosponsor_item in cosponsor_items:
                bioguide = cosponsor_item.get('bioguide', '')
                if bioguide:
                    cosponsor = Cosponsor.objects.filter(bioguide_id=bioguide).first()
                    if cosponsor:
                        committee_item.cosponsors.add(cosponsor)
                        cosponsor_item['committee'] = committee_thomas_id
                        if not cosponsor.committees:
                            cosponsor.committees = [cosponsor_item] 
                        else:
                            cosponsor.committees.append(cosponsor_item) 
                        cosponsor.save()


# Add cosponsors from cosponsors dict to join table for each bill 
def updateBillCosponsorJoinTable():
  bills_query_set = Bill.objects.all().only('bill_congress_type_number', 'cosponsors_dict')
  for bill in bills_query_set:
    bCTN =  bill.bill_congress_type_number
    if not bCTN:
      continue
    print('Adding cosponsors for ', bCTN)
    cosponsors_dict = bill.cosponsors_dict
    sponsor = bill.sponsor
    if not sponsor and not cosponsors_dict:
      continue
    if sponsor:
      cosponsors_dict.append(sponsor)
    for cosponsor_item in cosponsors_dict:
      bioguide_id = cosponsor_item.get('bioguide_id', '')
      if bioguide_id != '':
        cosponsor = Cosponsor.objects.filter(bioguide_id=bioguide_id).first()
        if cosponsor:
          bill.cosponsors.add(cosponsor)
        else:
          pass

def updateCosponsorAndCommittees():
    Committee.objects.all().delete()
    Cosponsor.objects.all().delete()
    updateLegislators()
    updateCommittees()
    updateCommitteeMembers()
    updateBillCosponsorJoinTable()
