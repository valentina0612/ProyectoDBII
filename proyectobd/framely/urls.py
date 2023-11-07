from django.views.generic import RedirectView
from django.views.static import serve
from django.urls import path, include
from django.urls import re_path
from framely import views
from framely.views import *
from django.conf import settings


urlpatterns = [
    path('', RedirectView.as_view(url='login/')),
    path('posts/', PostListado.as_view(template_name='post/posts.html'), name='listaPosts'),
    path('posts/crear', PostCrear.as_view(template_name='post/crearPost.html'), name='crearPost'),
    path('posts/editar/<int:pk>', PostActualizar.as_view(template_name= 'post/editarPost.html'), name='editarPost'),
    path('posts/eliminar/<int:pk>', PostEliminar.as_view(template_name= 'post/eliminarPost.html'), name='eliminarPost'),
    path('posts/like/<int:pk>', like, name='like'),
    path('posts/unlike/<int:pk>', unlike, name='unlike'),

    path('usuarios/', vistaUsuarios, name='listaUsuarios'),
    path('usuarios/<int:pk>', UsuarioDetalle.as_view(template_name= 'usuario/perfil.html'), name='detalleUsuario'),
    path('usuarios/crear', UsuarioCrear.as_view(template_name='login/registro.html'), name='crearUsuario'),
    path('usuarios/editar/<int:pk>', UsuarioActualizar.as_view(template_name= 'usuario/editarPerfil.html'), name='editarUsuario'),
    path('usuarios/eliminar/<int:pk>', UsuarioEliminar.as_view(template_name= 'usuario/eliminarPerfil.html'), name='eliminarUsuario'),
    path('usuarios/seguir/<int:pk>', seguir, name='seguir'),
    path('usuarios/unfollow/<int:pk>', unfollow, name='unfollow'),
    
    path('logout/', logout_view, name='logout'),
    path('login/', LoginView.as_view(template_name='login/login.html'), name='login'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root':settings.MEDIA_ROOT,
    })
    
]