from django.urls import path
from .views import home, about
from django.contrib.auth import views as auth_views
from users import views
app_name = 'home'
urlpatterns = [
    #coreyschafer/home
    path('home/', home, name = 'home' ),
    path('about/', about, name = 'about'),
    path('register/', views.register, name = 'register'),

    path('profile/', views.profile, name = 'profile'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = 'logout'),
    ]