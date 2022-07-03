from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('validate', views.validate, name = 'validate'),
    path('registered', views.registered, name= 'registered'),
]