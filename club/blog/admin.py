from django.contrib import admin
from .models import Post,Comentario,Mensaje
# Register your models here.
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
    list_display =('asunto','nombre')
    search_fields =('nombre',)

admin.site.register(Post,PostAdmin)
admin.site.register(Comentario,ComentarioAdmin)
admin.site.register(Mensaje,MensajeAdmin)
