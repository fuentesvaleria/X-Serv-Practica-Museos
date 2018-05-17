from django.shortcuts import render, render_to_response
#importo models 
from museos.models import Museo, Comentario
from museos.models import Control, Seleccionmuseo
#para usar login y logout
from django.contrib.auth import authenticate, login, logout
#para poder cargar una plantilla template
# https://docs.djangoproject.com/en/1.11/ref/templates/upgrading/
from django.template import Context, RequestContext
from django.template.loader import get_template
#usuario
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import xml.etree.ElementTree
import urllib.request import urlopen
from django.utils import timezone
# Create your views here.

direccion = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'

@csrf_exempt
def barra(request):
	#aqui tiene que ir la plantilla
"""
 un boton, que al pulsarlo se pasara a ver en todos 
 los listados los museos accesibles, y solo estos. 
 Si se vuelve a pulsar, se volveran a ver todos los museos.
"""
	if request.method == "POST":
		if "btn" in request.POST:
			option = request.POST['btn']
			if option == "push on":
"""
para agregar objetos individuales
# Each publisher, each with a count of books as a "num_books" attribute.
>>> from django.db.models import Count
>>> pubs = Publisher.objects.annotate(num_books=Count('book'))
Reserved.objects.filter(client=client_id).order_by('check_in')[::-1]
order_by = ordenar una lista 
https://stackoverflow.com/questions/9834038/django-order-by-query-set-ascending-and-descending
"""
				cincoment = Museo.objects.annotate(num_comentarios=Count('comentario')).filter(accesibilidad=1).order_by('-num_comentarios')[:5]
				accesibilidad = True
		else:
			option = ""
			#tenemos que parsear ademas de introducir el http museos
"""
urllib.request.urlopen( Url , datos = Ninguno , [ tiempo de espera , ] * ,
 cafile = Ninguno , capath = Ninguno , cadefault = False , context = Ninguno ) 
Abrir la URL url , que puede ser una cadena o un Requestobjeto.
https://docs.python.org/3/library/urllib.request.html
"""
			archivoxml = urlopen(direccion)
			#https://www.josedomingo.org/pledin/2015/01/trabajar-con-ficheros-xml-desde-python_1/
			tree = etree.parse(archivoxml)
			root = tree.getroot()
			for elemento in root.iter():
				if "IDX" in elem.attrib.values():
					Museonuevo = Museo(idEntidad=elem.text)
				elif "NAME" in elem.attrib.values():
					Museonuevo.nombre = elem.text
				elif "DESCRIPCION" in elem.attrib.values():
					Museonuevo.descripcion = elem.text
				elif "ACCESIBILIDAD" in elem.attrib.values():
					Museonuevo.accesibilidad = elem.text
				elif "URL" in elem.attrib.values():
					Museonuevo.url = elem.text
				elif "VIA" in elem.attrib.values():
					Museonuevo.via = elem.text
				elif "LOCALIDAD" in elem.attrib.values():
					Museonuevo.localidad = elem.text
				elif "PROVINCIA" in elem.attrib.values():
					Museonuevo.provincia = elem.text
				elif "CODIGO-POSTAL" in elem.attrib.values():
					Museonuevo.codigo_postal = elem.text
				elif "BARRIO" in elem.attrib.values():
					Museonuevo.barrio = elem.text
				elif "DISTRITO" in elem.attrib.values():
					Museonuevo.distrito = elem.text
				elif "TELEFONO" in elem.attrib.values():
					Museonuevo.telefono = elem.text
				elif "TIPO" in elem.attrib.values():
					Museonuevo.save()
				else:
					pass
	if request.method == "GET" or option == "push off" or option == "":
		cincoment = Museo.objects.annotate(num_comentarios('comentario')).order_by('-num_comentarios')[:5]
		accesibilidad = False
	listcontroles = Control.object.all()
	listusuarios = User.objects.all()
	if len(listcontroles) != len(listusuarios):
		for usuario in listusuarios:
			try:
				user = Control.object.all(usuario=usuario)
				except Control.DoesNotExist:
					user = Control(usuario=usuario)
					user.save()
		listcontroles = Control.object.all()
	listmuseos = Museo.object.all()
	if len(listmuseos) == 0:
		load = True
	else
		load = False
	
	respuesta = request
	return(respuesta) #tengo que implementarlo con templete
				
"""
crear una def login personalizada
def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
    return render_to_response('login.html', context_instance=RequestContext(request))

@login_required(login_url='/login/')
def main(request):
"""
@csrf_exempt
def userlogin(request):
	if request.method == "POST":
		nick = request.POST['username'] 
		password = request.POST['password']
		usuario = authenticate(username=nick, password=password)
        if usuario is not None:
            if usuario.is_active:
                login(request, usuario)
    return HttpResponseRedirect('/')

@csrf_exempt
def userlogout(request):
	if request.method == "POST":
		logout(request)
	return HttpResponseRedirect('/')
	
@csrf_exempt
"""
/museos: -> tengo que poner request
 Pagina con todos los museos. 
 Para cada uno de ellos aparecera solo el nombre, 
 y un enlace a su pagina. 
"""
def pagmuseos (request):
	#tengo que introducir plantilla
	if request.method == "POST":
"""
 En la parte superior de la pagina, existira un formulario distrito. 
 Para poder filtrar por distrito, se buscara en la base de datos cuales 
 son los distritos con museos.
"""
		if "options" in request.POST:
			distrito = request.POST['options']
			if distrito == "All"
				listmuseos = Museo.object.all()
			else:
				listmuseos = Museo.object.filter(distrito = distrito)
		else:
			if "Poner" in request.POST:
				uxd = request.POST['Poner']
				#para trocerar en , porque todo esta separado asi
				idx = uxd.split(',')[0]
				nick = uxd.split(',')[1]
				museo = Museo.object.get(idx=idx)
				usuario = User.object.get(username=nick)
				#debemos guardar con hora y fecha 
				#que hemos agregado ese museo
"""
https://es.stackoverflow.com/questions/121867/implementación-hora-y-fecha-en-django
 def get_default_my_hour():
      hour = timezone.now()
      formatedHour = hour.strftime("%H:%M:%S")
      return formatedHour
"""
				hour = timezone()
				newseleccion = Seleccionmuseo(usuario=usuario, museo=museo, fecha=hour)
				newseleccion.save()
			else:
				uxd = request.POST['NoPoner']
				#para trocerar en , porque todo esta separado asi
				idx = uxd.split(',')[0]
				nick = uxd.split(',')[1]
				museo = Museo.object.get(idx=idx)
				usuario = User.object.get(username=nick)
				#debemos borrar esa seleccion
				deleteMuseo = Seleccionmuseo.object.get(usuario=usuario, museo=museo)
				deleteMuseo.delete()
		if request.method == "GET" or "options"not in  request.POST:
			listmuseos = Museo.object.all()
			distrito = "All"
		#necesito todos los valores database de la lista de distritos para 
		#luego convertirlo en tupla y volver a guardarlo en el context
		#necesario para los templates
"""
Para obtener los valores de la DB
Check out the docs for values_list(). Django does a great job of creating the query specific to your request.
chat_messages.objects.all().values_list('name')
Will generate a query similar to:
SELECT `projectname_chat_messages`.`name` FROM `projectname_chat_messages`
obtener los valores lista
mynewlist = list(myset)
lista->tupla
[i[0] for i in e]
"""		
		listmuseos = Museo.object.all().values_list('museo')
		listmuseo = list(set(listmuseos))
		listmuseo = [museo[0]ofr museo in listmuseo]
		if request.user.is_authenticated():
			selecciones = Seleccionmuseo.objects.all().values_list('museo').filter(usuario=request.user)
			listselecciones = [selecciones[0]ofr selecciones in selecciones]
		else:
			listselecciones = ""
			respuesta = request
		return HttpResponse(respuesta)
		

@csrf_exempt
"""
/museos/id por eso tengo que poner request y id
Pagina de un museo en la aplicacion. 
Mostrara toda la informacion razonablemente posible de XML 
del portal de datos abierto del Ayuntamiento de Madrid->metemos laid del museo 
incluyendo al menos la que se menciona en otros apartados de este enunciado, 
la direccion, la descripcion, si es accesible o no, el barrio y el distrito, 
y los datos de contacto.-> texto del museo informacion mejor dicho
Ademas, se mostraran todos los comentarios del museo-> newcomentarios guardo todo 
"""
def museoo(request, idx):
	if request.method == "GET":
		try: #nos dan el id de cada museo
			museo = Museo.object.all(idx=idx)
			###
			comentarios = Comentario.object.filter(idx=idx)
		except Museo.DoesNotExist:
			#hay que meter una plantilla que nos diga que ha habido un error
			plantilla = get_template('error.html')
			return HttpResponse(plantilla.render(), status=404) #404 de que ha habido fallo
	else: #seria un post que significa que quiere agregar un comentario 
		respuesta = request.POST['texto']
		museo = Museo.objects.get(idx=idx)
		#tengo nuevo comentario donde devo guardar el texto y el museo
		# Ademas, se mostraran todos los comentarios que se 
		#hayan puesto para este museo.
		newcomentario = Comentario(museo=museo, texto=comentario)
		newcomentario.save()
		#tengo que meter el template de la pagina del museo 
		comentarios = Comentario.object.filter(museo=museo)
		respuesta=request
		return HttpResponse(respuesta)#tmb tengo que arreglarlo para que funcione con templates


"""
usuario: Pagina personal de un usuario. 
Si la URL es “/usuario”, 
 Mostrara los museos seleccionados por ese usuario  -> con su pagina personalizada letra color etc
un enlace para mostrar las 5 -> debemos comparar de 5 en 5 
 Ademas, para cada museo se debera mostrar 
 la fecha en la que fue seleccionada por el usuario.
"""

@csrf_exempt
def pusuario(request,nick):
	if request.method == "GET":
		try:
			usuario = User.objects.get(username=nick)
		except User.DoesNotExit:
			plantilla = get_template('error.html')
			return HttpResponse(plantilla.render(),status = 404)
		#para el query_string
		queri = request.META['QUERY_STRING']
	else:
		queri = ""
		if request.user.is_authenticated():
			usuario = User.objects.get(username=request.user.nick)
			try:
				usuario = Control.objects.get(usuario=usuario)
			except:
				user = User.objects.get(username=request.user.nick)
				usuario = Control(usuario=user)
			if 'titulo' in request.POST: #porque el usuario puede personalizar su pagina 
				usuario.titulo = request.POST['titulo']
			else:
				usuario.size = request.POST['size']
				usuario.color = request.POST['color']
			usuario.save()
	#aqui va plantulla del usuario
	usuario = User.objects.get(username=nick)
	if queri == "":
		selecciones = Seleccionmuseo.objects.filter(usuario=request.user)
	else:
		#https://docs.djangoproject.com/en/2.0/ref/contrib/postgres/fields/
		#operador de desigualdad
		rset = Seleccionmuseo.objects.filter(id_gt=(int(queri)))
		selecciones = rset.filter(usuario=usuario)
	
	if len(selecciones) <= 5:
		fin = True
	else:
		fin = False
	try:
		usuario = Control.objects.get(usuario=usuario)
	except:
		usuario = ""
	respuesta = request
	return HttpResponse(respuesta) 
			
	