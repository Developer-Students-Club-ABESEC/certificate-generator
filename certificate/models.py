from django.db import models
import jsonfield

# Create your models here.
class csvdata(models.Model):
    key = models.CharField(null=False,unique=True, max_length=50)
    details=jsonfield.JSONField()

class saveimage(models.Model):
    key = models.CharField(null=False,unique=True, max_length=50)
    photo= models.ImageField(upload_to='images', max_length=255, default='images/default.png')

class fonts(models.Model):
    name = models.CharField(max_length=1000, unique=True, null=False)
    path = models.CharField(max_length=10000,unique=True, null=False)