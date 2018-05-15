"""
https://docs.djangoproject.com/en/1.8/topics/http/urls/
# Examples:
# url(r'^$', 'myproject.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),
"""

from django.conf.urls import include, url
from django.contrib import admin
from museos import views
from django.contrib.auth.views import login, logout

urlpatterns = [
	url(r'^/?$',views.barra, name='pagina principal'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^css/style.css$',views.css, name='css'),
    url(r'^login/?$',views.userlogin, name='Usuario Login'),
    url(r'^logout/?$',views.userlogout, name='Usuario Logout'),
    url(r'^museos/?$',views.pagmuseos, name='Pag con todoslos museos'),
    url(r'^museos/(.*)/?$',views.museoo, name='Pag del museo'),
    url(r'^(.*)/xml/?$',views.xml, name='canal xml'),
    url(r'^about/?$',views.about, name='info en html autoria'),
	url(r'^rss/?$',views.rss, name='comentarios'),
	url(r'(.*)',views.usuario, name='Pagina del usuario'),
]
