from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('sign_up', views.sign_up),
    url('login', views.login),
]