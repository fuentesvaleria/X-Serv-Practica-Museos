# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='control',
            old_name='size',
            new_name='colorFondo',
        ),
        migrations.RenameField(
            model_name='seleccionmuseo',
            old_name='fecha',
            new_name='fechaHora',
        ),
        migrations.RemoveField(
            model_name='control',
            name='color',
        ),
        migrations.AddField(
            model_name='control',
            name='tamanioLetra',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
    ]
