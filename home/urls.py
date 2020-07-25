from django.urls import path
from .views import (home, about,
                    PostListView,
                    PostCreateView,
                    PostDetailView,
                    PostUpdateView,
                    PostDeleteView)
from django.contrib.auth import views as auth_views
from users import views
app_name = 'home'
urlpatterns = [
    #home/home
    path('home/', PostListView.as_view(), name = 'home' ),
    path('post/<int:pk>', PostDetailView.as_view(), name = 'detail' ),
    path('post/', PostCreateView.as_view(), name = 'create' ),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'update' ),

    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'delete' ),

    path('about/', about, name = 'about'),
    path('register/', views.register, name = 'register'),

    path('profile/', views.profile, name = 'profile'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = 'logout'),

    ]