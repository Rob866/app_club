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
from django.http import HttpResponseRedirect
from .forms import (UserAuthentication, UserUpdateForm)
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from  notifications.signals import notify
import online_users.models
from datetime import timedelta


def services(request):
    return render(request, 'app/services.html')

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
                usuarios = get_user_model().objects.all()
                if not  request.user.is_superuser:
                    for usuario  in usuarios:
                        if usuario.is_superuser:
                            notify.send(request.user,recipient=usuario,verb="Datos del Perfil Actualizados",description=f"datos actualizados del Perfil: {form.changed_data}",action_object=request.user)

        else:
            messages.warning(request,'Error al procesar el formulario')
    else:
        form =UserUpdateForm(
        initial = {
          'username' :request.user.username,
          'email': request.user.email,
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
    return render(request,'app/profile.html',context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:home'))

def login_view(request):
    context= {}
    user  = request.user
    if user.is_authenticated:
        return HttpResponseRedirect(reverse('blog:home'))

    if request.POST:
        form = UserAuthentication(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)

            if user:
                login(request,user)
                return HttpResponseRedirect(reverse('blog:home'))
    else:
        form = UserAuthentication()
    context['login_form'] = form
    return render(request,'app/login.html',context)



""""
class AlumnosListView(ListView):
    model = Alumno
    template_name= 'app/alumnos.html'
    #context_object_name = 'alumnos'

    def get_queryset(self,query):
        if not query.strip():
            return None
        if len(query) == 5:
            return self.model.objects.filter(id__startswith=query)
            #return Alumno.objects.filter(Q(apellido__icontains=query) | Q(nombre__icontains=query)).order_by('apellido')
        return  None

    def get(self,request,*args,**kwargs):
        if 'busqueda' in self.request.GET:
            query = request.GET.get('busqueda')
            context = {
            'alumnos': self.get_queryset(query)
            }
        else:
            context = {
              'alumnos': None
            }
        return  render(request,self.template_name,context)
"""
@login_required
def paquetes(request):
    #student = get_user_model().objects.all().get(pk=pk)
    #student = request.user
    #paquetes = []
    #for paquete in request.user.paquetes_inscritos.all():
    #    paquetes.append(paquete)
    context = {
    'student' : request.user,
    'paquetes': request.user.paquetes_inscritos.all()
    }
    return render(request,'app/paquetes.html',context)

@login_required
def clases(request,paquete_id):
    #student = get_user_model().objects.all().get(pk=pk)
    paquete = request.user.paquetes_inscritos.all().get(id=paquete_id)
    #paquete  = Paquete_Inscrito.objects.all().get(id=paquete_id)
    #clases = []
    #for clase in paquete.sesiones.all() :
    #    clases.append(clase)

    context = {
        'student':request.user,
        'clases': paquete.sesiones.all(),
        'paquete':paquete
         }
    return render(request,'app/clases.html',context)

@login_required
def clase(request,paquete_id,clase_id):
    sesion = Sesion.objects.all().get(id=clase_id)
    context = {
    'sesion': sesion
    }
    return render(request,'app/clase.html',context)


@login_required
def historial(request):
    historial = request.user.historial.all().order_by('-fecha')
    context = {
    'historial': historial
    }
    return render(request,'app/historial.html',context)

@login_required
def eventos(request):
    eventslist= []
    for paquete  in request.user.paquetes_inscritos.all():
        for clase in paquete.sesiones.all():
            eventslist.append({ 'titulo' : clase.asignatura, 'fecha': str(clase.tiempo_de_salida.date()),'paquete_id':clase.paquete_inscrito.id ,'clase_id': clase.id,'color':'red'})
    eventslist2 = []
    for notificacion in request.user.notifications.all():
        eventslist2.append({'titulo': notificacion.verb, 'fecha': notificacion.timestamp })

    context = {
    'eventslist': eventslist,
    'eventslist2': eventslist2
    }
    return render(request,'app/eventos.html',context)
"""
@login_required
def notificactionList(request):
    request.user.notifications.mark_all_as_read()
    notificaciones = request.user.notifications.read()
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
    users = (user for user in  user_status)

    context = {
            'notificaciones': notificaciones,
            'online_users': users
        }

    return render(request,'app/notifications_list.html',context)

"""
#@login_required
class notificationsList(ListView):
    template_name ='app/notificationsList.html'
    paginate_by= 4
    context_object_name='notificaciones'

    def get_queryset(self):
        self.request.user.notifications.mark_all_as_read()
        #user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
        return self.request.user.notifications.read()
"""
    def get(self,request,*args,**kwargs):
        request.user.notifications.mark_all_as_read()
        notificaciones = request.user.notifications.read()
        user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
        users = (user for user in  user_status)
        context =  {
                'notificaciones': notificaciones,
                'online_users': users
            }

        return  render(request,self.template_name,context)
"""
