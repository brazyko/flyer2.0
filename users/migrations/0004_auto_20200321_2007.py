# Generated by Django 3.0.2 on 2020-03-21 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_chat_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='author',
        ),
        migrations.RemoveField(
            model_name='message',
            name='chat',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
