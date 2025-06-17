from django.urls import path
from . import views

urlpatterns = [
    path('', views.application_form, name='application_form'),
    path('view_form/', views.view_form, name='view_form'),
]