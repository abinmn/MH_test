from django.shortcuts import render, redirect
from mhsite.forms import RegistrationForm
from .forms import ApplicationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


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
            form.save()
            return redirect('/')
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