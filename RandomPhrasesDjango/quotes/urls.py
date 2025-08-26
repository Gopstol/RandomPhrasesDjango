from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.random_quote_view, name='random_quote'),
    path('add/', views.add_quote_view, name='add_quote'),
    path('top/', views.top_quotes_view, name='top_quotes'),
    path("like/<int:pk>/", views.like_quote, name="like_quote"),
    path("dislike/<int:pk>/", views.dislike_quote, name="dislike_quote"),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
]