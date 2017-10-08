from __future__ import unicode_literals
from django.shortcuts import render,redirect
from mhsite.forms import RegistrationForm



def home(request):
    return render(request, 'mhsite/index.html')

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




