from django import template
from django.template.defaultfilters import stringfilter
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
def billnumbers_by_congress(billnumbers: list, current_bill: str):
   return  [billnumber for billnumber in list(billnumbers) if str(current_bill) in billnumber.split('(')[-1]]

@register.filter
def billnumbers_display(billnumbers: list):
    if isinstance(billnumbers, str):
        billnumbers = billnumbers.split(', ')
    return [billnumber_display(billnumber) for billnumber in list(billnumbers) ]

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
