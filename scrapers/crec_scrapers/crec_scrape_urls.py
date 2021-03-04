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

def get_detail_data(granuleID, packageID, congress_number):
    crec_data = {}
    time.sleep(0.0)
    response = requests.get('https://www.govinfo.gov/wssearch/getContentDetail?packageId='+str(packageID)+'&granuleId='+str(granuleID))

    data = json.loads(response.text)
    #print('-----------', data.keys())
    crec_data['title'] = data['title']
    crec_data['pdf_link'] = data['download']['pdflink']
    crec_data['congress'] = congress_number
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
with open('crec_detail_urls.json', 'a+') as crec_file:
    for congress_number in range(104, 118):
        data = get_response_in_json(congress_number)
        #print(data['childNodes'].__len__())
        for child_node in data['childNodes']:
            #print(child_node.keys())
            node_value = child_node['nodeValue']
            
            #print(node_value.keys())
            browse_path_alias = node_value['browsePathAlias']
            print('----', browse_path_alias)
            data = get_response_in_json(browse_path_alias)
            #print(data.keys())
            #print(len(data['childNodes']))


            for child_node in data['childNodes']:
                count += 1     
                #print(child_node.keys())
                granuleID = child_node['nodeValue']['granuleid']
                packageID = child_node['nodeValue']['packageid']
                #print(granuleID)
                #print(packageID)
                detail_url = 'https://www.govinfo.gov/wssearch/getContentDetail?packageId='+str(packageID)+'&granuleId='+str(granuleID)
                print(url)
                print('-----', count)
                crec_file.write(detail_url+'\n')
                # json.dump(crec_data, crec_file, indent=4)
        print(congress_number)
print(count)
