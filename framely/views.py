from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .models import Usuario, Post
from .forms import UsuarioForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import zip_longest
# Create your views here.

class UsuarioListado(ListView):
    model = Usuario


class UsuarioDetalle(DetailView):
    model = Usuario

class UsuarioCrear(CreateView):
    model = Usuario
    form_class = UsuarioForm
    success_message = 'Usuario Creado Correctamente!' 
        

    #Verificamos el formulario
    def form_valid(self, form):
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user= authenticate(username=username, password=password)
            cel = form.cleaned_data.get('cel')
            fecha_nacimiento = form.cleaned_data.get('fecha_nacimiento')
            email = form.cleaned_data.get('email')
            foto_perfil = "icono/userpost.png"
            #Creamos el usuario en la base de datos
            usuarioBD = Usuario.objects.create(cel=cel, username= username, email=email, fecha_nacimiento=fecha_nacimiento, user=user, foto_perfil=foto_perfil)
            usuarioBD.save()
            login(self.request, user)
            return redirect('listaUsuarios')

class UsuarioActualizar(UpdateView):
    model = Usuario
    form = Usuario
    fields = ['username', 'email', 'cel', 'foto_perfil']
    success_message = 'Usuario Actualizado Correctamente!'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        cel = form.cleaned_data.get('cel')
        foto_perfil = form.cleaned_data.get('foto_perfil')
        if foto_perfil == False:
            foto_perfil = "icono/userpost.png"
        usuario = Usuario.objects.get(id=self.kwargs['pk'])
        usuario.username = username
        usuario.email = email
        usuario.cel = cel
        usuario.foto_perfil = foto_perfil
        usuario.save()
        user = User.objects.get(id=usuario.user.id)
        user.username = username
        user.email = email
        user.save()
        login(self.request, user)
        return redirect('listaUsuarios')


class PostListado(ListView):
    model = Post

class PostDetalle(DetailView):
    model = Post

class PostCrear(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['foto_video', 'descripcion'] 
    success_message = 'Post Creado Correctamente!'

    def form_valid(self, form):
        form.instance.usuario.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('listaUsuarios')
    
class PostActualizar(UpdateView):
    model = Post
    form = Post
    fields = ['foto_video', 'descripcion']
    success_message = 'Post Actualizado Correctamente!' 
        

    def get_success_url(self):        
        return reverse('listaUsuarios')

@login_required
def PostEliminar(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('listaUsuarios')

#Función para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def vistaUsuarios(request):
    usuarios = Usuario.objects.all().exclude(user=request.user)
    usuarioLogueado = Usuario.objects.get(user = request.user)
    siguiendo = usuarioLogueado.following.all()
    posts = Post.objects.all()
    likes = [p.likes.count() for p in posts]
    likesUsuario = Post.objects.filter(likes=request.user)
    posteador = [p.usuario.first() for p in posts]
    usuarioPosteador = []
    for p in posteador:
        usuario = Usuario.objects.get(user=p)
        usuarioPosteador.append(usuario)
    zipped_data = zip_longest(posts, likes, usuarioPosteador)
    return render(request, 'usuario/usuarios.html', {'usuarios': usuarios, 'usuarioLogueado': usuarioLogueado, 'siguiendo': siguiendo, 'zipped_data':zipped_data, 'likesUsuario':likesUsuario})

@login_required
def perfil(request, pk):
    usuarioLogueado = User.objects.get(pk=request.user.pk)
    user = User.objects.get(pk=pk)
    if user == usuarioLogueado:
        editar = True
    else:
        editar = False
    print(editar)
    usuario = Usuario.objects.get(user=user)
    seguidores = usuario.followers.count()
    seguidos = usuario.following.count()
    cantidadPosts = Post.objects.filter(usuario=user).count()
    posts = Post.objects.filter(usuario=user)
    likes = [p.likes.count() for p in posts]
    zipped_data = zip_longest(posts, likes)
    return render(request, 'usuario/perfil.html', {'user':usuario, 'seguidores': seguidores, 'seguidos': seguidos, 'cantidadPosts': cantidadPosts, 'zipped_data':zipped_data, 'editar':editar})
        

@login_required
def seguir(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    usuario.followers.add(request.user)
    usuarioSiguiendo = Usuario.objects.get(user = request.user)
    usuarioSiguiendo.following.add(usuario.user)
    usuario.save()
    usuarioSiguiendo.save()
    return redirect('listaUsuarios')

@login_required
def unfollow(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    usuario.followers.remove(request.user)
    
    usuarioSiguiendo = Usuario.objects.get(user=request.user)
    usuarioSiguiendo.following.remove(usuario.user)
    
    usuario.save()
    usuarioSiguiendo.save()
    return redirect('listaUsuarios')

@login_required
def like(request, pk):
    usuario = Usuario.objects.get(user=request.user)
    post = Post.objects.get(pk=pk)
    post.likes.add(usuario.user)
    post.save()
    return redirect('listaUsuarios')

@login_required
def unlike(request, pk):
    usuario = Usuario.objects.get(user=request.user)
    post = Post.objects.get(pk=pk)
    post.likes.remove(usuario.user)
    post.save()
    return redirect('listaUsuarios')

@login_required
def eliminarPerfil(request, pk):
    usuarioLogueado = Usuario.objects.get(user=request.user)
    user = User.objects.get(pk=usuarioLogueado.user.pk)
    usuario = Usuario.objects.get(pk=pk)
    posts = Post.objects.filter(usuario=user)
    if usuarioLogueado == usuario:
        usuario.delete()
        user.delete()
    for post in posts:
        post.delete()    
    return redirect('login')

@login_required
def buscarUsuariosyPosts(request):
    if request.method == 'POST':
        usuarioLogueado = Usuario.objects.get(user = request.user)
        siguiendo = usuarioLogueado.following.all()
        buscar = request.POST['buscar']
        usuarios = Usuario.objects.filter(username__icontains=buscar)
        posts = Post.objects.filter(descripcion__icontains=buscar)
        if posts.count() == 0:
            vacio = True
        else:
            vacio = False
        likes = [p.likes.count() for p in posts]
        likesUsuario = Post.objects.filter(likes=request.user)
        posteador = [p.usuario.first() for p in posts]
        usuarioPosteador = []
        for p in posteador:
            usuario = Usuario.objects.get(user=p)
            usuarioPosteador.append(usuario)
        zipped_data = zip_longest(posts, likes, usuarioPosteador)
        return render(request, 'principal/resultadoBusqueda.html', {'usuarios': usuarios, 'zipped_data': zipped_data, 'siguiendo': siguiendo, 'likesUsuario':likesUsuario, 'usuarioLogueado':usuarioLogueado, 'vacio':vacio})

@login_required
def likesUsuario(request, pk):
    usuarios = []
    usuarioLogueado = Usuario.objects.get(user = request.user)
    post = Post.objects.get(pk=pk)
    posteador = post.usuario.first()
    posteador = Usuario.objects.get(user=posteador)
    likes = post.likes.count()  
    usuariosLikes = post.likes.all()
    siguiendo = usuarioLogueado.following.all()
    for usuario in usuariosLikes:
        usuario = Usuario.objects.get(user=usuario)
        usuarios.append(usuario)
    return render(request, 'post/likes.html', {'post':post, 'posteador':posteador, 'usuarios':usuarios, 'likes':likes, 'usuarioLogueado':usuarioLogueado, 'siguiendo':siguiendo})