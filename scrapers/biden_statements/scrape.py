from bs4 import BeautifulSoup as bs4
import requests
import re
import json

url = 'https://www.whitehouse.gov/omb/statements-of-administration-policy/'

response = requests.get(url)

soup = bs4(response.text, 'html.parser')

con = soup.find('section', {'class': 'body-content'})
con = con.find('div', {'class': 'row'})
print('---', con)
ps = con.findAllNext('p')[1:]
print(len(ps))
data = []
count = 0
new = {
    'url': '',
    'link': '',
    'link_text': '',
    'bill_number': '',
    'date_issued': '',
    'congress': '',
}

def get_congress_number(year):
    congress = 0
    const_year = 2022
    const_congress = 117
    dif = const_year - int(year)
    congress = const_congress - (dif // 2)
    return congress

for i in range(len(ps)):
    new['date_issued'] = ps[i].text.split('(')[-2].split(')')[0]
    print(new['date_issued'])
    count+=1
    new['link'] = ps[i].find('a', href=True)['href']
    # print(ps[i].find('a', href=True)['href'])
    year = new['date_issued'][-4:]
    a_text = ps[i].find('a').text
    new['link_text'] = a_text
    q = re.sub(r'\s', '', a_text.split('–')[0])
    qw = re.sub(r'\.', '', q)
    new['bill_number'] = qw.split('—')[0]
    new['congress'] = get_congress_number(year)
    print(new['congress'])

    new['url'] = url
    with open('../../server_py/flatgov/biden_data.json', 'a+') as meta_write_file:
        json.dump(new, meta_write_file, indent=4)

