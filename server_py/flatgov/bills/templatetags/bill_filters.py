from django import template
from django.template.defaultfilters import stringfilter
from datetime import date, timedelta
from common import constants


# BILL_NUMBER_REGEX = r'(?P<congress>[1-9][0-9]*)(?P<stage>[a-z]+)(?P<number>[0-9]+)(?P<version>[a-z]+)?$'

stagesFormat = {
    'S': 'S.',
    'HR': 'H.R.',
    'HRES': 'H.Res.',
    'HJRES': 'H.J.Res.',
    'HCONRES': 'H.Con.Res.',
    'SJRES': 'S.J.Res.',
    'SCONRES': 'S.Con.Res.',
    'SRES': 'S.Res.'
}

register = template.Library()


@register.filter
@stringfilter
def billnumber_display(billnumber: str):
    billMatch = constants.BILL_NUMBER_REGEX_COMPILED.match(billnumber) 
    if billMatch and billMatch.groupdict():
        billMatchGroups = billMatch.groupdict()
        congress = billMatchGroups.get('congress', '')
        stage = billMatchGroups.get('stage', '')
        number = billMatchGroups.get('number', '')
        stage_fmt = stagesFormat.get(stage.upper(), stage)
        if congress != constants.CURRENT_CONGRESS:
           billnumber_fmt = f' {stage_fmt} {number} ({congress})'
        else:
           billnumber_fmt = f' {stage_fmt} {number}'
        return billnumber_fmt
        
    else:
        return billnumber

@register.filter
def billnumbers_display(billnumbers: list):
    if isinstance(billnumbers, str):
        billnumbers = billnumbers.split(', ')
    return [billnumber_display(billnumber) for billnumber in list(billnumbers)]

@register.filter
@stringfilter
def cosponsor_name_display(name: str) -> str:
    """
    Converts "Waters, Maxine" to "Maxine Waters"
    TODO: Handle middle names or other variations

    Args:
        name (str): Last, First

    Returns:
        [str]: First Last
    """
    firstlast = ' '.join(reversed(name.split(', ')))

    return firstlast
