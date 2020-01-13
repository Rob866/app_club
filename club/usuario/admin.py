from django.contrib import admin
from django.contrib.auth.admin  import UserAdmin
from .models import Usuario
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from app.models import Paquete_Inscrito


class PaquetesInscritosInline(admin.TabularInline):
    model = Paquete_Inscrito
    extra=0

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):

    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Las contraseñas sin procesar no se almacenan, por lo que no hay forma de ver la contraseña de este usuario, "
                    "pero puede cambiar la contraseña mediante este formulario."
                    "<a href=\"../password/\">formulario</a>."))
    class Meta:
        model = Usuario
        fields = '__all__'


class UsuarioAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('nombre','apellido','email','date_joined','is_admin','is_staff',)
    search_fields=('username', 'email',)
    ready_fields =('date_joined','last_login',)
    inlines = [PaquetesInscritosInline]

    filter_horizontal = ()
    list_filter = ('is_staff',)

    fieldsets = ()
    #list_per_page=15


admin.site.register(Usuario,UsuarioAdmin)
