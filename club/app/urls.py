from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name ='app'
urlpatterns = [

    path('services/', views.services, name='services'),
    path('profile/', views.profile,name='profile'),
    path('historial/',views.historial,name='historial'),
    path('logout/',views.logout_view,name="logout"),
    path('login/',views.login_view,name="login"),
    #path('alumnos/', views.AlumnosListView.as_view(), name='alumnos'),
    path('paquetes/',views.paquetes,name='paquetes'),
    path('notificactionsList/', login_required(views.notificationsList.as_view()),name='notificactionsList'),
    path('notificactionsList/<int:id>/',views.notificacion,name='notificacion'),
    path('paquetes/<uuid:paquete_id>/',views.clases,name='clases'),
    path('paquetes/<uuid:paquete_id>/<uuid:clase_id>',views.clase,name='clase'),
    path('events/',views.Eventos.as_view(),name="events"),
]
