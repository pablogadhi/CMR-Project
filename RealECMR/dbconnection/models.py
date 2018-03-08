from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)

# Create your models here.
