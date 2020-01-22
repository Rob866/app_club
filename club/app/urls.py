from django.urls import path
from . import views
app_name ='app'
urlpatterns = [

    path('services/', views.services, name='services'),
    path('profile/', views.profile,name='profile'),
    path('logout/',views.logout_view,name="logout"),
    path('login/',views.login_view,name="login"),
    #path('alumnos/', views.AlumnosListView.as_view(), name='alumnos'),
    path('paquetes/',views.paquetes,name='paquetes'),
    path('paquetes/<uuid:paquete_id>/',views.clases,name='clases'),
]
