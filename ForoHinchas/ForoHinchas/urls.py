"""ForoHinchas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from foro.views import HomeView, DetailView, CreateView, DeleteJornadaView, search, CreateComment, ResultadoComment
from users.views import LoginView, LogoutView, RegistrationView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #Jornada URLs
    url(r'^$', HomeView.as_view(), name='index'),
    url(r'^jornada_(?P<pk>[0-9]+)$', DetailView.as_view(), name='jornada_detail'),
    url(r'^jornada_new$', CreateView.as_view(), name='add_jornada'),
    url(r'^jornada_(?P<pk>[0-9]+)_delete$', login_required(DeleteJornadaView.as_view()), name='delete_jornada'),
    url(r'^search/$', search, name='search'),


    # Posts URLs
    url(r'^jornada_(?P<pk>[0-9]+)/comment_new$', login_required(CreateComment.as_view()), name='new_post'),
    url(r'^jornada_(?P<pk>[0-9]+)/resultado_comment_new$', login_required(ResultadoComment.as_view()), name='post_bsp'),


    # Users URLs
    url(r'^login$', LoginView.as_view(), name='users_login'),
    url(r'^logout$', LogoutView.as_view(), name='users_logout'),
    url(r'^register$', RegistrationView.as_view(), name='users_register')



]
