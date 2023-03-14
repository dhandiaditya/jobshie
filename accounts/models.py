from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    
    email = models.EmailField(blank=False, null=False)
    is_jobseeker = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    
    #last_name = models.CharField(max_length=100)

class Skill(models.Model):
    skill = models.CharField(max_length=50)

class Jobseeker(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    full_name = models.CharField(max_length=100, default="Name") 
    phone_number = models.CharField(max_length=20,null=True)
    location = models.CharField(max_length=20,null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, null=True)
    cover_photo = models.ImageField(upload_to='cover_photo/', null=True) 
    skills = models.ManyToManyField(Skill)















class Company(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    company_name = models.CharField(max_length=100, default="Name") 
    phone_number = models.CharField(max_length=20,null=True)
    designation = models.CharField(max_length=20,null=True)








