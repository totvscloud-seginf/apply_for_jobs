import uuid

from django.db import models

# Create your models here.


class Password(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.CharField(max_length=50, null=True)
    expiration_date = models.DateField()
    maximum_views = models.IntegerField()
    views = models.IntegerField()


class Access(models.Model):
    password = models.ForeignKey('Password', on_delete=models.CASCADE)
    date = models.DateTimeField()
    ip = models.CharField(max_length=39)
