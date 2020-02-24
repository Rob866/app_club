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

    username= forms.CharField(label="Username",widget=forms.TextInput(attrs={ 'class':'fadeIn second username_login','placeholder':'Username'}))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'fadeIn third password_login','placeholder':'Password'}))

    class Meta:
        model  = get_user_model()
        fields = ('username','password')

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username,password=password):
            raise forms.ValidationError("Login Inválido")

class UserUpdateForm(forms.ModelForm):

    username         = forms.CharField(label="Username",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Username'}))
    email            = forms.EmailField(label="Email de contacto",required=False,widget=forms.EmailInput(attrs={'class': 'form-control'}))
    facebook          = forms.CharField(label="Facebook de contacto",required=False,widget=forms.EmailInput(attrs={'class': 'form-control'}))
    nombre           = forms.CharField(label="Nombre del Alumno",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Nombre'}))
    apellido         = forms.CharField(label="Apellido del Alumno",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Apellido'}))
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento del Alumno",widget=forms.SelectDateWidget(attrs={ 'class':'custom-select'},years=YEARS),initial="1990-06-21")
    edad             = forms.IntegerField(label="Edad del Alumno",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Edad'}))
    nivel_academico  = forms.ChoiceField(choices=NIVEL_STATUS,widget=forms.Select(attrs={'class':'custom-select'}))
    escuela          = forms.CharField(label="Escuela",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Escuela'}))
    domicilio        = forms.CharField(label="Domicilio",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Domicilio'}))
    imagen           = forms.ImageField()
    asistencia       = forms.CharField(label="Días de asistencia",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'dias de asistencia'}))
    enfoque          = forms.CharField(label="Area en la que guste que se enfocará la atención",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Enfoque'}))
    padecimientos    = forms.CharField(label="Alérgias o Padecimientos",widget=forms.Textarea(attrs={ 'class':'form-control','placeholder':'Alérgias o Padecimientos'}))
    nombre_de_la_madre     = forms.CharField(label="Nombre de la Madre",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Nombre'}))
    edad_de_la_madre       = forms.IntegerField(label="Edad de la Madre",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Edad'}))
    ocupacion_de_la_madre  = forms.CharField(label="Ocupación de la Madre",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Ocupación'}))
    numero_de_la_madre     = forms.IntegerField(label="Número de la Madre",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Tel'}))
    nombre_del_padre     = forms.CharField(label="Nombre del Padre",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Nombre'}))
    edad_del_padre       = forms.IntegerField(label="Edad del Padre",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Edad'}))
    ocupacion_del_padre  = forms.CharField(label="Ocupación del Padre",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Ocupación'}))
    numero_del_padre     = forms.IntegerField(label="Número del Padre",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Tel'}))

    class Meta:
        model = get_user_model()
        fields = ('username','email','facebook','nombre','apellido','fecha_nacimiento','edad','escuela','domicilio','imagen','nivel_academico','asistencia',
                  'enfoque','padecimientos','nombre_de_la_madre','edad_de_la_madre','ocupacion_de_la_madre','numero_de_la_madre','nombre_del_padre','edad_del_padre','ocupacion_del_padre',
                  'numero_del_padre')

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = get_user_model().objects.exclude(pk=self.instance.pk).get(username=username)
            except get_user_model().DoesNotExist:
                return username
            raise forms.ValidationError(f'User:{ username } esta en uso')
'''
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = get_user_model().objects.exclude(pk=self.instance.pk).get(email=email)
            except get_user_model().DoesNotExist:
                return email
            raise forms.ValidationError(f'Email:{ email } esta en uso')
'''
