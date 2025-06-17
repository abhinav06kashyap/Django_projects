from django.db import models

class credentials(models.Model):
    U_ID = models.TextField(max_length=8, unique=True, null=False)
    Email = models.TextField(max_length=50)
    Password = models.TextField(max_length=15)

class applications(models.Model):
    U_ID = models.TextField(max_length=8, unique=True, null=False)
    F_name = models.TextField(max_length=20)
    L_name = models.TextField(max_length=20)
    FandG_name = models.TextField(max_length=30)
    Gen = models.TextField(max_length=6)    
    Email = models.TextField(max_length=50)
    Ph = models.TextField(max_length=10)
    Course = models.TextField(max_length=6)
    B_date = models.TextField(max_length=10)
    