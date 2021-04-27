# Django
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt

# Tasks
from apps.etl.tasks import run_graph

# Models
from apps.etl.models import *
from apps.users.models import User

# Utilities
import json


@csrf_exempt
def test_etl_view(request):

    body = json.loads(request.body)
    run_graph(**body)

    return HttpResponse(f"Ok. Check for json file test.csv")


class Home(TemplateView):

    template_name = 'base/projects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.request.user.projects.all()
        return context
