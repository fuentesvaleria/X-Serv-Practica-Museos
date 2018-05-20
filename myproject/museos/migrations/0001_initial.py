# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('texto', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('titulo', models.CharField(max_length=50, blank=True)),
                ('size', models.CharField(max_length=20, blank=True)),
                ('color', models.CharField(max_length=20, default='black')),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('idx', models.IntegerField()),
                ('nombre', models.CharField(max_length=200, default='')),
                ('descripcion', models.TextField(blank=True, default='')),
                ('accesibilidad', models.IntegerField(choices=[(0, '0'), (1, '1')])),
                ('url', models.CharField(max_length=200, blank=True, default='')),
                ('via', models.CharField(max_length=100, blank=True, default='')),
                ('localidad', models.CharField(max_length=100, blank=True, default='')),
                ('provincia', models.CharField(max_length=30, blank=True, default='')),
                ('codigo_postal', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('barrio', models.CharField(max_length=200, blank=True, default='')),
                ('distrito', models.CharField(max_length=200, blank=True, default='')),
                ('telefono', models.CharField(max_length=40, default='S/T')),
            ],
        ),
        migrations.CreateModel(
            name='Seleccionmuseo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha', models.DateTimeField()),
                ('museo', models.ForeignKey(to='museos.Museo')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comentario',
            name='museo',
            field=models.ForeignKey(null=True, to='museos.Museo'),
        ),
    ]
