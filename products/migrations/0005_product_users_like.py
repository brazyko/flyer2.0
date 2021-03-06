# Generated by Django 3.0.2 on 2020-04-11 18:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_remove_product_users_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='products_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
