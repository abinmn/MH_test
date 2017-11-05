from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Application,Expense
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import datetime
from django.utils.dateformat import format



# Application form
class ApplicationForm(forms.ModelForm):
    date_of_birth=forms.DateField(input_formats=('%d/%m/%Y',),)

    class Meta:
        model=Application
        exclude=('status',)


# Signup Form after application is approved
class RegistrationForm(UserCreationForm):
    admission_number=forms.CharField(max_length=7,
                                    validators=[RegexValidator(regex=r'^[0-9]{4}/[0-9]{2}$',message='The format for admission number is 1234/17')],
                                    help_text='1234/17')
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)


    class Meta:
        model = User

        fields = (
            'admission_number',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()

class ExpenseForm(forms.ModelForm):

    date=forms.DateField(widget=forms.SelectDateWidget(years=range(2017,2031)),initial=timezone.now())


    class Meta:
        model=Expense
        fields='__all__'

    def save(self,commit=True):
        data=super(ExpenseForm,self).save(commit=False)
        date = self.cleaned_data.get('date')
        year = date.year
        month = format(date, 'm')
        day = '01'
        data.date=(datetime.datetime.strptime(day+month+str(year), "%d%m%Y").date())

        if commit:
            data.save()

class ReportForm(forms.Form):
    date=forms.DateField(widget=forms.SelectDateWidget(years=range(2017,2031)),initial=timezone.now())
