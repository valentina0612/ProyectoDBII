# Generated by Django 4.1.12 on 2023-11-03 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('framely', '0006_alter_usuario_email_alter_usuario_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=30),
        ),
    ]