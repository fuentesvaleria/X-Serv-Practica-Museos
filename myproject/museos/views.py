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
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import urllib
# Create your views here.


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
