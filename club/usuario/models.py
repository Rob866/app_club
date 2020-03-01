from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from PIL import Image

class MyUsuarioManager(BaseUserManager):
    def create_user(self,username,nombre,apellido,password=None):
        #if not email:
        #    raise ValueError("Debes de tener un Email")
        if not username:
            raise ValueError("Debes de tener un Username")
        if not nombre:
            raise ValueError("Debes de tener un Nombre")
        if not apellido:
            raise ValueError("Debes de tener un Apellido")

        user = self.model(
            #email=self.normalize_email(email),
            username=username,
            nombre=nombre,
            apellido=apellido,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,nombre,apellido,password="None"):
        user = self.create_user(
            #email= self.normalize_email(email),
            username=username,
            nombre = nombre,
            apellido=apellido,
            password=password,

        )

        user.is_admin =True
        user.is_staff = True
        user.is_superuser= True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser,PermissionsMixin):

    imagen       =  models.ImageField(default='default.jpg',upload_to='profile_pics')
    email        =  models.EmailField(max_length=60,null=True,blank=True)
    facebook     =  models.CharField(max_length=100,null=True,blank=True)
    username     =  models.CharField(max_length=30,unique=True)
    nombre       =  models.CharField(max_length=100,null=True)
    apellido     =  models.CharField(max_length=100,null=True)
    edad         =  models.IntegerField(blank=True, null=True)
    padecimientos = models.TextField(verbose_name="padecimientos",blank=True,null=True)
    asistencia = models.CharField(verbose_name="Días de asistencia",max_length=100,blank=True,null=True)
    enfoque = models.CharField(verbose_name="Area en la que guste que se enfocará la atención",max_length=100,blank=True, null=True)
    nombre_de_la_madre =  models.CharField(verbose_name="Nombre de la Madre",max_length=100,blank=True, null=True)
    edad_de_la_madre =  models.IntegerField(verbose_name="Edad",blank=True, null=True)
    ocupacion_de_la_madre = models.CharField(verbose_name="Ocupación",max_length=100,blank=True,null=True)
    numero_de_la_madre   =  models.IntegerField(verbose_name="Número de contacto",blank=True,null=True)
    nombre_del_padre =  models.CharField(verbose_name="Nombre del Padre",max_length=100,blank=True, null=True)
    edad_del_padre =  models.IntegerField(verbose_name="Edad",blank=True, null=True)
    ocupacion_del_padre = models.CharField(verbose_name="Ocupación",max_length=100,blank=True, null=True)
    numero_del_padre    =  models.IntegerField(verbose_name="Número de contacto",blank=True,null=True)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento",blank=True, null=True)
    escuela      =  models.CharField(verbose_name="Nombre de la escuela",max_length=60,blank=True, null=True)
    domicilio    =  models.CharField(verbose_name="Domicilio",max_length=150,blank=True, null=True)
    status_paquetes = models.BooleanField(verbose_name="¿Tiene Paquetes Activos?",default=False)

    NIVEL_STATUS = (
         ('k','Kinder'),
         ('p','Primaria'),
         ('s','Secundaria'),
         ('b','bachillerato'),
         ('u','universidad'))

    nivel_academico = models.CharField(max_length=1,choices=NIVEL_STATUS,blank=True,verbose_name='Nivel académico del alumno')

    date_joined  =  models.DateTimeField(verbose_name="Fecha de ingreso",auto_now_add=True)
    last_login   =  models.DateTimeField(verbose_name="Ultima fecha de Sesión",auto_now=True)
    is_admin     =  models.BooleanField(verbose_name="¿Es Administrador?",default=False)
    is_active    =  models.BooleanField(verbose_name="¿Esta Acivo?",default=True)
    is_staff     =  models.BooleanField(verbose_name="¿Es parte del Staff?",default=False)
    is_superuser =  models.BooleanField(verbose_name="¿Es Super Usuario?",default=False)


    USERNAME_FIELD  = "username"
    REQUIRED_FIELDS = ["nombre","apellido"]
    objects = MyUsuarioManager()

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.imagen.path)

        if img.height > 300 or img.width > 300:
            outputsize=(300,300)
            img.thumbnail(outputsize)
            img.save(self.imagen.path)


    def __str__(self):
        return f'{self.nombre}  {self.apellido}'

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
