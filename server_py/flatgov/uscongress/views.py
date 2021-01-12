from uscongress.tasks import update_bill_task
from django.views.generic import TemplateView

class UscongressTestView(TemplateView):
    template_name = 'uscongress/debug.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(args, kwargs)
        update = update_bill_task()
        return context
