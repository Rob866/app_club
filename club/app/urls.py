from django.urls import path
from . import views
app_name ='app'
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('testimony/', views.testimony, name='testimony'),
    path('profile/', views.profile,name='profile'),
    path('logout/',views.logout_view,name="logout"),
    path('login/',views.login_view,name="login"),
    #path('alumnos/', views.AlumnosListView.as_view(), name='alumnos'),
    path('paquetes/',views.paquetes,name='paquetes'),
    path('paquetes/<uuid:paquete_id>/',views.clases,name='clases'),
]
