from django.urls import path
from .views import (about,
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
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('confirm-email/<str:user_id>/<str:token>/', views.ConfirmRegistrationView.as_view(), name='confirm_email'),

    path('createprofile/', views.ProfileCreateView.as_view(), name = 'createprofile'),
    path('updateprofile/<int:pk>', views.ProfileUpdateView.as_view(), name = 'updateprofile'),
    path('login/', auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = 'logout'),

    ]