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


class NotificationForm(forms.Form):
    description = forms.CharField(label="Mensaje",required=True,widget=forms.Textarea(attrs={ 'class':'form-control','placeholder':'Escribe un mensaje..','style':'background-color: aliceblue !important;'}))

    def clean_description(self):
        description = self.cleaned_data['description']
        if not description:
            raise forms.ValidationError("Campo de Mensaje vacío")
        return description


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

    username         = forms.CharField(label="Username",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Username'}))
    email            = forms.EmailField(label="Email de contacto",required=False,widget=forms.EmailInput(attrs={'class': 'form-control'}))
    facebook         = forms.CharField(label="Facebook de contacto",required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre           = forms.CharField(label="Nombre del Alumno",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Nombre'}))
    apellido         = forms.CharField(label="Apellido del Alumno",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Apellido'}))
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento del Alumno",widget=forms.SelectDateWidget(attrs={ 'class':'custom-select'},years=YEARS),initial="1990-06-21")
    edad             = forms.IntegerField(label="Edad del Alumno",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Edad'}))
    nivel_academico  = forms.ChoiceField(choices=NIVEL_STATUS,widget=forms.Select(attrs={'class':'custom-select'}))
    escuela          = forms.CharField(label="Escuela",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Escuela'}))
    domicilio        = forms.CharField(label="Domicilio",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Domicilio'}))
    imagen           = forms.ImageField()
    asistencia       = forms.CharField(label="Días de asistencia",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'dias de asistencia'}))
    enfoque          = forms.CharField(label="Area en la que guste que se enfocará la atención",required=False,widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Enfoque'}))
    padecimientos    = forms.CharField(label="Alérgias o Padecimientos", required=False,widget=forms.Textarea(attrs={ 'class':'form-control','placeholder':'Alérgias o Padecimientos'}))
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

    def clean_nombre(self):

        if self.is_valid():
            nombre= self.cleaned_data['nombre']
            if not nombre:
                raise forms.ValidationError('El campo nombre no puede estar vacio')
            return nombre

    def clean_apellido(self):

        if self.is_valid():
            apellido=self.cleaned_data['apellido']
            if not apellido:
                raise forms.ValidationError('El campo apellido no puede estar vacio')
            return apellido

    def clean_username(self):

        if self.is_valid():
            username = self.cleaned_data['username']
            if not username:
                raise forms.ValidationError('El campo username no puede estar vacio')
            try:
                account = get_user_model().objects.exclude(pk=self.instance.pk).get(username=username)
            except get_user_model().DoesNotExist:
                return username
            raise forms.ValidationError(f'User: { username } ya esta en uso')
