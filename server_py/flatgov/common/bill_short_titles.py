from typing import List
from bills.models import Bill


def getBillShortTitles(congressnum: str='117') -> List[str]:
    """
    Generate list of strings with billnumber + # + short title
    E.g. '116hjres58#Constitutional Authorities Resolution'

    Args:
        congress (str, optional): [description]. Defaults to '117'.

    Returns:
        List[str]: [description]
    """

    return [item.bill_congress_type_number + '#' + item.short_title for item in Bill.objects.filter(congress=congressnum)];