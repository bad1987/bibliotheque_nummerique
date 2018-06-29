from django import forms
from .models import Document
from django.contrib.auth.models import User


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['description','document',]



class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(label='Mot de Passe',widget=forms.PasswordInput, max_length=50)
    password2 = forms.CharField(label='Confirmer Mot de Passe', widget=forms.PasswordInput, max_length=50)
    matricule = forms.CharField(label='Matricule',max_length=10)
    filiere = forms.CharField(label='Filiere',max_length=50)
    date_naissance = forms.DateField(label='Date Naissance')

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
        help_texts = {'username':None,}


    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Le mot de passe ne correspond pas')
        return cd['password2']

