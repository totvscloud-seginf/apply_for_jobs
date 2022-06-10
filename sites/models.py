from django.db import models
import uuid

# Create your models here.
class Password(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    password = models.CharField(max_length=30, null=True)
    expiration_date   = models.DateField()
    max_views = models.IntegerField()
    views = models.IntegerField()

    def __str__(self) -> str:
       return str(self.id)