from __future__ import unicode_literals
from django.shortcuts import render,redirect
from mhsite.forms import RegistrationForm,ApplicationForm,ExpenseForm,ReportForm,MessCutForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from mhsite import middleware
from django.contrib.auth.forms import AuthenticationForm
from mhsite.models import Application,Expense,MessCut, Profile
from django.views import View
from django.views.generic.edit import FormView
from django.db import IntegrityError
from django.utils.dateformat import format
from datetime import date, timedelta, datetime
import json, os, calendar


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
            args = {'form': form, 'error': True}
            return render(request, 'mhsite/login.html', args)


    return render(request, 'mhsite/login.html', args)


def logoutf(request):
    args = {'name': url_lock('log')}
    logout(request)
    return render(request, 'mhsite/logout.html')


def students():
    pass


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
        user = request.user.username
        users = ''
        for x in students:
            if x[3] == user:
                users = x
        if users is not None:
            args = {'form': form, 'name': url_lock('application'), 'user': users}
            return render(request, 'mhsite/application.html', args)


# error for registration pending


def registration(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():
            if Profile.objects.filter(admission_number=form.cleaned_data.get('admission_number')).exists():
                if User.objects.filter(username=form.cleaned_data.get('email')).exists():
                    args = {'error':'User already exist'}
                    return render(request, 'mhsite/regerror.html', args)
                else:
                    form.save()
                    return redirect('/')

            else:
                args = {'error': 'You are not selected'}
                return render(request, 'mhsite/regerror.html', args)


    else:
        form = RegistrationForm()
        args = {'forms': form, 'name': url_lock('reg')}
        return render(request, 'mhsite/registration.html', args)


def url_lock(page):
    index = ['' for x in range(9)]
    pages = ['home', 'gallery', 'student', 'mess', 'contact', 'log', 'alloc', 'application', 'reg']
    if page in pages:
        i = pages.index(page)
        index[i] = 'active'
        return index
    return index

#mess cut data generation function (supprot function for mess_cut)
def date_gen(lst,start_date,end_date,objects=None):
    delta = end_date - start_date
    for i in range(delta.days+1):
        lst['processing'].append(str(start_date + timedelta(days=i)))


    seen = set()
    seen_add = seen.add
    lst['processing'] = [x for x in lst['processing'] if not (x in seen or seen_add(x))]

    return lst

#support function for mess_cut
def duplicate(date_list,date_type):
    duplicate_dates = []
    for date in date_list['processing']:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        year = str(date_obj.year)
        month = str(date_obj.month)
        if year in date_type:

            if  month in date_type[year]:

                if date in date_type[str(date_obj.year)][str(date_obj.month)]:
                    duplicate_dates.append(date)

                else:
                    continue

            else:
                continue

        else:
            continue
    return duplicate_dates

def mess_cut(request):
    if request.method=='POST':
        form=MessCutForm(request.POST)

        if form.is_valid():
            email= request.user.email
            start_date=form.cleaned_data['start_date']
            end_date=form.cleaned_data['end_date']
            try:

                obj = MessCut.objects.get(email=email)
                date_list = json.loads(obj.mess_cut_dates)

                date_list=(date_gen(date_list,start_date,end_date))

                approved_dates = json.loads(obj.approved_dates)
                rejected_dates = json.loads(obj.rejected_dates)

                duplicate_dates = duplicate(date_list,approved_dates) + duplicate(date_list,rejected_dates)
                date_list['processing'] = [date for date in date_list['processing'] if date not in duplicate_dates]

                date_list = (json.dumps(date_list))

                obj.mess_cut_dates=date_list
                obj.applied_date =  datetime.now().timestamp()

                obj.save()

                #return to new page
            except:

                date_list = (date_gen({'processing':[]},start_date,end_date))
                date_list = json.dumps(date_list)
                obj = MessCut(email=email, mess_cut_dates=date_list, applied_date =  datetime.now().timestamp())
                obj.save()


            return redirect('/')
        else:
            args={'form':form}
            return render(request,'mhsite/mess_cut.html',args)
    else:
        form = MessCutForm()
        args={'form':form}
        return render(request,'mhsite/mess_cut.html',args)

def processing(request, year=str(datetime.now().year), month=str(datetime.now().month) ):


    if request.method == 'POST':
        year = request.POST['year']
        month = str(datetime.strptime(request.POST['month'], '%B').month)


    rows = MessCut.objects.all().order_by('applied_date')
    res = []
    approved = []
    rejected = []
    for row in rows:
        profile = Profile.objects.get(email=row.email)
        name = profile.fname + " " + profile.lname
        mid = MessCut.objects.get(email=row.email).id
        room_number = profile.room_number #Complete after finishing profile
        approved_dates = json.loads(MessCut.objects.get(pk=mid).approved_dates)
        rejected_dates = json.loads(MessCut.objects.get(pk=mid).rejected_dates)


        data = json.loads(row.mess_cut_dates)
        timestamp = float(MessCut.objects.get(email=row.email).applied_date)
        applied_date = datetime.fromtimestamp(timestamp).strftime("%A, %d-%m-%Y")


        if year in approved_dates:
            if month in approved_dates[year]:
                approved.append([name, room_number,len(approved_dates[year][month]), mid])


        if year in rejected_dates:
            if month in rejected_dates[year]:
                rejected.append([name, room_number,len(rejected_dates[year][month]), mid])



    if len(data['processing']) > 0:
        res.append([name,room_number,applied_date,mid])

    years = [year for year in approved_dates]
    dupe = [year for year in rejected_dates if year not in years]
    if len(dupe)>0:
        for year in dupe:
            years.append(year)

    cal = {'months':list(calendar.month_name), 'years':years, 'default':[year, datetime.strftime(datetime(2017,int(month),1),'%B')]}
    args = {'data':res,'approved':approved, 'rejected':rejected, 'calendar':cal }
    return render(request,'mhsite/mess_cut_processing.html', args)

def approval(request,mess_id):
    mess = MessCut.objects.get(id=mess_id)
    mess_data = json.loads(mess.mess_cut_dates)
    dates = mess_data['processing']

    profile_data = Profile.objects.get(email=mess.email)
    profile = {'name':profile_data.fname + profile_data.lname, 'room_number':profile_data.room_number, 'mobile':profile_data.phone}

    args = {'dates':dates, 'profile':profile,}
    return render(request,'mhsite/verify.html', args)

#Final processing of mess data
def final(request, mess_id):
    mess = MessCut.objects.get(id=mess_id)
    mess_data = json.loads(mess.mess_cut_dates)
    dates = mess_data['processing']

    approved_dates = []
    rejected_dates = []
    for date in dates:
        try:

            choice = request.POST[date]
            if choice == '1':
                approved_dates.append(date)
            elif choice == '0':
                rejected_dates.append(date)
        except:
            pass

    mess_data['processing'] = [date for date in dates if (date not in approved_dates) and (date not in rejected_dates)]

    def date_data(x_date,dates):
        for date in dates:
            dateobject = datetime.strptime(date, '%Y-%m-%d')

            if str(dateobject.year) not in x_date:
                x_date[str(dateobject.year)] = {}

            if str(dateobject.month) not in x_date[str(dateobject.year)]:
                x_date[str(dateobject.year)][str(dateobject.month)] = []

            x_date[str(dateobject.year)][str(dateobject.month)].append(date)

        return x_date


    dic_approved_dates = (date_data(json.loads(mess.approved_dates),approved_dates))
    dic_rejected_dates = (date_data(json.loads(mess.rejected_dates),rejected_dates))


    mess.mess_cut_dates = json.dumps(mess_data)
    mess.approved_dates = json.dumps(dic_approved_dates)
    mess.rejected_dates = json.dumps(dic_rejected_dates)
    mess.process_date = datetime.now().timestamp()

    mess.save()

    #print ('approved', approved_dates, 'rejected', rejected_dates)
    return redirect('/')

def edit(request,type, mess_id, year = datetime.now().year, month = datetime.now().month ) :

    if month.isalpha():
        month = datetime.strptime(month,"%B").month

    approved_dates = json.loads(MessCut.objects.get(id= mess_id).approved_dates)
    rejected_dates = json.loads(MessCut.objects.get(id= mess_id).rejected_dates)

    if type == 'approved':
        dates = approved_dates[str(year)][str(month)]
    elif type == 'rejected':
        dates = rejected_dates[str(year)][str(month)]

    args = {'dates':dates, 'type':type, 'mess_id':mess_id}
    return render(request, 'mhsite/edit.html', args)

def submit_edit(request, type, mess_id, year = datetime.now().year, month = datetime.now().month ):
    mess = MessCut.objects.get(id= mess_id)
    if month.isalpha():
        month = datetime.strptime(month,"%B").month
    approved_dates = json.loads(mess.approved_dates)
    rejected_dates = json.loads(mess.rejected_dates)

    if type == 'approved':
        dates = {date:request.POST[date] for date in approved_dates[str(year)][str(month)] if date in request.POST}
        for date in dates:
            if dates[date] == '0':
                approved_dates[str(year)][str(month)].remove(date)

                if year in rejected_dates:
                    if month in rejected_dates[year]:
                        rejected_dates[str(year)][str(month)].append(date)
                    else:
                        rejected_dates[str(year)][str(month)] = []
                        rejected_dates[str(year)][str(month)].append(date)
                else:
                    rejected_dates[str(year)] = {}
                    rejected_dates[str(year)][str(month)] = []
                    rejected_dates[str(year)][str(month)].append(date)

    if type == 'rejected':
        dates = {date:request.POST[date] for date in rejected_dates[str(year)][str(month)] if date in request.POST}
        for date in dates:
            if dates[date] == '1':
                rejected_dates[str(year)][str(month)].remove(date)

                if year in approved_dates:
                    if month in approved_dates[year]:
                        approved_dates[str(year)][str(month)].append(date)
                    else:
                        approved_dates[year][str(month)] = []
                        approved_dates[str(year)][str(month)].append(date)
                else:
                    approved_dates[year] = {}
                    approved_dates[year][str(month)] = []
                    approved_dates[str(year)][str(month)].append(date)

    mess.approved_dates = json.dumps(approved_dates)
    mess.rejected_dates = json.dumps(rejected_dates)
    mess.process_date = datetime.now().timestamp()
    mess.save()

    return redirect('/secretary/processing')

def expense(request,year,month,day):
    date=(year+'-'+month+'-'+day)
    if request.method=='POST':
        try:
            expense = Expense.objects.get(date=date)
            form = ExpenseForm(request.POST, instance=expense)

        except Expense.DoesNotExist:
            form = ExpenseForm(request.POST)

        if form.is_valid():

            try:
                form.save()
                return redirect('/report'+'/'+date)

            except IntegrityError as e:

                return render(request, 'mhsite/expense_tracker.html', args)
        else:
            args = {'form': form}
            return render(request, 'mhsite/expense_tracker.html', args)

#edit/create expense
    else:
        #edit expense for a month
        try:
            expense = Expense.objects.get(date=date)
            form = ExpenseForm(instance=expense)
            args = {'form': form}
            return render(request, 'mhsite/expense_tracker.html', args)
        #create expense for a month
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
