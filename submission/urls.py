from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage at the root URL
    path('submit/', views.submit_text, name='submit_text'),  # URL for submitting text
    path('submission/<int:pk>/', views.submission_detail, name='submission_detail'),
    # ... you can add more URL patterns here if needed ...
]
