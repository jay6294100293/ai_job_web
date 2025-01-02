from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views.api_key_views import update_api_keys
from .views.dashboard_view import dashboard
from .views.register_view import register

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='./auth_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-api-keys/', update_api_keys, name='update_api_keys'),
    path('dashboard/', dashboard, name='dashboard'),
]
