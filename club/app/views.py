from django.shortcuts import render
from .models import Paquete_Inscrito
from django.db.models import Q
from django.templatetags.static import static
from django.conf import settings
from  django.contrib.auth import (login,logout,authenticate)
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
# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

def services(request):
    return render(request, 'app/services.html')

def testimony(request):
    return render(request, 'app/testimony.html')

@login_required
def profile(request):
    context = {}
    if request.POST:
        form = UserUpdateForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
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
          'nivel_academico': request.user.nivel_academico}
        )
    context['profile_form'] = form
    return render(request,'app/profile.html',context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:home'))

def login_view(request):
    context= {}
    user  = request.user
    if user.is_authenticated:
        return HttpResponseRedirect(reverse('app:home'))


    if request.POST:
        form = UserAuthentication(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)

            if user:
                login(request,user)
                return HttpResponseRedirect(reverse('app:home'))
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

def paquetes(request,id):
    return_query = str(id)[0:5]
    student = Alumno.objects.all().get(id=id)
    paquetes = []
    for paquete in student.paquete_inscrito_set.all():
        paquetes.append(paquete)
    context = {
    'student' : student,
    'paquetes': paquetes,
    'return_query' : return_query
    }
    return render(request,'app/paquetes.html',context)

def clases(request,id,paquete_id):
    student = Alumno.objects.all().get(id=id)
    paquete  = Paquete_Inscrito.objects.all().get(id=paquete_id)
    clases = []
    for clase in paquete.sesiones.all() :
        clases.append(clase)

    context = {
        'student':student,
        'clases': clases,
        'paquete':paquete
         }
    return render(request,'app/clases.html',context)
"""
