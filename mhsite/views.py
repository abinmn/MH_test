from __future__ import unicode_literals
from django.shortcuts import render, redirect
from mhsite.forms import RegistrationForm, ApplicationForm, ExpenseForm, ReportForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from mhsite.models import Application, Expense
from django.views import View
from django.views.generic.edit import FormView
from django.db import IntegrityError
from django.utils.dateformat import format
import os
from .models import Profile
from django.contrib.auth.models import User
from mhsite import middleware


def home(request):
    args = {'name': url_lock('home')}
    return render(request, 'mhsite/index.html', args)


def gallery(request):
    args = {'name': url_lock('gallery')}
    return render(request, 'mhsite/gallery.html', args)


def mess(request):
    args = {'name': url_lock('mess')}
    return render(request, 'mhsite/messlogout.html', args)


def studentlist():
    pwd = os.path.dirname(__file__)
    file = open(pwd + '/students.csv')
    data = file.readlines()
    file.close()
    students = []
    for row in data:
        a = row.split(',')
        a[3] = a[3].replace('\n', '')
        students.append(a)
    students.pop(0)
    return students


def allocation(request):
    if request.method == 'POST':
        students = studentlist()
        Profile.objects.filter().delete()
        for x in students:
            p = Profile(admission_number=x[0], fname=x[1], lname=x[2], email=x[3])
            p.save()

        return redirect('/')

    else:
        students = studentlist()
        args = {'name': url_lock('alloc'), 'data': students}
        return render(request, 'mhsite/allocation.html', args)


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
            args = {'name': url_lock('home'), 'error': 'Login Failed', 'erlink':'/login'}
            return render(request, 'mhsite/regerror.html', args)

    return render(request, 'mhsite/login.html', args)


def pwdreset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form, 'name': url_lock('log')}
        return render(request, 'mhsite/passwordreset.html', args)


def logoutf(request):
    args = {'name': url_lock('log')}
    logout(request)
    return render(request, 'mhsite/logout.html')


def students(request):
    try:
        details = Application.objects.get(e_mail=request.user.username)
    except:
        details =''
    args = {'data':details}
    return render(request, 'mhsite/studentscorner.html', args)


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
        students = studentlist()
        usern = request.user.username
        users = ''
        for x in students:
            if x[3] == usern:
                users = x
        if users is not None:
            args = {'form': form, 'name': url_lock('application'), 'usern': users}
            return render(request, 'mhsite/application.html', args)


# error for registration pending


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if Profile.objects.filter(admission_number=form.cleaned_data.get('admission_number')).exists():
                if User.objects.filter(username=form.cleaned_data.get('email')).exists():
                    args = {'name': url_lock('home'), 'error':'User already exist', 'erlink':'/register'}
                    return render(request, 'mhsite/regerror.html', args)
                else:
                    form.save()
                    return redirect('/')

            else:
                args = {'name': url_lock('home'), 'error': 'You are not selected', 'erlink':'/register'}
                return render(request, 'mhsite/regerror.html', args)
        else:
            args = {'forms': form}
            return render(request, 'mhsite/registration.html', args)

    else:
        form = RegistrationForm()
        args = {'forms':form}
        return render(request, 'mhsite/registration.html', args)


def url_lock(page):
    index = ['' for x in range(9)]
    pages = ['home', 'gallery', 'student', 'mess', 'contact', 'log', 'alloc', 'application', 'reg']
    if page in pages:
        i = pages.index(page)
        index[i] = 'active'
        return index
    return index


def expense(request, year, month, day):
    date = (year + '-' + month + '-' + day)

    if request.method == 'POST':
        try:
            expense = Expense.objects.get(date=date)
            form = ExpenseForm(request.POST, instance=expense)

        except Expense.DoesNotExist:
            form = ExpenseForm(request.POST)

        if form.is_valid():

            try:
                form.save()
                return redirect('report' + '/' + date)

            except IntegrityError as e:

                return render(request, 'mhsite/expense_tracker.html', args)
        else:
            args = {'form': form}
            return render(request, 'mhsite/expense_tracker.html', args)


    else:
        try:
            expense = Expense.objects.get(date=date)
            form = ExpenseForm(instance=expense)
            args = {'form': form}
            return render(request, 'mhsite/expense_tracker.html', args)

        except Expense.DoesNotExist:
            form = ExpenseForm(initial={'date': date})
            args = {'form': form}
            return render(request, 'mhsite/expense_tracker.html', args)


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
        date = (year + '-' + month + '-' + day)
        try:
            expense = Expense.objects.get(date=date)
            return render(request, 'mhsite/report_details.html', {'data': expense, 'link': date})

        except Expense.DoesNotExist:
            return redirect('expense', year, month, day)
