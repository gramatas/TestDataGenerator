# Django
from django.urls import path

# Views
from apps.etl.views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('test-etl/', test_etl_view, name='test_etl'),
]