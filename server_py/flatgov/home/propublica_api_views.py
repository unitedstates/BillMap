from django.http import JsonResponse
from django.views import View
import json
from django.conf import settings
import requests


class GetPressStatementsAPIView(View):
    """Getting the data from propublica and returning for datatable serverside rendering"""
    def get(self, request, congress, bill_type, bill_number):
        offset = request.GET['start']
        url = f'https://api.propublica.org/congress/v1/{congress}/bills/{bill_type}{bill_number}/statements.json?offset={offset}'
        propublica_api_key = getattr(settings, "PROPUBLICA_CONGRESS_API_KEY", None)
        headers = {
            'x-api-key': propublica_api_key
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.content)
        processed_data = {
            "recordsTotal":  data.get('num_results', 0),
            "recordsFiltered": data.get('num_results', 0),
            'data': data.get('results', [])
        }
        return JsonResponse(processed_data)
