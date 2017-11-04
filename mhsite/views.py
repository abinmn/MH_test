<<<<<<< HEAD
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from mhsite.forms import RegistrationForm,ApplicationForm
=======
from django.shortcuts import render, redirect
from mhsite.forms import RegistrationForm
from .forms import ApplicationForm
>>>>>>> 1604a83491d33b27fe1cf01e9d657fc921011652
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from mhsite.models import Application


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
<<<<<<< HEAD
            args={'form':form}
            return render(request,'mhsite/application.html',args)
=======
            print(form.errors)
            args = {'form': form, 'name': url_lock('reg')}
            return render(request, 'mhsite/application.html', args)
>>>>>>> 1604a83491d33b27fe1cf01e9d657fc921011652

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