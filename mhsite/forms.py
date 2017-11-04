from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Application
from django.contrib.auth.models import User
from django.core.validators import RegexValidator




# Application form
class ApplicationForm(forms.ModelForm):
<<<<<<< HEAD
    date_of_birth=forms.DateField(input_formats=('%d/%m/%Y',),)

    class Meta:
        model=Application
        exclude=('status',)
=======
    date_of_birth = forms.DateField(input_formats=('%d/%m/%Y',))

    class Meta:
        model = Application
        fields = '__all__'
>>>>>>> 1604a83491d33b27fe1cf01e9d657fc921011652


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
