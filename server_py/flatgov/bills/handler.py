# from bills.models import Bill, Sponsor, Cosponsor


class BillDataHandler(object):
    def __init__(self, *args, **kwargs):
        self.data = kwargs.get('data')
        self.congress = kwargs.get('congress_type_num')
        self.bill = self.get_bill()
        self.cosponsors = self.get_cosponsors(bill=self.bill)

    def get_bill(self, *args, **kwargs):
        related = self.data.get('related')
        target = related.get(self.congress)

        if not target:
            sponsor = dict()
            cosponsors_dict = dict()
        else:
            sponsor = target.get('sponsor')
            cosponsors_dict = target.get('cosponsors')

            if not sponsor:
                sponsor = dict()

            if not cosponsors_dict:
                cosponsors_dict = dict()
        
        bill_data = {
            'titles': self.data.get('titles'),
            'titles_whole_bill': self.data.get('titles_whole_bill'),
            'related_bills': self.data.get('related_bills'),
            'sponsor': sponsor,
            'cosponsors_dict': cosponsors_dict,
        }
        # bill = Bill.objects.get_or_create(
        #     bill_congress_type_number=self.congress,
        #     default=bill_data
        # )
        return bill_data

    def get_cosponsors(self, *args, **kwargs):
        bill = kwargs.get('bill')
        cosponsors = self.data.get('cosponsors')
        return cosponsors
