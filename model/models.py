from django.db import models
from django.utils import timezone
# Create your models here.

class ModelUsers(models.Model) :
    fullname = models.CharField(max_length=255 , default='')
    user_name = models.CharField(max_length=255 , unique=True,  name="user_name")
    user_auth = models.CharField(max_length=255 , name="user_auth")
    date  = models.DateTimeField("created_on" , default=timezone.now)