# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from django.views.generic import View, ListView
from django.shortcuts import render, redirect, render_to_response

from foro.forms import JornadaForm, PostForm
from foro.models import Jornada, Post
from foro.scraping import get_index
from users.models import Profile, TEAMS


class HomeView(View):

    @method_decorator(login_required())
    def get(self, request):
        jornadas = Jornada.objects.all().order_by('-create_at')
        paginator = Paginator(jornadas, 5)

        page = request.GET.get('page')

        try:
            jornadas = paginator.page(page)
        except PageNotAnInteger:
            jornadas = paginator.page(1)
        except EmptyPage:
            jornadas = paginator.page(paginator.num_pages)

        context = {
            'jornadas_list': jornadas,
            'next_url': '/index',
            'username': request.user.username
        }
        return render(request, 'foro/index.html', context)


class DetailView(View):

    @method_decorator(login_required())
    def get(self, request, pk):
        post_form = PostForm()
        posible_jornada = Jornada.objects.all().filter(pk=pk)
        jornada = posible_jornada[0] if len(posible_jornada) == 1 else None
        if jornada is not None:
            posts = Post.objects.filter(jornada=jornada).order_by('-create_at')
            paginator = Paginator(posts, 7)

            page = request.GET.get('page')

            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            context = {
                'jornada': jornada,
                'posts': posts,
                'next_url': '/detail',
                'username': request.user.username,
                'post_form': post_form
            }
            return render(request, 'foro/detail.html', context)
        else:
            return HttpResponseNotFound('Ups!! Algo salió mal. Posiblemente no se encuentra la jornada')


class CreateView(View):

    @method_decorator(login_required())
    def get(self, request):
        form = JornadaForm()
        context = {
            'form': form,
            'success_message': ''
        }
        return render(request, 'foro/new_jornada.html', context)

    @method_decorator(login_required())
    def post(self, request):
        success_message = ''
        jornada_with_author = Jornada()
        jornada_with_author.author = request.user
        form = JornadaForm(request.POST, instance=jornada_with_author)
        if form.is_valid():
            new_jornada = form.save()  # Guarda el objeto y me lo devuelves
            form = JornadaForm()
            success_message = 'Guardado con éxito!'
            success_message += '<br/> <a href="{0}">'.format(reverse('jornada_detail', args=[new_jornada.pk]))
            success_message += 'Ver jornada'
            success_message += '</a>'
        context = {
            'form': form,
            'success_message': success_message
        }
        return render(request, 'foro/new_jornada.html', context)


class DeleteJornadaView(DeleteView):
    model = Jornada
    success_url = reverse_lazy('index')


@login_required
def search(request):
    query = request.GET.get('q')
    if query is not None and query != '' and request.is_ajax():
        jornadas = Jornada.objects.filter(Q(title__icontains=query))
        context = {
            'jornadas': jornadas
        }
        return render(request, 'foro/search.html', context)
    return render(request, 'foro/search.html')


class CreateComment(View):
    def get(self, request, pk):
        form = PostForm()
        context = {
            'form': form,
            'pk': pk
        }
        return render(request, 'foro/createComment.html', context)

    def post(self, request, pk):
        if request.method == "POST":
            jornada = Jornada.objects.filter(pk=pk)[0]
            posible_post = Post()
            posible_post.author = request.user
            posible_post.jornada = jornada
            form = PostForm(request.POST, instance=posible_post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('/jornada_'+pk)
            else:
                return DetailView()

        return redirect('/')


def buscarPorEquipo(equipo,jornada):
    resultados = get_index(jornada)

    for partido in resultados:
        if(partido[0] == equipo):
            return partido
        elif(partido[1] == equipo):
            return partido
        else:
            continue


class ResultadoComment(View):
    @csrf_exempt
    def get(self, request, pk):
        form = PostForm()
        context = {
            'form': form,
            'pk': pk
        }
        return render(request, 'foro/createCommentResultado.html', context)

    def post(self, request, pk):

        if request.method == "POST":
            user = request.user
            profile = Profile.objects.filter(user=user)[0]
            contenido_post = buscarPorEquipo(dict(TEAMS).get(profile.team), pk)
            jornada = Jornada.objects.filter(pk=pk)[0]
            posible_post = Post()
            posible_post.author = request.user
            posible_post.jornada = jornada
            print contenido_post
            form = PostForm(request.POST, instance=posible_post)
            if form.is_valid():
                post = form.save(commit=False)
                post.text = 'El resutlado de mi equipo es: \n'
                post.text += contenido_post[0] + ' '
                post.text += contenido_post[2] + ' '
                post.text += contenido_post[1]
                post.url = contenido_post[3]
                post.save()
                return redirect('/jornada_' + pk)
            else:
                return DetailView()
        return redirect('/')