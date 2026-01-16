from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    summary = models.TextField()

    skills = models.TextField(
        help_text="Comma separated skills"
    )

    experience = models.TextField()
    education = models.TextField()
    projects = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.username} Resume"