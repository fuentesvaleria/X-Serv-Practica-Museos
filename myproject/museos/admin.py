from django.contrib import admin

# Register your models here.

from museos.models import Museo
from museos.models import Comentario
from museos.models import Control
from museos.models import Seleccionmuseo


admin.site.register(Museo)
admin.site.register(Comentario)
admin.site.register(Control)
admin.site.register(Seleccionmuseo)
