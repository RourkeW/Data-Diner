from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BookTable(models.Model):
    table_number = models.IntegerField(unique=true)
    capacity = models.IntegerField()
