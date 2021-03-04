import requests
import json
import time

def url(path):
    return (
        'https://www.govinfo.gov/wssearch/rb/crpt/'
        + str(path)
        + '/?fetchChildrenOnly=1'
    )
    
def get_response_in_json(path):
    response = requests.get(url(path))
    return json.loads(response.text)

def get_detail_data(url):
    crec_data = {}
    time.sleep(0.0)
    response = requests.get(url)

    data = json.loads(response.text)
    #print('-----------', data.keys())
    crec_data['title'] = data['title']
    crec_data['pdf_link'] = data['download']['pdflink']
    for col in data['metadata']['columnnamevalueset']:
        #print(col)
        if col['colname'] == 'Category':
            crec_data['category'] = col['colvalue']
        elif col['colname'] == 'Report Type':
            crec_data['report_type'] = col['colvalue']
        elif col['colname'] == 'Report Number':
            crec_data['report_number'] = col['colvalue']
        elif col['colname'] == 'Date':
            crec_data['date'] = ' '.join(col['colvalue'].split())
        elif col['colname'] == 'Committee':
            crec_data['committee'] = col['colvalue']
        elif col['colname'] == 'Associated Legislation':
            crec_data['associated_legistation'] = col['colvalue']
    return crec_data 

count = 0
with open('crec_detail_urls.json', 'r') as file:
    urls = file.read().split('\n')
with open('crec_data.json', 'a+') as crec_file:
            
    for i, url in enumerate(urls):
        try:
            crec_data = get_detail_data(url)
            print(crec_data)
            print(i, url)
            json.dump(crec_data, crec_file, indent=4)
        except Exception as e:
            print('----- error', i, url)


print(count)
