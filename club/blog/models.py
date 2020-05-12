from django.db import models
import uuid
from django.conf import settings
from django.urls import reverse
from embed_video.fields import EmbedVideoField
# Create your models here.

class Servicio(models.Model):
    ESTADO_STATUS =(
    ('commenting','Comentario'),
    ('book','Libro'),
    ('th','Cuadricula'),
    ('file-text','Archivo'),
    ('cogs','Engranes'),
    ('spinner','Spinner'),
    ('gg','gg'),
    ('sort-alpha-desc','sort-alpha-desc'),
    ('sort-numeric-asc','sort-numeric-asc'),
    ('snowflake-o','snowflake-o'),
    ('share-alt','share-alt'),
    )

    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    icono = models.CharField(max_length=20,choices=ESTADO_STATUS,blank=True)

    def __str_(self):
        return self.titulo

class Testimonio(models.Model):
    imagen =  models.ImageField(default="default.jpg",upload_to='testimonios_pics')
    nombre = models.CharField(max_length=100)
    mensaje = models.TextField()
    profesion = models.CharField(max_length=100)

    def __str_(self):
        return self.nombre

class Rotulo(models.Model):
    subcabecera = models.CharField(max_length=100,default="Bienvenido al Club de Tareas")
    cabecera = models.CharField(max_length=100)
    contenido = models.TextField()
    imagen =  models.ImageField(upload_to='rotulos_pics')

    def __str__(self):
        return self.cabecera

class Publicidad(models.Model):
    imagen =  models.ImageField(upload_to='publicidad_pics')
    class Meta:
        verbose_name_plural ="Carteles de Publicidad"

class Profesor(models.Model):
    imagen = models.ImageField(default="default.jpg",upload_to="profesores_pics")
    nombre = models.CharField(max_length=100)
    profesion = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural= "Profesores"

    def __str__(self):
        return self.nombre



class Post(models.Model):
    STATUS = (
    (0,'borrador'),
    (1,'publicado')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="id del Post")
    titulo = models.CharField(max_length=200,unique=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='blog_posts')
    update_on= models.DateTimeField(auto_now=True)
    imagen = models.ImageField(upload_to='post_image/%Y/%m/%d',blank=True)
    video = models.FileField(upload_to='videos/',null=True,blank=True)
    #video = EmbedVideoField(blank=True)
    content = models.TextField()
    create_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS,default=0)

    class Meta:
        ordering = ['-create_on']

    def get_absolute_url(self):
            return reverse('blog:post_detail', kwargs={'id':self.id})

    def __str__(self):
        return self.titulo

#comentarios de los posts
class Comentario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="id del comentario")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comentarios',null=True)
    nombre = models.CharField(max_length=80)
    mensaje = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Comentarios de Posts"
        ordering = ['created_on']

    def __str__(self):
        return 'Comentario de:{}'.format(self.nombre)

#mensaje de contacto
class Mensaje(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="id del mensaje")
    nombre = models.CharField(max_length=80)
    asunto = models.CharField(max_length=80)
    email = models.EmailField()
    body= models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)



    class Meta:
        verbose_name_plural="Mensajes(Formulario de Contacto)"
        ordering = ['created_on']
    def __str__(self):
        return self.nombre
