from django.contrib import admin
from django.contrib.auth.admin  import UserAdmin
from .models import Usuario
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from app.models import Paquete_Inscrito
from django.utils.safestring import mark_safe


class PaquetesInscritosInline(admin.TabularInline):
    model = Paquete_Inscrito
    extra=0


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = Usuario
        fields = ('username','nombre','apellido','password1', 'password2',)

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

    list_display = ('nombre','apellido','email','date_joined','is_admin','check_status_paquetes')
    list_filter = ('status_paquetes','is_admin')

    search_fields=('nombre', 'username',)

    #ready_fields =('date_joined','last_login','imagen_image')
    #inlines = [PaquetesInscritosInline]

    def check_status_paquetes(self,object):

        for paquete in object.paquetes_inscritos.all():
            if paquete.status:
                object.status_paquetes = True
                object.save()
                return True
        object.status_paquetes = False
        object.save()
        return False
    check_status_paquetes.boolean = True

    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'password','email','grupo')}),
        ('Información del Alumno', {'fields': ('nombre', 'apellido','edad','imagen','preview','padecimientos','enfoque','fecha_nacimiento','escuela','domicilio','status_paquetes')}),
        ('Información del Padre o Tutor', {'fields': ('nombre_del_padre','edad_del_padre','ocupacion_del_padre','numero_del_padre',)}),
        ('Información de la Madre o Tutor', {'fields': ('nombre_de_la_madre','edad_de_la_madre','ocupacion_de_la_madre','numero_de_la_madre',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff','is_admin','is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','nombre', 'apellido','password1', 'password2', ),
        }),
    )


    readonly_fields = ['preview','date_joined','last_login','status_paquetes']

    def preview(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.imagen.url,
            width=obj.imagen.width,
            height=obj.imagen.height,
            )
    )

    #list_per_page=15


admin.site.register(Usuario,UsuarioAdmin)
