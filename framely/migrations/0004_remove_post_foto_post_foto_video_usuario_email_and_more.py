# Generated by Django 4.1.12 on 2023-11-03 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('framely', '0003_usuario_foto_perfil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='foto',
        ),
        migrations.AddField(
            model_name='post',
            name='foto_video',
            field=models.FileField(null=True, upload_to='posts'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='username',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
    ]
