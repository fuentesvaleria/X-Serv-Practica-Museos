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
import xml.etree.ElementTree as ET
from django.utils import timezone
from urllib.request import urlopen
# Create your views here.

direccion = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'
@csrf_exempt
def barra(request):
    plantilla = get_template('barra.html')

#un boton, que al pulsarlo se pasara a ver en todos 
#los listados los museos accesibles, y solo estos. 
#Si se vuelve a pulsar, se volveran a ver todos los museos.

    if request.method == "POST":
        if "boton" in request.POST:
            opcion = request.POST['boton']
            if opcion == "Activar":

#para agregar objetos individuales
# Each publisher, each with a count of books as a "num_books" attribute.
#>>> from django.db.models import Count
#>>> pubs = Publisher.objects.annotate(num_books=Count('book'))
#Reserved.objects.filter(client=client_id).order_by('check_in')[::-1]
#order_by = ordenar una lista 
#https://stackoverflow.com/questions/9834038/django-order-by-query-set-ascending-and-descending

                masComentados = Museo.objects.annotate(
                                num_com=Count('comentario')).filter(
                                accesibilidad=1).order_by('-num_com')[:5]
                accesibilidad = True
        else:
        
        #tenemos que parsear ademas de introducir el http museos

#urllib.request.urlopen( Url , datos = Ninguno , [ tiempo de espera , ] * ,
#cafile = Ninguno , capath = Ninguno , cadefault = False , context = Ninguno ) 
#Abrir la URL url , que puede ser una cadena o un Requestobjeto.
#https://docs.python.org/3/library/urllib.request.html	
        
            opcion = ""
            xmlarchivo = urlopen(direccion)
			#https://www.josedomingo.org/pledin/2015/01/trabajar-con-ficheros-xml-desde-python_1/
            arbol = ET.parse(xmlarchivo)
            raiz = arbol.getroot()

            for elem in arbol.iter():
                if "ID-ENTIDAD" in elem.attrib.values():   # Es un diccionario
                    nuevoMuseo = Museo(idx=elem.text)
                elif "NOMBRE" in elem.attrib.values():
                    nuevoMuseo.nombre = elem.text
                elif "DESCRIPCION" in elem.attrib.values():
                    nuevoMuseo.descripcion = elem.text
                elif "ACCESIBILIDAD" in elem.attrib.values():
                    nuevoMuseo.accesibilidad = elem.text
                elif "CONTENT-URL" in elem.attrib.values():
                    nuevoMuseo.url = elem.text
                elif "NOMBRE-VIA" in elem.attrib.values():
                    nuevoMuseo.via = elem.text
                elif "LOCALIDAD" in elem.attrib.values():
                    nuevoMuseo.localidad = elem.text
                elif "PROVINCIA" in elem.attrib.values():
                    nuevoMuseo.provincia = elem.text
                elif "CODIGO-POSTAL" in elem.attrib.values():
                    nuevoMuseo.codigo_postal = elem.text
                elif "BARRIO" in elem.attrib.values():
                    nuevoMuseo.barrio = elem.text
                elif "TELEFONO" in elem.attrib.values():
                    nuevoMuseo.telefono = elem.text
                elif "TIPO" in elem.attrib.values():
                    nuevoMuseo.save()
                else:
                    pass

    if request.method == "GET" or opcion == "Desactivar" or opcion == "":
        masComentados = Museo.objects.annotate(
                        num_com=Count('comentario')).order_by('-num_com')[:5]
        accesibilidad = False

    listaControles = Control.objects.all()
    listaUsuarios = User.objects.all()
    if len(listaControles) != len(listaUsuarios):
        for usuario in listaUsuarios:
            try:
                user = Control.objects.get(usuario=usuario)
            except Control.DoesNotExist:
                user = Control(usuario=usuario)
                user.save()

        listaControles = Control.objects.all()

    listaMuseos = Museo.objects.all()
    if len(listaMuseos) == 0:
        cargar = True
    else:
        cargar = False

    context = RequestContext(request, {'listaUsuarios': listaControles,
                                        'accesibilidad': accesibilidad,
                                        'masComentados': masComentados,
                                        'cargar': cargar})

    return HttpResponse(plantilla.render(context))

#http://www.tutorialmonsters.com/creando-una-web-ejemplo-con-div-y-css-primera-parte/
#carpetas separadas
#http://www.maestrosdelweb.com/curso-django-los-archivos-estaticos/
def css(request):
    plantilla = get_template('css/style.css')
    if request.user.is_authenticated():
        usuario = User.objects.get(username=request.user.username)
        try:
            usuario = Control.objects.get(usuario=usuario)
        except:
            return HttpResponse(plantilla.render(), content_type="text/css")

        context = Context({'color': usuario.colorFondo,
                            'tamanio': usuario.tamanioLetra})

        return HttpResponse(plantilla.render(context),
                            content_type="text/css")

    else:
        return HttpResponse(plantilla.render(), content_type="text/css")


#/museos: -> tengo que poner request
# Pagina con todos los museos. 
# Para cada uno de ellos aparecera solo el nombre, 
# y un enlace a su pagina. 
@csrf_exempt
def pagmuseos(request):
    plantilla = get_template('museos.html')
    if request.method == "POST":
        if "opciones" in request.POST:
            distrito = request.POST['opciones']
            if distrito == "Todos":
                listaMuseos = Museo.objects.all()
            else:
                listaMuseos = Museo.objects.filter(
                                     distrito=distrito)
        else:
            if "marcar" in request.POST:
                recibido = request.POST['marcar']
                idx = recibido.split(',')[0]
                nick = recibido.split(',')[1]
                museo = Museo.objects.get(idx=idx)
                usuario = User.objects.get(username=nick)

#https://es.stackoverflow.com/questions/121867/implementación-hora-y-fecha-en-django
# def get_default_my_hour():
#      hour = timezone.now()
#      formatedHour = hour.strftime("%H:%M:%S")
#      return formatedHour

                fechaHora = timezone.now()
                nuevaSeleccion = Seleccionmuseo(museo=museo,
                                            usuario=usuario,
                                            fechaHora=fechaHora)
                nuevaSeleccion.save()
            else:
                recibido = request.POST['desmarcar']
                idx = recibido.split(',')[0]
                nick = recibido.split(',')[1]
                museo = Museo.objects.get(idx=idx)
                usuario = User.objects.get(username=nick)
                borrarSeleccion = Seleccionmuseo.objects.get(
                                  museo=museo, usuario=usuario)
                borrarSeleccion.delete()

    if request.method == "GET" or "opciones" not in request.POST:
        listaMuseos = Museo.objects.all()
        distrito = "Todos"

    listaDistritos = Museo.objects.all().values_list('distrito')
    listaDistritosUnicos = list(set(listaDistritos))
    listaDistritosUnicos = [distrito[0] for distrito in listaDistritosUnicos]

    if request.user.is_authenticated():
        seleccionados = Seleccionmuseo.objects.all().values_list(
                        'museo').filter(usuario=request.user)
        listaSeleccionados = [seleccionado[0] for seleccionado
                              in seleccionados]
    else:
        listaSeleccionados = ""

    context = RequestContext(request, {'listaDistritos': listaDistritosUnicos,
                                        'museos': listaMuseos,
                                        'distrito': distrito,
                                        'seleccionados': listaSeleccionados})

    return HttpResponse(plantilla.render(context))

#/museos/id por eso tengo que poner request y id
#Pagina de un museo en la aplicacion. 
#Mostrara toda la informacion razonablemente posible de XML 
#del portal de datos abierto del Ayuntamiento de Madrid->metemos laid del museo 
#incluyendo al menos la que se menciona en otros apartados de este enunciado, 
#la direccion, la descripcion, si es accesible o no, el barrio y el distrito, 
#y los datos de contacto.-> texto del museo informacion mejor dicho
#Ademas, se mostraran todos los comentarios del museo-> newcomentarios guardo todo 

@csrf_exempt
def museoo(request, idx):
    if request.method == "GET":
        try:
            museo = Museo.objects.get(idx=idx)
        except Museo.DoesNotExist:
            plantilla = get_template('error.html')

            return HttpResponse(plantilla.render(), status=404)

    else: #seria un post que significa que quiere agregar un comentario 
        comentario = request.POST['texto']
        museo = Museo.objects.get(idx=idx)
        nuevoComentario = Comentario(texto=comentario,
                                     museo=museo)
        nuevoComentario.save()

    plantilla = get_template('pagmuseo.html')
    comentarios = Comentario.objects.filter(museo=museo)
    context = RequestContext(request, {'museo': museo,
                              'comentarios': comentarios})

    return HttpResponse(plantilla.render(context))
    
@csrf_exempt
def pusuario(request, nick):
    if request.method == "GET":
        try:
            usuario = User.objects.get(username=nick)
        except User.DoesNotExist:
            plantilla = get_template('error.html')

            return HttpResponse(plantilla.render(), status=404)

#sirvera para obtener un querystring 
#https://stackoverflow.com/questions/11280948/best-way-to-get-query-string-from-a-url-in-python
#request.META['QUERY_STRING']
#https://docs.djangoproject.com/en/2.0/ref/request-response/#django.http.HttpRequest.META

        queristring = request.META['QUERY_STRING']

    else:
        queristring = ""
        if request.user.is_authenticated():
            usuario = User.objects.get(username=request.user.username)
            try:
                usuario = Control.objects.get(usuario=usuario)
            except:
                user = User.objects.get(username=request.user.username)
                usuario = Control(usuario=user)

            if 'titulo' in request.POST:
                usuario.titulo = request.POST['titulo']
            else:
                usuario.tamanioLetra = request.POST['tamanioLetra']
                usuario.colorFondo = request.POST['colorFondo']
            usuario.save()

    plantilla = get_template('usuario.html')
    usuario = User.objects.get(username=nick)
    if queristring == "":
        seleccionados = Seleccionmuseo.objects.filter(usuario=usuario)
    else:

        restantes = Seleccionmuseo.objects.filter(id__gt=(int(queristring)))
        seleccionados = restantes.filter(usuario=usuario)

    if len(seleccionados) <= 5:
        fin = True
    else:
        fin = False

    try:
        usuario = Control.objects.get(usuario=usuario)
    except:
        usuario = ""

    context = RequestContext(request, {'usuario': usuario,
                                        'nick': nick,
                                        'seleccionados': seleccionados,
                                        'fin': fin})

    return HttpResponse(plantilla.render(context))

#crear una def login personalizada
#def login_user(request):
#    logout(request)
#    username = password = ''
#    if request.POST:
#        username = request.POST['username']
#        password = request.POST['password']
#
#        user = authenticate(username=username, password=password)
#        if user is not None:
#            if user.is_active:
#                login(request, user)
#                return HttpResponseRedirect('/main/')
#    return render_to_response('login.html', context_instance=RequestContext(request))
#
#@login_required(login_url='/login/')
#def main(request):

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

def xml(request, nick):
    try:
        usuario = User.objects.get(username=nick)
    except User.DoesNotExist:
        plantilla = get_template('error.html')

        return HttpResponse(plantilla.render(), status=404)

    plantilla = get_template('xml/xmlmuseos.xml')
    seleccionados = Seleccionmuseo.objects.filter(usuario=usuario)
    context = RequestContext(request, {'usuario': usuario,
                              'seleccionados': seleccionados})

    return HttpResponse(plantilla.render(context), content_type="text/xml")

#el def de los comentarios 
def rss(request):
    plantilla = get_template('rss/comentarios.rss')
    comentarios = Comentario.objects.all()
    context = RequestContext(request, {'comentarios': comentarios})

    return HttpResponse(plantilla.render(context),
                        content_type="text/rss+xml")

def about(request):
    plantilla = get_template('about.html')
    context = RequestContext(request)

    return HttpResponse(plantilla.render(context))
    



