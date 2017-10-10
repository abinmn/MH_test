# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Application(models.Model):
    admission_number=models.CharField(max_length=7,validators=[RegexValidator(r'^[0-9]{4}/[0-9]{2}$')])
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=500)
    pincode=models.CharField(max_length=6,validators=[RegexValidator(r'^[0-9]{6}$')])
    phone=models.CharField(max_length=10,validators=[RegexValidator(r'[0-9]{10}')])
    dob=models.DateField(verbose_name='Date of Birth')
    distance=models.IntegerField(default=0)
    keam=models.IntegerField(default=0)
    plus2=models.DecimalField(default=00.00,max_digits=4,decimal_places=2)
    category=models.CharField(max_length=10)
    religion=models.CharField(max_length=50)
    caste=models.CharField(max_length=50)
