from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.


class Meals(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=250)
    category = models.ForeignKey('Category' , on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='meals/')
    slug = models.SlugField(blank=True, null=True)

# override the save function for Meals model and say if there is a name without a slug then slugify name and add to slug
    def save(self, *args, **kwargs):
        if not self.slug and self.name :
            self.slug = slugify(self.name)
        super(Meals , self).save(*args , **kwargs)


    class Meta:
        verbose_name = 'meal'
        verbose_name_plural = 'meals'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    

