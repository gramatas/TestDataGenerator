""" ETL models."""

# Django
from django.db import models

# Utilities
from apps.utils.models import BaseModel

# Models
from apps.users.models import User


SOURCE_TYPES = [('postgres', 'PostgresQL'), ('api', 'Rest API')]
STATUS_CHOICES = [('created', 'Created'), ('running', 'In progress'), ('completed', 'Completed'), ('error', 'Error')]


class Project(BaseModel):

    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name


class DataSource(BaseModel):

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=SOURCE_TYPES)
    config = models.JSONField()

    def __str__(self):
        return self.name


class Job(BaseModel):

    name = models.CharField(max_length=50)
    logical_position = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='jobs')
    source = models.OneToOneField(DataSource, on_delete=models.CASCADE, related_name='source_job')
    destination = models.OneToOneField(DataSource, on_delete=models.CASCADE, related_name='destination_job')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class JobRun(BaseModel):

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    log_path = models.CharField(max_length=300)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='runs')
