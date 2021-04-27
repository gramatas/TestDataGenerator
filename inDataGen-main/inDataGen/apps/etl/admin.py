"""ETL models admin."""

# Django
from django.contrib import admin

# Models
from apps.etl.models import *


admin.site.register(Project)
admin.site.register(Job)
admin.site.register(DataSource)
admin.site.register(JobRun)