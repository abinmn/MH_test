# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from  .models import Application, Expense, MessCut, Profile
# Register your models here.
admin.site.register(Application)
admin.site.register(Expense)
admin.site.register(MessCut)
admin.site.register(Profile)
