# Generated by Django 3.0.8 on 2020-10-04 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0011_repairman_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='repairman',
            old_name='worksop_name',
            new_name='workshop_name',
        ),
    ]
