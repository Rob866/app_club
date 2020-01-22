from django.urls import path
from . import views

app_name ='blog'
urlpatterns = [
    path('', views.home, name='home'),
    path('testimony/', views.testimony, name='testimony'),
    path('blog/',views.blog.as_view(),name='blog'),
    path('blog/<uuid:id>/',views.postDetail,name="post_detail"),
    path('contact/', views.contact,name="contact")

]
