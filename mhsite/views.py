from __future__ import unicode_literals
from django.shortcuts import render,redirect
from mhsite.forms import RegistrationForm,ApplicationForm,ExpenseForm,ReportForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from mhsite.models import Application,Expense
from django.views import View
from django.views.generic.edit import FormView
from django.db import IntegrityError
from django.utils.dateformat import format
import datetime


def home(request):
    args = {'name': url_lock('home')}
    return render(request, 'mhsite/index.html', args)

def gallery(request):
    args = {'name': url_lock('gallery')}
    return render(request, 'mhsite/gallery.html', args)

def mess(request):
    args = {'name': url_lock('mess')}
    return render(request, 'mhsite/messlogout.html', args)


def allocation(request):
    args = {'name': url_lock('alloc')}
    return render(request, 'mhsite/allocation.html')


def loginf(request):
    form = AuthenticationForm
    args = {'form': form, 'name': url_lock('log')}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
        else:
            args = {'form': form, 'error': True}
            return render(request, 'mhsite/login.html', args)

    return render(request, 'mhsite/login.html', args)


def logoutf(request):
    args = {'name': url_lock('log')}
    logout(request)
    return render(request, 'mhsite/logout.html')


def application(request):
    form = ApplicationForm()
    args = {'form': form, 'name': url_lock('application')}
    if request.method == 'POST':
        form = ApplicationForm(request.POST)


        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print(form.errors)
            args = {'form': form, 'name': url_lock('application')}
            return render(request, 'mhsite/application.html', args)
    else:
        return render(request, 'mhsite/application.html', args)


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            admission_number = (form.cleaned_data['admission_number'])
            if Application.objects.get(admission_number=admission_number).status:
                form.save()
                return redirect('/')
            else:
                print ("Application not approved yet")
                return render(request,'mhsite/application_status.html')

        else:
            print(form.errors)
            args = {'form': form, 'name': url_lock('reg')}
            return render(request, 'mhsite/application.html', args)

    else:
        form = RegistrationForm()
        args = {'forms': form, 'name': url_lock('reg')}
        return render(request, 'mhsite/registration.html', args)

def url_lock(page):
    index = [''  for x in range(9)]
    pages = ['home','gallery','student','mess','contact','log', 'alloc', 'application','reg']
    if page in pages:
        i = pages.index(page)
        index[i] = 'active'
        return index
    return index

def expense(request,year,month,day):

    if request.method=='POST':
        form=ExpenseForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except IntegrityError as e:

                if 'UNIQUE constraint' in e.message:
                    args={'update':True}
                    return render(request, 'mhsite/expense_tracker.html', args)
                return render(request, 'mhsite/expense_tracker.html', args)
        else:
            args={'form':form}
            return render(request, 'mhsite/expense_tracker.html', args)


    else:
        try:
            date=(year+'-'+month+'-'+day)
            expense=Expense.objects.get(date=date)
            data={'item5':expense.item5}
            form=ExpenseForm(initial=data)
            args = {'form': form}
            return render(request, 'mhsite/expense_tracker.html', args)
        except Expense.DoesNotExist:
            form=ExpenseForm()
            args = {'form': form}
            return render(request, 'mhsite/expense_tracker.html',args)


class Report(FormView):
    template_name = 'mhsite/report.html'
    form_class = ReportForm

    def form_valid(self, form):
        date = form.cleaned_data.get('date')
        year = date.year
        month = format(date, 'm')
        day = '01'
        return redirect('report_details', year, month, day)

class ReportDetails(View):
    def get(self, request, year, month, day):
        date=(year+'-'+month+'-'+day)
        expense=Expense.objects.get(date=date)
        return render(request, 'mhsite/report_details.html', {'data': expense,'link':date})
