from uscongress.tasks import update_bill_task
from django.views.generic import TemplateView

class UscongressDebugView(TemplateView):
    template_name = 'uscongress/debug.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = update_bill_task()
        return context
