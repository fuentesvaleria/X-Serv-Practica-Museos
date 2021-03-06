from django.db import models
#autentificacion de usuario django https://docs.djangoproject.com/en/2.0/topics/auth/default/
from django.contrib.auth.models import User
#guarda lo que has puesto save
from django.db.models.signals import post_save
#lista conectar a una funcion 
from django.dispatch import receiver 
# Create your models here.

class Museo (models.Model):
    idx = models.IntegerField()
    nombre = models.CharField(max_length=200, default='')
    descripcion = models.TextField(default = '', blank = True)
    # debido a que la accesibilidad solo son dos opciones 0/1
    #https://docs.djangoproject.com/en/2.0/ref/models/fields/
    accesibilidad = models.IntegerField(choices=((0, '0'), (1, '1')))
    url = models.CharField(max_length=200, default='', blank = True)
    via = models.CharField(max_length=100, default='', blank=True)
    localidad = models.CharField(max_length=100, default='', blank=True)
    provincia = models.CharField(max_length=30, default='', blank = True)
    codigo_postal = models.PositiveSmallIntegerField(null=True, blank = True)
    barrio = models.CharField(max_length=200, default='', blank = True)
    distrito = models.CharField(max_length=200, default='', blank = True)
    telefono = models.CharField(max_length=40, default="S/T")

    	
class Comentario (models.Model):
    texto = models.TextField()
    museo = models.ForeignKey('Museo')
"""
no se si es necesario
class Pagina(models.Model):
    usuario = models.ForeignKey(User)
    nombre = models.CharField(max_length=200, default='')
    enlace = models.CharField(max_length=200, default='')
    def __str__(self):
        return ('Pagina de ' + self.usuario.nick)
"""   
"""     
clase que se usara para la modificacion del tamaño/color de la pag
uso OneToOneField y no ForeignKey porque va mas rapido y porque se puede agregar campos
personalidados 
#https://stackoverflow.com/questions/31670393/difference-between-foreignkey-and-extending-the-user-class-model-in-django 
"""
     
class Control(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50, blank=True)
    tamanioLetra = models.CharField(max_length=50, blank=True)
    colorFondo = models.CharField(max_length=20, blank=True)


class Seleccionmuseo (models.Model):
    museo = models.ForeignKey('Museo')
    usuario = models.ForeignKey(User)
    fechaHora = models.DateTimeField()