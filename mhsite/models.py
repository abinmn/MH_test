# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
class Application(models.Model):
    admission_number=models.CharField(max_length=7,
                                    validators=[RegexValidator(regex=r'^[0-9]{4}/[0-9]{2}$',message='The format for admission number is 1234/17')],
                                    help_text='9999/17',unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    address=models.CharField(max_length=500)
    pincode=models.CharField(max_length=6,validators=[RegexValidator(regex=r'^[0-9]{6}$',message='Enter a valid pincode')])
    phone=models.CharField(max_length=10,validators=[RegexValidator(regex=r'[0-9]{10}',message='Invalid mobile number')])
    date_of_birth=models.DateField()
    distance=models.IntegerField(default=0)
    keam=models.IntegerField(default=0)
    plus_2=models.DecimalField(default=00.00,max_digits=4,decimal_places=2)
    category=models.CharField(max_length=10)
    religion=models.CharField(max_length=50)
    caste=models.CharField(max_length=50)
