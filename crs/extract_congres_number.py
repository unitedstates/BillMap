import re

def extract_congres_number(bill_number):
    match = re.match(r"([0-9]+)([a-z]+)([0-9]+)", bill_number, re.I)
    congres_number = None
    report_string = None

    if match:
        congres_number = match.group(1)
        report_string = match.group(2) + match.group(3)

    return {"congres_number": congres_number, "report_string" : report_string}