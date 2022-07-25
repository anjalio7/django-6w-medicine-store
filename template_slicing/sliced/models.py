from tkinter import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

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
    MfgDate=models.DateTimeField()
    Expirydate=models.DateTimeField()
    Description=models.CharField(max_length=500)
    ManufacturedBy=models.CharField(max_length=500)

class Order(models.Model):
    User_id=models.ForeignKey(user,on_delete=models.CASCADE, related_name='User_id')
    Medicine_id=models.ForeignKey(Medicine,on_delete=models.CASCADE, related_name='Medicine_id')
    Booking_date=models.DateTimeField()
    Quantity=models.IntegerField()
    Status=models.CharField(max_length=100, default="pending")
    Address=models.CharField(max_length=500)
    Total_price=models.IntegerField()



    
