"""Main URLs module."""

# Django
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include(('apps.users.urls', 'users'), namespace='users')),
    path('', include(('apps.etl.urls', 'etl'), namespace='etl')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
