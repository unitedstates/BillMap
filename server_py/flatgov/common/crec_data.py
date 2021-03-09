import json
from bills.models import CommitteeDocument
from django.conf import settings
from . import constants
import re

def get_congress_number(date):
    year = date.split()[-1]

    congress = 0
    const_year = 2022
    const_congress = 117
    dif = const_year - int(year)
    congress = const_congress - (dif // 2)
    return congress

def json_validator():
    with open(settings.BASE_DIR / 'crec_data.json', 'r') as a_file:
        lines = a_file.readlines()
        new_lines = []
        for line in lines:
            if line.split()[0] == '}{':
                line = re.sub('}{', '},{', line)
            new_lines.append(line)
    with open(settings.BASE_DIR / 'crec_data.json', 'w') as f:
        f.write("[\n")
        for line in new_lines:
            f.write('    '+line)
        f.write("]\n")


def crec_loader():

    try:
        with open(settings.BASE_DIR / 'crec_data.json', 'r') as file:
            data = json.loads(file.read())
            print(len(data))
    except Exception as e:
        with open(settings.BASE_DIR / 'crec_data.json', 'r') as file:
            print('---- file is not valid', e)
            json_validator()
            data = json.loads(file.read())


    for crec_data in data:
        
        try:
            crec = CommitteeDocument()
            crec.title = crec_data['title']
            crec.category = crec_data['category']
            crec.committee = crec_data['committee']
            crec.report_number = ''.join(crec_data['report_number'].split('&nbsp;'))
            crec.associated_legislation = ''.join(crec_data['associated_legislation'].split('&nbsp;'))
            crec.original_pdf_link = crec_data['pdf_link']
            crec.bill_number = re.sub('\ |\?|\.|\!|\/|\;|\:|\-|\(|\)', '', ''.join(crec_data['associated_legislation'].split('&nbsp;'))).lower()
            crec.chamber = crec_data['report_type'].split()[0]
            crec.report_type = crec_data['report_type']
            crec.date = crec_data['date']
            crec.congress = get_congress_number(crec_data['date'])
            crec.save()
        except Exception as e:
            print('-----', e)
        