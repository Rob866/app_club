from django.shortcuts import render
from .models import Paquete_Inscrito,Historial_User,Sesion,Notificacion
from django.db.models import Q
from django.templatetags.static import static
from django.conf import settings
from django.contrib import  messages
from  django.contrib.auth import (login,logout,authenticate,get_user_model)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views import View
from django.http import HttpResponseRedirect,Http404,HttpResponse
from .forms import (UserAuthentication, UserUpdateForm,NotificationForm)
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from  notifications.signals import notify
from  notifications.models import Notification
import online_users.models
from datetime import timedelta
from datetime import datetime
from blog.models import Publicidad
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
import json

@login_required
def notificacionPage(request):
    context = {}
    if request.POST:
        form = NotificationForm(request.POST)
        if form.is_valid():
            mensaje = request.POST['description']
            verb=""
            form.cleaned_data
            if request.user.is_superuser:
                #obtengo a todos los usuarios que no son del staff
                users = get_user_model().objects.filter(is_superuser=False)
                verb="Mensaje del Staff"
            else:
                #obtengo todos los usuarios que son del staff
                users = get_user_model().objects.filter(is_superuser=True)
                verb="Mensaje de Usuario"
            notify.send(request.user,recipient=users,verb=verb,
            description=mensaje,action_object= request.user)
            messages.success(request,'Tu mensaje a sido enviado con éxito')
            return HttpResponseRedirect(reverse('app:form_notification'))
    else:
        form = NotificationForm()
    context["notification_form"] = form
    return render(request,'app/form_notification.html',context)

#borrar una sola notificacion
@login_required
def deleteNotification(request,id):
    try:
        notificacion = Notification.objects.all().get(id=id)
    except  Notification.DoesNotExist:
        raise Http404("Notificacion no encontrada")

    if request.POST:
        if not (notificacion.recipient == request.user):
             raise PermissionDenied()

        if notificacion:
            notificacion.delete()
            return HttpResponseRedirect(reverse('app:notificationsList'))
        else:
            raise Http404("Elemento no encontrado")

    context  =   {"notificacion": notificacion }
    return render(request,'app/delete_notification.html',context)

#borrar todas las notificaciones de un usuario normal
@login_required
def deleteAllNotification(request):
    if  request.user.is_superuser:
        return HttpResponseRedirect(reverse('app:notificationsList'))
    if request.POST:
        try:
            user_notifications = Notification.objects.all().filter(recipient=request.user)
        except Notification.DoesNotExist:
            raise  Http404("Notificaciones no encontradas")

        if user_notifications:
            for notificacion in user_notifications:
                notificacion.delete()
        return HttpResponseRedirect(reverse('app:notificationsList'))
    context = {"mensaje": "Seguro de que quieres eliminar todas las Notificaciones?"}
    return render(request,'app/delete_all_notifications.html', context)


#borrar notificaciones segun el tipo de notificacion
#para superusuarios

@login_required
def deleteByTopicNotifications(request,verb=None):
    if  not request.user.is_superuser:
        return HttpResponseRedirect(reverse('app:notificationsList'))
    user_notifications = Notification.objects.all().filter(recipient=request.user)
    notificaciones_by_topic = user_notifications.filter(verb=verb.replace('_',' '))

    if (not user_notifications) or (not notificaciones_by_topic):
        raise Http404("No hay notificaciones para eliminar")
        
    if request.POST:
        if notificaciones_by_topic:
            for notificacion in notificaciones_by_topic:
                notificacion.delete()
            return HttpResponseRedirect(reverse('app:notificationsList'))
        else:
            raise Http404("Elemento que se desea eliminar no encontrado")

    context ={ 'verb' : verb.replace('_',' ') }
    return render(request,'app/delete_by_topic_notifications.html',context)


@login_required
def profile(request):
    context = {}
    if request.POST:
        form = UserUpdateForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            if form.changed_data:
                evento = Historial_User(mensaje=f"datos actualizados del Perfil: {form.changed_data}",usuario=request.user)
                evento.save()
                messages.success( request,'Los datos del formulario han sido actualizados')
                if not request.user.is_superuser:
                    usuarios = get_user_model().objects.filter(is_superuser=True)
                    notify.send(request.user,recipient=usuarios,verb="Datos de Perfil Actualizado",description=f"datos actualizados del Perfil: {form.changed_data}",action_object=request.user)
        else:
            messages.warning(request,'Error al procesar el formulario')
    else:
        form =UserUpdateForm(instance=request.user)
        '''initial = {
          'username' :request.user.username,
          'email': request.user.email,
          'facebook': request.user.facebook,
          'nombre': request.user.nombre,
          'apellido': request.user.apellido,
          'fecha_nacimiento': request.user.fecha_nacimiento,
          'edad': request.user.edad,
          'escuela': request.user.escuela,
          'domicilio': request.user.domicilio,
          'imagen': request.user.imagen,
          'nivel_academico': request.user.nivel_academico,
          'padecimientos': request.user.padecimientos,
          'asistencia': request.user.asistencia,
          'enfoque': request.user.enfoque,
          'nombre_de_la_madre': request.user.nombre_de_la_madre,
          'edad_de_la_madre': request.user.edad_de_la_madre,
          'ocupacion_de_la_madre': request.user.ocupacion_de_la_madre,
          'numero_de_la_madre': request.user.numero_de_la_madre,
          'nombre_del_padre': request.user.nombre_del_padre,
          'edad_del_padre': request.user.edad_del_padre,
          'ocupacion_del_padre': request.user.ocupacion_del_padre,
          'numero_del_padre': request.user.numero_del_padre
          }
        )'''

    context['profile_form'] = form
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))

    context['online_users'] = (user for user in  user_status)
    context['historial'] = request.user.historial.all().order_by('-fecha')

    publicidad = Publicidad.objects.all()
    id_item_activate = 0

    if publicidad:
        id_item_activate = publicidad[0].id
    context["publicidad"] = publicidad
    context["id_item_activate"] = id_item_activate

    return render(request,'app/profile.html',context)


def logout_view(request):
    logout(request)
    messages.success( request,'Has salido de sesión con éxito')
    return HttpResponseRedirect(reverse('app:login'))

def login_view(request):
    context= {}
    user  = request.user
    if user.is_authenticated:
        return HttpResponseRedirect(reverse('app:profile'))

    if request.POST:
        form = UserAuthentication(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)

            if user:
                login(request,user)
                return HttpResponseRedirect(reverse('app:profile'))
    else:
        form = UserAuthentication()
    context['login_form'] = form


    return render(request,'app/login.html',context)

@login_required
def paquetes(request):
    context = {
    'student' : request.user,
    'paquetes': request.user.paquetes_inscritos.all()
    }
    return render(request,'app/paquetes.html',context)


@login_required
def clases(request,paquete_id):
    try:
        paquete = Paquete_Inscrito.objects.all().get(id=paquete_id)
        clases = Sesion.objects.filter(paquete_inscrito=paquete)
        if not (paquete.usuario == request.user):
            raise PermissionDenied()
    except  Paquete_Inscrito.DoesNotExist:
        raise Http404
    except  Sesion.DoesNotExist:
        raise Http404

    context = {
        'student':request.user,
        'clases': clases,
        'paquete':paquete
         }
    return render(request,'app/clases.html',context)


@login_required
def clase(request,paquete_id,clase_id):
    try:
        paquete = Paquete_Inscrito.objects.all().get(id=paquete_id)
        sesion = Sesion.objects.all().get(id=clase_id)
    except  Paquete_Inscrito.DoesNotExist:
        raise Http404("Pauete no Encontrado")
    except  Sesion.DoesNotExist:
        raise Http404("Sesion no encontrada")

    if (not paquete.usuario == request.user) or (not sesion.paquete_inscrito == paquete):
        raise PermissionDenied()

    context = {
    'sesion': sesion,
    'paquete_id': paquete_id
    }
    return render(request,'app/clase.html',context)


@login_required
def historial(request):
    historial = request.user.historial.all().order_by('-fecha')
    context = {
    'historial': historial
    }
    return render(request,'app/historial.html',context)


class Eventos(View):

    def get(self,request,*args,**kwargs):
        seleccion = ''
        eventslist = []
        seleccion = request.GET.get('seleccion')
        if seleccion == "clases":
            for paquete  in request.user.paquetes_inscritos.all():
                for clase in paquete.sesiones.all():
                    eventslist.append({ 'titulo' : clase.asignatura, 'fecha':clase.tiempo_de_salida,'paquete_id':clase.paquete_inscrito.id ,'clase_id': clase.id,'color':'red'})
        else:
            seleccion = 'notificaciones'
            eventslist= []
            for notificacion in request.user.notifications.all():
                eventslist.append({'titulo': notificacion.verb, 'fecha': notificacion.timestamp,'id':notificacion.id,'color':'blue' })

        context = {
        'eventslist': eventslist,
        'seleccion': seleccion
        }
        return render(request,'app/eventos.html',context)


@login_required
def notificacion(request,id):
    try:
        notificacion = Notification.objects.all().get(id=id)
    except Notification.DoesNotExist:
        raise Http404("Elemento no Encontrado")

    if not (notificacion.recipient == request.user):
        raise PermissionDenied

    notificacion.mark_as_read()
    context ={
    "notificacion": notificacion
    }
    return render(request,'app/notificacion.html',context)


@login_required
def notificationsList(request):
    if not request.user.is_superuser:
        try:
            notificaciones = Notification.objects.all().filter(recipient=request.user)
        except  Notification.DoesNotExist:
            raise Http404("Elementos no encontrados")

        paginator = Paginator(notificaciones,5)
        page= request.GET.get('page')
        try:
            notificaciones = paginator.page(page)
        except PageNotAnInteger:
            notificaciones = paginator.page(1)
        except  EmptyPage:
            notificaciones = paginator.page(paginator.num_pages)
        context = {"notificaciones": notificaciones}
        return render(request,'app/notificationsList.html',context)
    else:
        try:
            notificaciones = Notification.objects.all().filter(recipient=request.user)
        except  Notification.DoesNotExist:
            raise Http404('Elementos no encontrados')


        notificaciones_message_user =  notificaciones.filter(verb="Mensaje de Usuario")
        paginator = Paginator(notificaciones_message_user,5)
        page= request.GET.get('page1')
        try:
            notificaciones_message_user = paginator.page(page)
        except PageNotAnInteger:
            notificaciones_message_user = paginator.page(1)
        except  EmptyPage:
            notificaciones_message_user = paginator.page(paginator.num_pages)
        notificaciones_edit_profile_user = notificaciones.filter(verb="Datos de Perfil Actualizado")

        paginator = Paginator(notificaciones_edit_profile_user,5)
        page= request.GET.get('page2')
        try:
            notificaciones_edit_profile_user = paginator.page(page)
        except PageNotAnInteger:
            notificaciones_edit_profile_user = paginator.page(1)
        except  EmptyPage:
            notificaciones_edit_profile_user = paginator.page(paginator.num_pages)

        context = {
          'notificaciones_message_user':notificaciones_message_user,
          'notificaciones_edit_profile_user':notificaciones_edit_profile_user}

        return render(request,'app/notificationsList0.html',context)
