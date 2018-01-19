from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Application,Expense,MessCut
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import datetime
from django.utils.dateformat import format


# Application form
class ApplicationForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={"class": "datepicker"}))

    class Meta:
        model = Application
        exclude = ('status',)


        


# Signup Form after application is approved
class RegistrationForm(UserCreationForm):
    admission_number = forms.CharField(max_length=7, validators=[
        RegexValidator(regex=r'^[0-9]{4}/[0-9]{2}$', message='The format for admission number is 1234/17')],
                                       help_text='1234/17')

    class Meta:
        model = User

        fields = (
            'admission_number',
            'first_name',
            'last_name',
            'password1',students = studentlist()
            'password2',
        )

        user.email = email
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={"class": "datepicker"}))

    class Meta:
        model = Expense
        fields = '__all__'

    def save(self, commit=True):
        data = super(ExpenseForm, self).save(commit=False)
        date = self.cleaned_data.get('date')
        year = date.year
        month = format(date, 'm')
        day = '01'
        data.date = (datetime.datetime.strptime(day + month + str(year), "%d%m%Y").date())

        if commit:
            data.save()


class ReportForm(forms.Form):
    date=forms.DateField(widget=forms.TextInput(attrs={"class":"datepicker"}))


class MessCutForm(forms.Form):

    start_date=forms.DateField(widget=forms.TextInput(attrs={"class":"datepicker"}))
    end_date=forms.DateField(widget=forms.TextInput(attrs={"class":"datepicker"}))

    def save(self,commit=True):
        data=super(MessCutForm,self).save(commit=False)
        data.mess_cut_dates=self.cleaned_data['mess_cut_dates']
        data.email=self.cleaned_data['email']

        if commit:
            data.save()
"""class MessCutForm(forms.ModelForm):
    start_date=forms.DateField(widget=forms.TextInput(attrs={"class":"datepicker"}))
    end_date=forms.DateField(widget=forms.TextInput(attrs={"class":"datepicker"}))


    class Meta:
        model=MessCut
        fields='__all__'
        widgets = {'email': forms.HiddenInput()}

    def save(self,commit=True):
        data=super(MessCutForm,self).save(commit=False)
        data.start_date=self.cleaned_data['start_date']
        data.start_date=self.cleaned_data['end_date']
        data.email=self.cleaned_data['email']

        if commit:
            data.save()"""
