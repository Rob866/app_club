from django import forms
from django.contrib.auth import (get_user_model, authenticate)
YEARS= [x for x in range(1940,2021)]
NIVEL_STATUS = (
         ('k','Kinder'),
         ('p','Primaria'),
         ('s','Secundaria'),
         ('b','bachillerato'),
         ('u','universidad'))

class SearchForm(forms.Form):

    busqueda =  forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Busqueda'}))

class UserAuthentication(forms.ModelForm):

    username= forms.CharField(label="Username",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

    class Meta:
        model  = get_user_model()
        fields = ('username','password')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username,password=password):
            raise forms.ValidationError("Login Inválido")

class UserUpdateForm(forms.ModelForm):

    username= forms.CharField(label="Username",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Username'}))
    email= forms.EmailField(label="Email",widget=forms.EmailInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(label="Nombre",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Nombre'}))
    apellido = forms.CharField(label="Apellido",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Apellido'}))
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento",widget=forms.SelectDateWidget(attrs={ 'class':'custom-select'},years=YEARS),initial="1990-06-21")
    edad = forms.IntegerField(label="Edad",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Edad'}))
    nivel_academico = forms.ChoiceField(choices=NIVEL_STATUS,widget=forms.Select(attrs={'class':'custom-select'}))
    escuela = forms.CharField(label="Escuela",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Escuela'}))
    numero = forms.IntegerField(label="Número de Contacto",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Tel'}))
    domicilio= forms.CharField(label="Domicilio",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Domicilio'}))
    imagen = forms.ImageField()

    class Meta:
        model = get_user_model()
        fields = ('username','email','nombre','apellido','fecha_nacimiento','edad','escuela','domicilio','numero','imagen','nivel_academico')

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = get_user_model().objects.exclude(pk=self.instance.pk).get(username=username)
            except get_user_model().DoesNotExist:
                return username
            raise forms.ValidationError(f'User:{ username } esta en uso')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = get_user_model().objects.exclude(pk=self.instance.pk).get(email=email)
            except get_user_model().DoesNotExist:
                return email
            raise forms.ValidationError(f'Email:{ email } esta en uso')
