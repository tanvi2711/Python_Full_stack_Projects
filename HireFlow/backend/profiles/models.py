from django.conf import settings
from django.db import models


class CandidateProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='candidate_profile'
    )

    full_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=200, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class RecruiterProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recruiter_profile'
    )

    company_name = models.CharField(max_length=150)
    company_website = models.URLField(blank=True)
    designation = models.CharField(max_length=100, blank=True)
    company_description = models.TextField(blank=True)

    def __str__(self):
        return self.company_name