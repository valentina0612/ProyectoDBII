from djongo import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    foto_perfil = models.ImageField('foto_perfil', upload_to='usuario', null=True, blank=True)
    cel = models.CharField(max_length=15)
    fecha_nacimiento = models.DateField()
    followers = models.ArrayReferenceField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        related_name='seguidores'
    )
    following = models.ArrayReferenceField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        related_name='siguiendo'
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    usuario = models.ArrayReferenceField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        related_name='posts'
    )
    foto_video = models.FileField('foto_video', upload_to='posts', null=True, blank=True)
    descripcion = models.TextField(max_length=500)
    likes = models.ArrayReferenceField(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        related_name='me_gusta'
    )
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.descripcion
