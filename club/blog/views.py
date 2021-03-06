from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post,Comentario,Mensaje,Testimonio,Rotulo,Profesor,Servicio,Publicidad
from .forms import CommentForm,MensajeForm
import uuid
from django.http import HttpResponseRedirect
from django.views.generic import (ListView)
from django.urls import reverse
from django.contrib import  messages

class blog(ListView):
    model= Post
    template_name= 'blog/blog.html'
    context_object_name='posts'
    paginate_by= 3

    def get_queryset(self):
        return self.model.objects.filter(status=1).order_by('-create_on')
        #return Post.objects.filter(status=1).order_by('-create_on')

def services(request):
    servicios = Servicio.objects.all()
    id_activate = 0
    if servicios:
        id_activate = servicios[0].id

    context= {
    'servicios': servicios,
    'id_activate': id_activate
    }

    return render(request, 'blog/services.html',context)

def contact(request):
    if request.method == 'POST':
        mensaje_form = MensajeForm(request.POST)
        if mensaje_form.is_valid():
            #mensaje = Mensaje(nombre=request.POST["nombre"],asunto=request.POST["asunto"],email=request.POST["email"],body=request.POST["body"])
            mensaje_form.save()
            mensaje_form.cleaned_data
            messages.success( request,'Gracias por escribirnos. Nos pondremos en contacto con usted')
            return HttpResponseRedirect(reverse('blog:contact'))
        else:
            messages.warning(request,'Error al procesar el formulario')

    else:
        mensaje_form = MensajeForm()
    context = {
         'mensaje_form': mensaje_form
    }
    return render(request,'blog/contact.html',context)


def postDetail(request,id):
    post_object = get_object_or_404(Post,id=id)
    comment_form= None
    comentarios = post_object.comentarios.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = Comentario(post=post_object,nombre=request.POST["nombre"],mensaje=request.POST["mensaje"])
            new_comment.save()
            return HttpResponseRedirect(post_object.get_absolute_url())
    else:
        comment_form= CommentForm()
    #print(comment_form.errors)
    #obtengo todos los posts activos
    posts = Post.objects.filter(status=1).exclude(id=id)
    # los ordeno segun el numero de comentarios activos (mayor a menor)
    #order_post_by_comments = sorted(posts,key= lambda post: len(post.comentarios.filter(active=True)),reverse=True)
    # me  aseguro que las lista de los post mas comentados sea como máximo 5 posts
    order_post_by_date = sorted(posts,key=lambda post: post.create_on,reverse=True)

    if len(order_post_by_date) > 5 :
        order_post_by_date = order_post_by_date[:6]

    publicidad = Publicidad.objects.all()
    id_item_activate = 0

    if publicidad:
        id_item_activate = publicidad[0].id

    context = {
    'order_post_by_date': order_post_by_date,
    'posts': posts,
    'post': post_object,
    'comentarios': comentarios,
    'comment_form':comment_form,
    'publicidad': publicidad,
    'id_item_activate': id_item_activate
    }

    return render(request,'blog/detail.html',context)

def testimony(request):
    testimonios = Testimonio.objects.all()

    context = {
    "testimonios" : testimonios
    }
    return render(request,'blog/testimony.html',context)

def home(request):
    rotulos = Rotulo.objects.all()
    context = {
    "rotulos" : rotulos
    }
    return render(request,'blog/home.html',context)

def about(request):
    profesores = Profesor.objects.all()
    context = {
    "profesores":profesores
    }
    return render(request, 'blog/about.html',context)
