from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Application
from django.contrib.auth.models import User

#Application form
class ApplicationForm(forms.ModelForm):
    date_of_birth=forms.DateField(input_formats=('%d/%m/%Y',),)

    class Meta:
        model=Application
        fields='__all__'


#Signup Form after application is approved
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)

    class Meta:
        model = User

        fields = (
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
