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
            #Creamos el usuario en la base de datos
            usuarioBD = Usuario.objects.create(cel=cel, username= username, email=email, fecha_nacimiento=fecha_nacimiento, user=user)
            usuarioBD.save()
            login(self.request, user)
            return redirect('listaUsuarios')

class UsuarioActualizar(UpdateView):
    model = Usuario
    form = Usuario
    fields = ['username', 'email', 'cel', 'foto_perfil']
    success_message = 'Usuario Actualizado Correctamente!' 

    def get_success_url(self):        
        return reverse('listaUsuarios')

class UsuarioEliminar(DeleteView):
    model = Usuario
    form = Usuario
    fields = "__all__" 
    success_message = 'Usuario Eliminado Correctamente!' 
        

    def get_success_url(self):        
        return reverse('listaUsuarios')

class PostListado(ListView):
    model = Post

class PostDetalle(DetailView):
    model = Post

class PostCrear(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['foto_video', 'descripcion']  # Define los campos que el usuario ingresará

    success_message = 'Post Creado Correctamente!'

    def form_valid(self, form):
        form.instance.usuario.add(self.request.user)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('listaPosts')

    def get_success_url(self):
        return reverse('listaPosts')
    
class PostActualizar(UpdateView):
    model = Post
    form = Post
    fields = "__all__" 
    success_message = 'Post Actualizado Correctamente!' 
        

    def get_success_url(self):        
        return reverse('listaPosts')

class PostEliminar(DeleteView):
    model = Post
    form = Post
    fields = "__all__" 
    success_message = 'Post Eliminado Correctamente!' 
        

    def get_success_url(self):        
        return reverse('listaPosts')

#Función para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def vistaUsuarios(request):
    usuarios = Usuario.objects.all().exclude(user=request.user)
    usuarioLogueado = Usuario.objects.get(user = request.user)
    siguiendo = usuarioLogueado.following.all()
    return render(request, 'usuario/usuarios.html', {'usuarios': usuarios, 'usuarioLogueado': usuarioLogueado, 'siguiendo': siguiendo})


def seguir(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    usuario.followers.add(request.user)
    usuarioSiguiendo = Usuario.objects.get(user = request.user)
    usuarioSiguiendo.following.add(usuario.user)
    usuario.save()
    usuarioSiguiendo.save()
    return render(request, 'usuario/usuarios.html')

def unfollow(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    usuario.followers.remove(request.user)
    
    usuarioSiguiendo = Usuario.objects.get(user=request.user)
    usuarioSiguiendo.following.remove(usuario.user)
    
    usuario.save()
    usuarioSiguiendo.save()
    return render(request, 'usuario/usuarios.html')

def buscarUsuarios(request):
    if request.method == 'POST':
        buscar = request.POST['buscar']
        usuarios = Usuario.objects.filter(user__username__contains=buscar)
        return render(request, 'usuario/usuarios.html', {'usuario': usuarios})
    else:
        return render(request, 'usuario/usuarios.html', {})

def like(request, pk):
    usuario = Usuario.objects.get(user=request.user)
    post = Post.objects.get(pk=pk)
    post.likes.add(usuario.user)
    post.save()
    return render(request, 'post/posts.html')

def unlike(request, pk):
    usuario = Usuario.objects.get(user=request.user)
    post = Post.objects.get(pk=pk)
    post.likes.remove(usuario.user)
    post.save()
    return render(request, 'post/posts.html')