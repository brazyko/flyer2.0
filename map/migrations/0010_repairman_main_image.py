# Generated by Django 3.0.8 on 2020-09-25 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0009_auto_20200924_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairman',
            name='main_image',
            field=models.ImageField(null=True, upload_to='images/%Y/%m/%d/%H/%M/%S/'),
        ),
    ]
