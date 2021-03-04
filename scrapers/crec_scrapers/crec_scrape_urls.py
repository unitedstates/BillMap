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
                granuleID = child_node['nodeValue']['granuleid']
                packageID = child_node['nodeValue']['packageid']
                detail_url = 'https://www.govinfo.gov/wssearch/getContentDetail?packageId='+str(packageID)+'&granuleId='+str(granuleID)
                print(url)
                print('-----', count)
                crec_file.write(detail_url+'\n')
        print(congress_number)
print(count)
