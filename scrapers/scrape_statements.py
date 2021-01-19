from bs4 import BeautifulSoup as bs4
import requests
import re
import json

url = 'https://www.whitehouse.gov/omb/statements-of-administration-policy/'

response = requests.get(url)

soup = bs4(response.text, 'html.parser')

con = soup.find('div', {'class': 'page-content__content editor'})

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
    'congres': '',
}


for i in range(len(ps)):
    
    if ps[i].text.find('Administration Policy on') != -1:
        
        new['date_issued'] = ps[i].text.split('on')[-1]
        # print(new, count)
        # data.append(ps[i])
        pass
    else:
        
        if ps[i].text.find('Administration Policy on') != -1:
            new['date_issued'] = ps[i].text.split('on')[-1]
        else:
            count+=1
            new['link'] = ps[i].find('a', href=True)['href']
            # print(ps[i].find('a', href=True)['href'])
            a_text = ps[i].find('a').text
            new['link_text'] = a_text
            q = re.sub(r'\s', '', a_text.split('–')[0])
            qw = re.sub(r'\.', '', q)
            # print()
            new['bill_number'] = qw.split('—')[0]
            
            print(new['date_issued'][-2:])
            if new['date_issued'][-2:] in ['15', '16']:
                new['congres'] = '114'
            elif new['date_issued'][-2:] in ['17', '18']:
                new['congres'] = '115'
            elif new['date_issued'][-2:] in ['19', '20']:
                new['congres'] = '116'
            elif new['date_issued'][-2:] in ['21', '22']:
                new['congres'] = '117'
            new['url'] = url
            with open('data.json', 'a+') as meta_write_file:
                json.dump(new, meta_write_file, indent=4)


print(count)
print(new)