import os
import requests
import json
import time
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve(strict=True).parent
FILE_PATH = os.path.join(BASE_DIR, 'commitee_report_detail_urls.json')

def url(path):
    return (
        'https://www.govinfo.gov/wssearch/rb/crpt/'
        + str(path)
        + '/?fetchChildrenOnly=1'
    )
    
def get_response_in_json(path):
    response = requests.get(url(path))
    return json.loads(response.text)

def get_detail_urls(last_congress):
    count = 0
    if last_congress:
        first_congress = last_congress
    else:
        first_congress = 103
    with open(FILE_PATH, 'w') as crec_file:
        current_year = datetime.today().year
        current_congress = (current_year - 1787) // 2
        for congress_number in range(current_congress, first_congress, -1):
            data = get_response_in_json(congress_number)
            #print(data['childNodes'].__len__())
            for child_node in data['childNodes']:
                #print(child_node.keys())
                node_value = child_node['nodeValue']
                
                #print(node_value.keys())
                browse_path_alias = node_value['browsePathAlias']
                print('----', browse_path_alias)
                data = get_response_in_json(browse_path_alias)


                for child_node in data['childNodes']:
                    count += 1
                    granuleID = child_node['nodeValue']['granuleid']
                    packageID = child_node['nodeValue']['packageid']
                    detail_url = 'https://www.govinfo.gov/wssearch/getContentDetail?packageId='+str(packageID)+'&granuleId='+str(granuleID)
                    print('-----', count)
                    crec_file.write(detail_url+'\n')
            print(congress_number)
    print(count)
    return current_congress - 1
