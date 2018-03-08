from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.name
# Create your models here.
