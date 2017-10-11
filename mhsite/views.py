from __future__ import unicode_literals
from django.shortcuts import render,redirect
from mhsite.forms import RegistrationForm
from .forms import ApplicationForm


def home(request):
    return render(request, 'mhsite/index.html')

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
        form = RegistrationForm()
        args = {'forms':form}
        return render(request, 'mhsite/registration.html', args)
