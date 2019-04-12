
from django.db import models

class NewsCategroy(models.Model):
    name = models.CharField(max_length=100)

class Teachers(models.Model):
    name =models.CharField(max_length=100)
    desc = models.TextField()