from __future__ import unicode_literals
from django.shortcuts import render,redirect
from mhsite.forms import RegistrationForm
from .forms import ApplicationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return render(request, 'mhsite/index.html')


def loginf(request):
    form = AuthenticationForm
    args = {'form':form}
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user
                      )
                return redirect('/')
        else:
            args = {'form': form, 'error':True}
            return render(request,'mhsite/login.html',args)

    return render(request, 'mhsite/login.html', args)

def logoutf(request):
    logout(request)
    return render(request, 'mhsite/logout.html')


def application(request):
    form=ApplicationForm()
    args={'form':form}
    if request.method=='POST':
        form=ApplicationForm(request.POST)


        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print (form.errors)
            args={'form':form}
            return render(request,'mhsite/application.html',args)
    else:
        return render(request,'mhsite/application.html',args)

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print (form.errors)
            args={'form':form}
            return render(request,'mhsite/application.html',args)

    else:
        form = RegistrationForm()
        args = {'forms':form}
        return render(request, 'mhsite/registration.html', args)
