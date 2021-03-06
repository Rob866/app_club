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

class UserAuthentication(forms.Form):

    username= forms.CharField(label="Username",widget=forms.TextInput(attrs={ 'class':'fadeIn second username_login','placeholder':'Username'}))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'fadeIn third password_login','placeholder':'Password'}))

    def __init__(self,request=None,*args,**kwargs):
        self.request = request
        self.user =None
        super(UserAuthentication,self).__init__(*args,**kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user = authenticate(username=username,password=password)
        if self.user is None:
            raise forms.ValidationError('error de autentificación')
        return self.cleaned_data

    def get_user(self):
        return self.user


class UserUpdateForm(forms.ModelForm):

    username         = forms.CharField(label="Username",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Username'}))
    email            = forms.EmailField(label="Email de contacto",widget=forms.EmailInput(attrs={'class': 'form-control'}),required=False)
    facebook         = forms.CharField(label="Facebook de contacto",widget=forms.TextInput(attrs={'class': 'form-control'}),required=False)
    nombre           = forms.CharField(label="Nombre del Alumno",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Nombre'}))
    apellido         = forms.CharField(label="Apellido del Alumno",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Apellido'}))
    fecha_nacimiento = forms.DateField(label="Fecha de nacimiento del Alumno",widget=forms.SelectDateWidget(attrs={ 'class':'custom-select'},years=YEARS),initial="1990-06-21")
    edad             = forms.IntegerField(label="Edad del Alumno",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Edad'}),required=False)
    #nivel_academico = forms.ChoiceField(choices=NIVEL_STATUS,widget=forms.Select(attrs={'class':'custom-select'}))
    nivel_academico  = forms.CharField(label="Nivel académico",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'nivel cademico'}),required=False)
    escuela          = forms.CharField(label="Escuela",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Escuela'}),required=False)
    domicilio        = forms.CharField(label="Domicilio",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Domicilio'}),required=False)
    imagen           = forms.ImageField()
    asistencia       = forms.CharField(label="Días de asistencia",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'dias de asistencia'}),required=False)
    enfoque          = forms.CharField(label="Area en la que guste que se enfocará la atención",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Enfoque'}),required=False)
    padecimientos    = forms.CharField(label="Alérgias o Padecimientos",widget=forms.Textarea(attrs={ 'class':'form-control','placeholder':'Alérgias o Padecimientos'}),required=False)
    nombre_de_la_madre     = forms.CharField(label="Nombre de la Madre",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Nombre'}),required=False)
    edad_de_la_madre       = forms.IntegerField(label="Edad de la Madre",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Edad'}),required=False)
    ocupacion_de_la_madre  = forms.CharField(label="Ocupación de la Madre",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Ocupación'}),required=False)
    numero_de_la_madre     = forms.IntegerField(label="Número de la Madre",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Tel'}),required=False)
    nombre_del_padre     = forms.CharField(label="Nombre del Padre",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Nombre'}),required=False)
    edad_del_padre       = forms.IntegerField(label="Edad del Padre",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Edad'}),required=False)
    ocupacion_del_padre  = forms.CharField(label="Ocupación del Padre",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Ocupación'}),required=False)
    numero_del_padre     = forms.IntegerField(label="Número del Padre",widget=forms.TextInput(attrs={ 'class':'form-control','placeholder':'Tel'}),required=False)

    class Meta:
        model = get_user_model()
        fields = ('username','email','facebook','nombre','apellido','fecha_nacimiento','edad','escuela','domicilio','imagen','nivel_academico','asistencia',
                  'enfoque','padecimientos','nombre_de_la_madre','edad_de_la_madre','ocupacion_de_la_madre','numero_de_la_madre','nombre_del_padre','edad_del_padre','ocupacion_del_padre',
                  'numero_del_padre')
