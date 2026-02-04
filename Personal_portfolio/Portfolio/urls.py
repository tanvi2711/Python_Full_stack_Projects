from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('certifications/', views.certifications, name='certifications'),
    path('education/', views.education, name='education'),
]