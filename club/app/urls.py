from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
app_name ='app'
urlpatterns = [
    path('profile/', views.profile,name='profile'),
    path('historial/',views.historial,name='historial'),
    path('logout/',views.logout_view,name="logout"),
    path('login/',views.LoginView.as_view(),name="login"),
    #path('alumnos/', views.AlumnosListView.as_view(), name='alumnos'),
    path('paquetes/',views.paquetes,name='paquetes'),
    path('formNotification/',views.notificacionPage,name="form_notification"),
    path('notificationsList/',views.notificationsList,name='notificationsList'),
    path('notificationsList/delete_notification/<int:id>',views.deleteNotification,name="borrar_notificacion"),
    path('notificationsList/vista/<int:id>',views.notificacion,name='notificacion'),
    path('notificationsList/delete_by_topic/<str:verb>',views.deleteByTopicNotifications,name='delete_by_topic'),
    path('notificationsList/delete_all_notifications/',views.deleteAllNotification,name='delete_all'),
    path('paquetes/<uuid:paquete_id>/',views.clases,name='clases'),
    path('paquetes/<uuid:paquete_id>/<uuid:clase_id>',views.clase,name='clase'),
    path('events',login_required(views.Eventos.as_view()),name="events"),
    path('change_password/', views.change_password, name='change_password'),
]
