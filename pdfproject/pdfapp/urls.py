from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_pdfs, name='home'),         # Home route
    path('display/', views.display_pdfs, name='display_pdfs'),  # Optional
]
