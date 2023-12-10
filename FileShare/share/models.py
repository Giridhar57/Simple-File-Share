from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Files(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    file = models.FileField(upload_to="media",null=False, blank=False)
    author_id=models.IntegerField()