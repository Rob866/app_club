from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name ='app'
urlpatterns = [

    path('profile/', views.profile,name='profile'),
    path('historial/',views.historial,name='historial'),
    path('logout/',views.logout_view,name="logout"),
    path('login/',views.login_view,name="login"),
    #path('alumnos/', views.AlumnosListView.as_view(), name='alumnos'),
    path('paquetes/',views.paquetes,name='paquetes'),
    path('formNotification/',views.notificacionPage,name="form_notification"),
    path('notificationsList/',views.notificationsList,name='notificationsList'),
    path('notificationsList/delete/<int:id>/',views.deleteNotification,name="borrar_notificacion"),
    path('notificationsList/vista/<int:id>/',views.notificacion,name='notificacion'),
    path('paquetes/<uuid:paquete_id>/',views.clases,name='clases'),
    path('paquetes/<uuid:paquete_id>/<uuid:clase_id>/',views.clase,name='clase'),
    path('events/',login_required(views.Eventos.as_view()),name="events"),
]
