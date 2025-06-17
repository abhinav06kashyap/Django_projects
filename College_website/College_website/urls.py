"""
URL configuration for College_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Application_Form import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('change_password/', views.change_password, name='change_password'),
    path('login_page/', views.login_page, name='login_page'),
    path('signup/', views.signup, name='signup'),
    # path('home_page/', views.home_page, name='home_page'),
    path('new_user/', views.new_user, name='new_user'),
    path('exist_user/', views.exist_user, name='exist_user'),
    path('view_exist_form/', views.view_exist_form, name='view_exist_form'),
    path('change_password/', views.change_password, name='change_password'),
    path('edit_form/', views.edit_form, name='edit_form'),
    path('admin/', admin.site.urls),
    path('Application_Form/', include('Application_Form.urls'))
]