from django.contrib import admin
from .models import Post,Comentario,Mensaje,Testimonio,Rotulo,Profesor,Servicio,Publicidad

# Register your models here.
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('titulo',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo','status','create_on')
    search_fields =['titulo','contenido']

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'mensaje', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('nombre',)
    actions = ['desactivar_comentarios']

    def desactivar_comentarios(self, request, queryset):
        queryset.update(active=False)

class MensajeAdmin(admin.ModelAdmin):
    list_display = ('asunto','nombre')
    search_fields = ('nombre',)

class TestimonioAdmin(admin.ModelAdmin):
    list_display=('nombre',)

class RotuloAdmin(admin.ModelAdmin):
    list_display = ('cabecera',)

class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

admin.site.register(Post,PostAdmin)
admin.site.register(Comentario,ComentarioAdmin)
admin.site.register(Mensaje,MensajeAdmin)
admin.site.register(Testimonio,TestimonioAdmin)
admin.site.register(Rotulo,RotuloAdmin)
admin.site.register(Profesor,ProfesorAdmin)
admin.site.register(Servicio,ServicioAdmin)
admin.site.register(Publicidad)
