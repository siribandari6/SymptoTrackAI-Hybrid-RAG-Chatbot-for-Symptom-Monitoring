from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=80)
    
    class Meta:
        db_table = 'register'

class Log(models.Model):
    username = models.CharField(max_length=50)
    symptoms_text = models.CharField(max_length=400)
    predicted_advice = models.CharField(max_length=60)
    checked_date = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'log'
