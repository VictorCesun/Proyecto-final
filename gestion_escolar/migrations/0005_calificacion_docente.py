# Generated by Django 5.1.7 on 2025-04-03 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_escolar', '0004_remove_asistencia_falta_remove_asistencia_presente_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calificacion',
            name='docente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gestion_escolar.docente'),
            preserve_default=False,
        ),
    ]
