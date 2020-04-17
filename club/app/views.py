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
    DeleteView
)
from django.http import HttpResponseRedirect,Http404
from .forms import (UserAuthentication, UserUpdateForm,NotificationForm)
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from  notifications.signals import notify
import online_users.models
from datetime import timedelta
from datetime import datetime
from blog.models import Publicidad
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

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

@login_required
def deleteNotification(request,id):
    #no sirve de nada raise Http404
    notificacion = request.user.notifications.all().get(id=id)
    if notificacion:
        if request.POST:
            notificacion.delete()
            return HttpResponseRedirect(reverse('app:notificationsList'))
    else:
        raise Http404
    context  =   {"notificacion": notificacion }
    return render(request,'app/delete_notification.html',context)


@login_required
def deleteByTopicNotifications(request,verb=None):
    notificaciones = request.user.notifications.filter(verb=verb.replace('_',' '))
    if notificaciones:
        if request.POST:
            for notificacion in notificaciones:
                notificacion.delete()
            return HttpResponseRedirect(reverse('app:notificationsList'))
    else:
        raise  Http404
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
        form =UserUpdateForm(
        initial = {
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
        )

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
       paquete = Paquete_Inscrito.objects.filter(id=paquete_id,usuario= request.user)
       clases = paquete.sesiones.all()
       #paquete = request.user.paquetes_inscritos.all().get(id=paquete_id)
   except:
       Paquete_Inscrito.DoesNotExist:
       raise Http404

    context = {
        'student':request.user,
        'clases': clases,
        'paquete':paquete
         }
    return render(request,'app/clases.html',context)

@login_required
def clase(request,paquete_id,clase_id):
    sesion = Sesion.objects.all().get(id=clase_id)
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


class Eventos(ListView):
    template_name= "app/aventos.html"
    seleccion=""
    eventslist=[]
    def get(self,request,*args,**kwargs):
        if 'seleccion' in self.request.GET:
            self.seleccion = self.request.GET.get('seleccion')
            self.eventslist= []
            if self.seleccion == "clases":
                for paquete  in self.request.user.paquetes_inscritos.all():
                    for clase in paquete.sesiones.all():
                        self.eventslist.append({ 'titulo' : clase.asignatura, 'fecha':clase.tiempo_de_salida,'paquete_id':clase.paquete_inscrito.id ,'clase_id': clase.id,'color':'red'})
            else:
                self.eventslist= []
                for notificacion in self.request.user.notifications.all():
                    self.eventslist.append({'titulo': notificacion.verb, 'fecha': notificacion.timestamp,'id':notificacion.id,'color':'blue' })
        else:
            self.seleccion = "clases"
            self.eventslist=[]
            for paquete in self.request.user.paquetes_inscritos.all():
                for clase in paquete.sesiones.all():
                    self.eventslist.append({ 'titulo' : clase.asignatura, 'fecha':clase.tiempo_de_salida,'paquete_id':clase.paquete_inscrito.id ,'clase_id': clase.id,'color':'red'})
        context = {
            'eventslist': self.eventslist,
            'seleccion': self.seleccion
            }
        return render(request,'app/eventos.html',context)

@login_required
def notificacion(request,id):
    notificacion = request.user.notifications.all().get(id=id)
    notificacion.mark_as_read()
    context ={
    "notificacion": notificacion
    }
    return render(request,'app/notificacion.html',context)

#@login_required
'''
class notificationsList(ListView):
    template_name ='app/notificationsList.html'
    paginate_by= 8
    context_object_name='notificaciones'

    def get_queryset(self):
        return self.request.user.notifications.all()
'''
@login_required
def notificationsList(request):
    if not request.user.is_superuser:
        notificaciones = request.user.notifications.all()
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
        notificaciones = request.user.notifications
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
