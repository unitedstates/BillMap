from django import template

register = template.Library()


@register.simple_tag
def check_bill(bill_number: str, congress: int):
    if bill_number[:len(str(congress))] == str(congress):
        return True
    return False

@register.simple_tag
def check_billnumbers_congress(bill_numbers: list, congress: int):
    return any( check_bill(bill_number, congress) for bill_number in bill_numbers)