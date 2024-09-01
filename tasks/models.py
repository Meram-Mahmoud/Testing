from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=255)

    description = models.TextField(default='No description')  
    status = models.BooleanField(default=False)

    def _str_(self):
        return self.title
    