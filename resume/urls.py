from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_resume, name="create_resume"),
    path("preview/<int:resume_id>/", views.resume_preview, name="resume_preview"),
]