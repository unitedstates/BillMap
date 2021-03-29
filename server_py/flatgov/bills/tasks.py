from celery import shared_task, states
import requests
import json
from django.conf import settings
from .models import PressStatement, PressStatementTask



@shared_task
def scrape_press_statements_task(url, press_statement_task_id):
    self = scrape_press_statements_task
    press_statement_task = PressStatementTask.objects.get(id=press_statement_task_id)
    press_statement_task.task_id = self.AsyncResult(self.request.id).task_id
    press_statement_task.save()
    
    headers = {
        'x-api-key': settings.PROPUBLICA_CONGRESS_API_KEY
    }

    has_data = True
    next_offset = 0
    count = 0

    while has_data:
        offset_url = url + str(next_offset)
        response = requests.request("GET", offset_url, headers=headers)
        offset_data = json.loads(response.text)['results']
        if not offset_data:
            has_data = False
        for data in offset_data:
            count += 1
            print(count, offset_url)
            press_statement = PressStatement()
            press_statement.congress = press_statement_task.congress
            press_statement.bill_number = press_statement_task.bill_number
            press_statement.title = data['title']
            press_statement.url = data['url']
            press_statement.date = data['date']
            press_statement.statement_type = data['statement_type']
            press_statement.member_id = data['member_id']
            press_statement.member_uri = data['member_uri']
            press_statement.name = data['name']
            press_statement.chamber = data['chamber']
            press_statement.state = data['state']
            press_statement.party = data['party']
            press_statement.save()


        next_offset += 20
    
    press_statement_task.status = states.SUCCESS
    press_statement_task.save()
