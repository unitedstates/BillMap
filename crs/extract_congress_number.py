import re

def extract_congress_number(bill_number):
    match = re.match(r"([0-9]+)([a-z]+)([0-9]+)", bill_number, re.I)
    congress_number = None
    report_string = None

    if match:
        congress_number = match.group(1)
        report_string = match.group(2) + match.group(3)

    return {"congress_number": congress_number, "report_string" : report_string}