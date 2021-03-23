from django import template

register = template.Library()


@register.simple_tag
def check_bill(bill_number, congress):
    if bill_number[:len(str(congress))] == str(congress):
        return True
    return False
