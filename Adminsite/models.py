from django.db import models

# Create your models here.
class Admin_RegDB(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 