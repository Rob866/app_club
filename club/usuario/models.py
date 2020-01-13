from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class MyUsuarioManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Los usuarios  deben de tener un Email")
        if not username:
            raise ValueError("Los usuarios  deben de tener un Username")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password="None"):
        user = self.create_user(
            email= self.normalize_email(email),
            username=username,
            password=password,

        )

        user.is_admin =True
        user.is_staff = True
        user.is_superuser= True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    email        =  models.EmailField(max_length=60,unique=True)
    username     =  models.CharField(max_length=30,unique=True)

    nombre =  models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    NIVEL_STATUS = (
         ('k','Kinder'),
         ('p','Primaria'),
         ('s','Secundaria'),
         ('b','bachillerato'),
         ('u','universidad'))

    nivel_academico = models.CharField(max_length=1,choices=NIVEL_STATUS,blank=True,help_text='Elige el nivel académico del alumno')

    date_joined  =  models.DateTimeField(verbose_name="fecha de inicio",auto_now_add=True)
    last_login   =  models.DateTimeField(verbose_name="Ultima fecha de Sesión",auto_now=True)
    is_admin     =  models.BooleanField(verbose_name="¿Es Administrador?",default=False)
    is_active    =  models.BooleanField(verbose_name="¿Esta Acivo?",default=True)
    is_staff     =  models.BooleanField(verbose_name="¿Es parte del Staff?",default=False)
    is_superuser =  models.BooleanField(verbose_name="¿Es Super Usuario?",default=False)

    USERNAME_FIELD  = "username"
    REQUIRED_FIELDS = ["nombre","apellido"]
    objects = MyUsuarioManager()

    def __str__(self):
        return f'{self.email}'

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
