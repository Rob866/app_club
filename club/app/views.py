from django.shortcuts import render,redirect
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
from django.views.generic.edit import  FormView
from django.views import View
from django.http import HttpResponseRedirect,Http404,HttpResponse
from .forms import (UserAuthentication, UserUpdateForm,NotificationForm)
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from  notifications.signals import notify
from  notifications.models import Notification
import online_users
from datetime import timedelta
from datetime import datetime
from blog.models import Publicidad
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
import json
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

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
                verb="notificacion-del-staff"
            else:
                #obtengo todos los usuarios que son del staff
                users = get_user_model().objects.filter(is_superuser=True)
                verb="notificacion-de-usuario"
            if users:
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

    if not (notificacion.recipient == request.user):
        raise PermissionDenied

    if request.POST:
        if notificacion:
            notificacion.delete()
        return HttpResponseRedirect(reverse('app:notificationsList'))


    context  =   {"notificacion": notificacion }
    return render(request,'app/delete_notification.html',context)

#borrar todas las notificaciones de un usuario normal
@login_required
def deleteAllNotification(request):
    if  request.user.is_superuser:
        return HttpResponseRedirect(reverse('app:notificationsList'))

    if request.POST:
        user_notifications = Notification.objects.all().filter(recipient=request.user)
        if not user_notifications:
            raise  Http404("Notificaciones no encontradas para eliminar")
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

    if request.POST:
        user_notifications = Notification.objects.all().filter(recipient=request.user)
        notificaciones_by_topic = user_notifications.filter(verb=verb)
        #verb.replace('_',' ')
        if (not user_notifications) or (not notificaciones_by_topic):
            raise Http404("No hay notificaciones para eliminar")

        for notificacion in notificaciones_by_topic:
            notificacion.delete()
        return HttpResponseRedirect(reverse('app:notificationsList'))

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
                    notify.send(request.user,recipient=usuarios,verb="notificacion-de-edicion-de-perfil",description=f"datos actualizados del Perfil: {form.changed_data}",action_object=request.user)
        else:
            messages.warning(request,'Error al procesar el formulario')
    else:
        form =UserUpdateForm(instance=request.user)

    context['profile_form'] = form
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


class LoginView(FormView):
    form_class = UserAuthentication
    template_name = "app/login.html"
    success_url = reverse_lazy('app:profile')

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return super(LoginView,self).dispatch(request,*args,**kwargs)

    def form_valid(self, form):
        login(self.request,form.get_user())
        return super(LoginView, self).form_valid(form)


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
        notificaciones = Notification.objects.all().filter(recipient=request.user)
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

        notificaciones = Notification.objects.all().filter(recipient=request.user)
        mensajes_de_usuarios = [mensaje for mensaje in  notificaciones.filter(verb="notificacion-de-usuario")]
        mensajes_del_staff = [mensaje for mensaje in  notificaciones.filter(verb="notificacion-del-staff")]

        notificaciones_message_user =  mensajes_de_usuarios + mensajes_del_staff

        paginator = Paginator(notificaciones_message_user,5)
        page= request.GET.get('page1')
        try:
            notificaciones_message_user = paginator.page(page)
        except PageNotAnInteger:
            notificaciones_message_user = paginator.page(1)
        except  EmptyPage:
            notificaciones_message_user = paginator.page(paginator.num_pages)


        notificaciones_edit_profile_user = notificaciones.filter(verb="notificacion-de-edicion-de-perfil")
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
          'notificaciones_edit_profile_user':notificaciones_edit_profile_user
          }

        user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
        context['online_users'] = (user for user in  user_status)

        return render(request,'app/notificationsList0.html',context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Tu password se a Actualizado con Éxito!')
            return HttpResponseRedirect(reverse('app:change_password'))
        else:
            messages.warning(request, 'Por favor corrige los errors que se te indican.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/change_password.html', {
        'form': form
    })
