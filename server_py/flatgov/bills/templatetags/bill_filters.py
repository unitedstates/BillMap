from django import template
from django.template.defaultfilters import stringfilter
from common import constants
from typing import Union
import re
from datetime import datetime


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
def billtitle_display(title: Union[str, None]):
    if not title:
        return title
    # Uncomment this line to show the bill stage
    #return re.sub(r'(:?.*\s([^ ]*):\s*)?(.*)$', r'\3 (\2)', title ).replace(' ()','')
    return re.sub(r'(:?.*\s([^ ]*):\s*)?(.*)$', r'\3', title ).replace(' ()','')

@register.filter
@stringfilter
def billnumber_display(billnumber: Union[str, None]):
    if not billnumber:
        return billnumber

    billMatch = constants.BILL_NUMBER_REGEX_COMPILED.match(billnumber) 
    if billMatch and billMatch.groupdict():
        billMatchGroups = billMatch.groupdict()
        congress = numstring_to_ordinal(billMatchGroups.get('congress', ''))
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
def billnumbers_by_congress(billnumbers: list, congress: str):
    return  list([billnumber for billnumber in list(billnumbers) if str(congress) in billnumber.split('(')[-1]])

@register.filter
def billnumbers_display(billnumbers: list, withorig=False):
    if not billnumbers:
        return []
    if isinstance(billnumbers, str):
        billnumbers = billnumbers.split(', ')
    if withorig:
        return [(billnumber, billnumber_display(billnumber)) for billnumber in list(billnumbers) ]
    return [billnumber_display(billnumber) for billnumber in list(billnumbers) ]

@register.filter
@stringfilter
def add_number_of_sections(reason: str, number_of_sections: int) -> str:
    if not number_of_sections:
        return reason
    
    return reason.replace('section similarity', 'section similarity ({})'.format(number_of_sections))

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

@register.filter
@stringfilter
def congress_to_year(congress: str) -> int:
    if not congress:
        return 0 

    try:
        congress_num = int(congress)
    except ValueError:
        return 0

    if congress_num and congress_num != 0:
        return 1787 + int(congress_num)*2
    else:
        return 0

@register.filter
@stringfilter
def numstring_to_ordinal(numstring: str) -> str:
    """
    See https://stackoverflow.com/a/50992575/628748
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'

    Args:
        numstring (str): string to add ordinal to (usu used for congress number) 

    Returns:
        str: ordinal expression, e.g. 117th 
    """

    if not numstring:
        return ''

    try:
        n = int(numstring)
    except ValueError as err:
        return numstring 

    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


@register.filter
def normalize_score(score: float, total: float) -> int:
    if not total:
        total = 100
    if not score:
        return 0
    else:
        return round(score/total * 100)


@register.filter
def custom_date(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d')
    except:
        pass
    return date
