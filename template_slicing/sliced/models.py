from tkinter import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import datetime

# Create your models here.
class user(AbstractUser):
    pass

class Diseases(models.Model):
    name=models.CharField(max_length=100)

class Medicine(models.Model):
    Disease_id=models.ForeignKey(Diseases, on_delete= models.CASCADE, related_name='Disease_id')
    Name=models.CharField(max_length=500)
    Image=models.ImageField(upload_to='image')
    Price=models.IntegerField()
    MfgDate=models.CharField(max_length = 20)
    Expirydate=models.CharField(max_length = 20)
    Description=models.CharField(max_length=500)
    ManufacturedBy=models.CharField(max_length=500)
    stock = models.IntegerField(default='1')

class Order(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, related_name='userId')
    orderDate = models.DateField(default=datetime.date.today())
    totalCost = models.IntegerField()
    address = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=20, default='pending')
    medicineId = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name= 'medicineId')
    quantity = models.IntegerField(default = 1)

    

    
