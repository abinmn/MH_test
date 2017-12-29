from __future__ import unicode_literals
from django.shortcuts import render, redirect
from mhsite.forms import RegistrationForm, ApplicationForm, ExpenseForm, ReportForm, MessCutForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from mhsite.models import Application, Expense, MessCut, Profile
from django.views import View
from django.views.generic.edit import FormView
from django.db import IntegrityError
from django.utils.dateformat import format
from datetime import date, timedelta, datetime
import json, os, calendar
from django.http import HttpResponse

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


def home(request):
    return render(request, 'mhsite/index.html')


def gallery(request):
    return render(request, 'mhsite/gallery.html')


def mess(request):
    if request.user.is_authenticated:
        return redirect('/mess_cut')
    else:
        return render(request, 'mhsite/messlogout.html')


def allocation(request):
    if request.user.is_authenticated and (request.user.username == 'admin' or request.user.username == 'secretary'):
        if request.method == 'POST':
            students = studentlist()
            Profile.objects.filter().delete()
            for x in students:
                p = Profile(admission_number=x[0], fname=x[1], lname=x[2], email=x[3])
                p.save()

            return redirect('/')

        else:
            students = studentlist()
            args = {'data': students}
            return render(request, 'mhsite/admin/allocation.html', args)
    else:
        return redirect('/')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if Profile.objects.filter(admission_number=form.cleaned_data.get('admission_number')).exists():
                if User.objects.filter(username=form.cleaned_data.get('email')).exists():
                    args = {'error': 'User already exist', 'erlink': '/register'}
                    return render(request, 'mhsite/regerror.html', args)
                else:
                    form.save()
                    return redirect('/accounts/login')

            else:
                args = {'error': 'You are not selected', 'erlink': '/register'}
                return render(request, 'mhsite/regerror.html', args)
        else:
            args = {'forms': form}
            return render(request, 'mhsite/accounts/registration.html', args)

    else:
        form = RegistrationForm()
        args = {'forms': form}
        return render(request, 'mhsite/accounts/registration.html', args)


def loginf(request):
    form = AuthenticationForm
    args = {'form': form}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
        else:
            args = {'error': 'Login Failed', 'erlink': '/accounts/login'}
            return render(request, 'mhsite/regerror.html', args)


    return render(request, 'mhsite/accounts/login.html', args)

def logoutf(request):
    logout(request)
    return render(request, 'mhsite/accounts/logout.html')


def pwdreset(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(data=request.POST, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('/accounts/login')
            else:
                print(form.errors)
                args = {'error': 'Password reset failed', 'erlink': '/accounts/pwdreset'}
                return render(request, 'mhsite/regerror.html', args)

        else:
            form = PasswordChangeForm(user=request.user)
            args = {'form': form}
            return render(request, 'mhsite/accounts/passwordreset.html', args)
    else:
        return redirect('/')


def application(request):
    if request.user.is_authenticated:
        form = ApplicationForm()
        args = {'form': form}
        if request.method == 'POST':
            form = ApplicationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/students/studentscorner')
            else:
                print(form.errors)
                args = {'form': form}
                return render(request, 'mhsite/students/application.html', args)
        else:
            students = studentlist()
            usern = request.user.username
            users = ''
            for x in students:
                if x[3] == usern:
                    users = x

            try:
                app = Application.objects.get(email=request.user.email)
                print (app.room_number)
                personal = {'room_number':app.room_number, 'address':app.address, 'pincode':app.pincode, 'phone':app.phone, 'dob':app.date_of_birth, 'category':app.category, 'religion':app.religion, 'caste':app.caste }
            except:
                pass
                #personal ={'room_number':'', 'address':'' 'pincode':'', 'phone':'', 'dob':'', 'category':'', 'religion':'', 'caste':''}
            if users is not None:
                args = {'form': form, 'usern': users, 'data':personal}
                return render(request, 'mhsite/students/application.html', args)
    else:
        return redirect('/')


def contacts(request):
    return render(request, 'mhsite/contacts.html')


def students(request):
    if request.user.is_authenticated:
        print(request.user.username)
        if Application.objects.filter(email=request.user.username).exists:
            details = Application.objects.get(email=request.user.username)
            args = {'data': details}
            return render(request, 'mhsite/students/studentscorner.html', args)

        else:
            return redirect('/students/application')
    else:
        return redirect('/')


def mess_cut(request, year=str(datetime.now().year), month=str(datetime.now().month)):
    try:
        email = request.user.email
        mess = MessCut.objects.get(email=email)
        if request.method == 'POST':
            year = str(request.POST['year'])
            month = str(datetime.strptime(request.POST['month'], '%B').month)

        approved_dates = json.loads(mess.approved_dates)
        rejected_dates = json.loads(mess.rejected_dates)

        if year in approved_dates:
            if month in approved_dates[year]:
                approved_dates = approved_dates[year][month]

        if year in rejected_dates:
            if month in rejected_dates[year]:
                rejected_dates = rejected_dates[year][month]

        processing_dates = json.loads(mess.mess_cut_dates)['processing']

        years = [year for year in json.loads(mess.approved_dates)]
        dupe = [year for year in json.loads(mess.rejected_dates) if year not in years]
        if len(dupe)>0:
            for year in dupe:
                years.append(year)

        if len(years) == 0:
            years = [year]
        cal = {'months': list(calendar.month_name), 'years': years,
              'default':[year, datetime.strftime(datetime(2017,int(month),1),'%B')]}
        args = {'calendar': cal, 'processing': processing_dates, 'approved': approved_dates, 'rejected': rejected_dates, 'dtype': [isinstance(approved_dates, dict), isinstance(rejected_dates, dict)]}

        return render(request, 'mhsite/mess/mess_user.html', args)

    except AttributeError :
        return redirect('/accounts/login')

    except:
        print ("hello")
        if request.method == 'POST':
            error = True
            month = request.POST['month']
        else:
            error = False
            month = datetime.strftime(datetime(2017, int(month), 1), '%B')

        cal = {'months':list(calendar.month_name), 'years':[year], 'default':[year, month]}
        args = {'calendar': cal, 'status':error}
        return render(request, 'mhsite/mess/mess_user.html', args)


def date_gen(lst, start_date, end_date, objects=None):
    delta = end_date - start_date
    for i in range(delta.days + 1):
        lst['processing'].append(str(start_date + timedelta(days=i)))
    seen = set()
    seen_add = seen.add
    lst['processing'] = [x for x in lst['processing'] if not (x in seen or seen_add(x))]

    return lst


def duplicate(date_list, date_type):
    duplicate_dates = []
    for date in date_list['processing']:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        year = str(date_obj.year)
        month = str(date_obj.month)
        if year in date_type:

            if month in date_type[year]:

                if date in date_type[str(date_obj.year)][str(date_obj.month)]:
                    duplicate_dates.append(date)

                else:
                    continue

            else:
                continue

        else:
            continue
    return duplicate_dates


def mess_cut_apply(request):
    if request.method == 'POST':
        form = MessCutForm(request.POST)

        if form.is_valid():
            email = request.user.email
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            try:

                obj = MessCut.objects.get(email=email)
                date_list = json.loads(obj.mess_cut_dates)

                date_list = (date_gen(date_list, start_date, end_date))

                #if len(date_list) < 3:

                    #return render(request, 'mhsite/mess_cut.html')

                approved_dates = json.loads(obj.approved_dates)
                rejected_dates = json.loads(obj.rejected_dates)

                duplicate_dates = duplicate(date_list, approved_dates) + duplicate(date_list, rejected_dates)
                date_list['processing'] = [date for date in date_list['processing'] if date not in duplicate_dates]

                date_list = (json.dumps(date_list))

                obj.mess_cut_dates = date_list
                obj.applied_date = datetime.now().timestamp()

                obj.save()

                # return to new page
            except:

                date_list = (date_gen({'processing': []}, start_date, end_date))
                date_list = json.dumps(date_list)
                obj = MessCut(email=email, mess_cut_dates=date_list, applied_date=datetime.now().timestamp())
                obj.save()

            return redirect('/')
        else:
            args = {'form': form}
            return render(request, 'mhsite/mess_cut.html', args)
    else:
        form = MessCutForm()
        args = {'form': form}
        return render(request, 'mhsite/mess/mess_cut.html', args)


def processing(request, year=str(datetime.now().year), month=str(datetime.now().month)):
    if request.user.is_authenticated and (request.user.username == 'mess'):
        if request.method == 'POST':
            year = request.POST['year']
            month = str(datetime.strptime(request.POST['month'], '%B').month)

        rows = MessCut.objects.all().order_by('applied_date')
        res = []
        approved = []
        rejected = []
        for row in rows:
            profile = Application.objects.get(email=row.email)
            name = profile.first_name + " " + profile.last_name
            mid = MessCut.objects.get(email=row.email).id
            room_number = profile.room_number  # Complete after finishing profile
            approved_dates = json.loads(MessCut.objects.get(pk=mid).approved_dates)
            rejected_dates = json.loads(MessCut.objects.get(pk=mid).rejected_dates)

            data = json.loads(row.mess_cut_dates)
            timestamp = float(MessCut.objects.get(email=row.email).applied_date)
            applied_date = datetime.fromtimestamp(timestamp).strftime("%A, %d-%m-%Y")

            if year in approved_dates:
                if month in approved_dates[year]:
                    approved.append([name, room_number, len(approved_dates[year][month]), mid])

            if year in rejected_dates:
                if month in rejected_dates[year]:
                    rejected.append([name, room_number, len(rejected_dates[year][month]), mid])

            if len(data['processing']) > 0:
                res.append([name, room_number, applied_date, mid])


        if request.POST.get('download'):
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            from io import StringIO, BytesIO
            buff = BytesIO()

            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak, Table, TableStyle

            styles = getSampleStyleSheet()
            styleNormal = styles['Normal']
            styleHeading = styles['Heading2']
            styleHeading.alignment = 0

            story = []
            story.append(Paragraph('Report for '+request.POST['month'] + ", " +year, styleHeading))

            for i in approved:
                i.pop()
            approved.insert(0, ['Name', 'Room Number', 'Days'])
            tableData = approved
            ts = [
        ('LINEABOVE', (0,0), (-1,0), 1, colors.gray),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.gray)]
            story.append(Table(tableData, hAlign = 'LEFT', style=ts))

            doc = SimpleDocTemplate(buff, title = "Mess Cut Report %s, %s"%(request.POST['month'], year), author = "mess committee")
            doc.build(story)
            response.write(buff.getvalue())
            buff.close()
            return response


        years = [year for year in approved_dates]
        dupe = [year for year in rejected_dates if year not in years]
        if len(dupe) > 0:
            for year in dupe:
                years.append(year)

        if len(years) == 0:
            years = [year]

        cal = {'months': list(calendar.month_name), 'years': years,
               'default': [year, datetime.strftime(datetime(2017, int(month), 1), '%B')]}
        args = {'data': res, 'approved': approved, 'rejected': rejected, 'calendar': cal}
        print (approved)
        return render(request, 'mhsite/mess/mess_cut_processing.html', args)

    else:
        return redirect('/')


def approval(request, mess_id):
    if request.user.is_authenticated and (request.user.username == 'mess'):
        mess = MessCut.objects.get(id=mess_id)
        mess_data = json.loads(mess.mess_cut_dates)
        dates = mess_data['processing']

        profile_data = Application.objects.get(email=mess.email)
        profile = {'name': profile_data.first_name + profile_data.last_name, 'room_number': profile_data.room_number,
                   'mobile': profile_data.phone}

        args = {'dates': dates, 'profile': profile, }
        return render(request, 'mhsite/mess/verify.html', args)

    else:
        return redirect('/')

# Final processing of mess data
def final(request, mess_id):
    if request.user.is_authenticated and (request.user.username == 'mess'):
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

        def date_data(x_date, dates):
            for date in dates:
                dateobject = datetime.strptime(date, '%Y-%m-%d')

                if str(dateobject.year) not in x_date:
                    x_date[str(dateobject.year)] = {}

                if str(dateobject.month) not in x_date[str(dateobject.year)]:
                    x_date[str(dateobject.year)][str(dateobject.month)] = []

                x_date[str(dateobject.year)][str(dateobject.month)].append(date)

            return x_date

        dic_approved_dates = (date_data(json.loads(mess.approved_dates), approved_dates))
        dic_rejected_dates = (date_data(json.loads(mess.rejected_dates), rejected_dates))

        mess.mess_cut_dates = json.dumps(mess_data)
        mess.approved_dates = json.dumps(dic_approved_dates)
        mess.rejected_dates = json.dumps(dic_rejected_dates)
        mess.process_date = datetime.now().timestamp()

        mess.save()

        return redirect('/mess/secretary/processing')

    else:
        return redirect('/')

def edit(request, type, mess_id, year=datetime.now().year, month=datetime.now().month):
    if request.user.is_authenticated and (request.user.username == 'mess'):
        if month.isalpha():
            month = datetime.strptime(month, "%B").month

        approved_dates = json.loads(MessCut.objects.get(id=mess_id).approved_dates)
        rejected_dates = json.loads(MessCut.objects.get(id=mess_id).rejected_dates)

        if type == 'approved':
            dates = approved_dates[str(year)][str(month)]
        elif type == 'rejected':
            dates = rejected_dates[str(year)][str(month)]

        args = {'dates': dates, 'type': type, 'mess_id': mess_id}
        return render(request, 'mhsite/edit.html', args)

    else:
        return redirect('/')


def submit_edit(request, type, mess_id, year=datetime.now().year, month=datetime.now().month):
    if request.user.is_authenticated and (request.user.username == 'mess'):
        mess = MessCut.objects.get(id=mess_id)
        if month.isalpha():
            month = datetime.strptime(month, "%B").month
        approved_dates = json.loads(mess.approved_dates)
        rejected_dates = json.loads(mess.rejected_dates)

        if type == 'approved':
            dates = {date:request.POST[date] for date in approved_dates[str(year)][str(month)] if date in request.POST}

            for date in dates:
                if dates[date] == '0':
                    approved_dates[str(year)][str(month)].remove(date)

                    if year in rejected_dates:
                        if str(month) in rejected_dates[year]:
                            rejected_dates[str(year)][str(month)].append(date)
                        else:
                            rejected_dates[str(year)][str(month)] = []
                            rejected_dates[str(year)][str(month)].append(date)
                    else:
                        rejected_dates[str(year)] = {}
                        rejected_dates[str(year)][str(month)] = []
                        rejected_dates[str(year)][str(month)].append(date)

        if type == 'rejected':
            dates = {date: request.POST[date] for date in rejected_dates[str(year)][str(month)] if date in request.POST}
            for date in dates:
                if dates[date] == '1':
                    rejected_dates[str(year)][str(month)].remove(date)

                    if year in approved_dates:
                        if str(month) in approved_dates[year]:
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

        return redirect('/mess/secretary/processing')

    else:
        return redirect('/')

def expense(request, year, month, day):
    if request.user.is_authenticated and (request.user.username == 'mess'):
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
                    return redirect('/expense' + '/' + date)

                except IntegrityError as e:

                    return render(request, 'mhsite/expense_tracker.html', args)
            else:
                args = {'form': form}
                return render(request, 'mhsite/expense_tracker.html', args)

        # edit/create expense
        else:
            # edit expense for a month
            try:
                expense = Expense.objects.get(date=date)
                form = ExpenseForm(instance=expense)
                args = {'form': form}
                return render(request, 'mhsite/expense_tracker.html', args)
            # create expense for a month
            except Expense.DoesNotExist:
                form = ExpenseForm(initial={'date': date})
                args = {'form': form}
                return render(request, 'mhsite/expense_tracker.html', args)
    else:
        return redirect('/')

class Report(FormView):

    template_name = 'mhsite/report.html'
    form_class = ReportForm

    def form_valid(self, form):
        if self.request.user.is_authenticated and (self.request.user.username == 'mess'):
            date = form.cleaned_data.get('date')
            year = date.year
            month = format(date, 'm')
            day = '01'
            return redirect('report_details', year, month, day)
        else:
            return redirect('/')

class ReportDetails(View):


    def get(self, request, year, month, day):
        if request.user.is_authenticated and (request.user.username == 'mess'):
            date = (year + '-' + month + '-' + day)
            try:
                expense = Expense.objects.get(date=date)
                return render(request, 'mhsite/report_details.html', {'data': expense, 'link': date})

            except Expense.DoesNotExist:
                return redirect('expense', year, month, day)
        else:
            return redirect('/')
