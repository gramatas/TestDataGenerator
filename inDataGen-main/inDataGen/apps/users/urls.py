# Django
from django.urls import include, path

# Views
from apps.users.views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
]
