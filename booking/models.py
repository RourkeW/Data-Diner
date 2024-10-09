from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.


class Meals(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='meals/')
    slug = models.SlugField(blank=True, null=True)


    def __str__(self):
        return self.name

