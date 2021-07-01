# Generated by Django 3.0.2 on 2020-04-20 07:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_product_users_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
