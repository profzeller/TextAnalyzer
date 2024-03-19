from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage at the root URL
    path('login/', auth_views.LoginView.as_view(template_name='submission/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('submit/', views.submit_text, name='submit_text'),  # URL for submitting text
    path('submission/<int:pk>/', views.submission_detail, name='submission_detail'),
    # ... you can add more URL patterns here if needed ...
]
