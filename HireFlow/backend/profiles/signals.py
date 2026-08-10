from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from .models import CandidateProfile, RecruiterProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.role == User.Role.CANDIDATE:
        CandidateProfile.objects.create(
            user=instance,
            full_name=instance.username
        )

    elif instance.role == User.Role.RECRUITER:
        RecruiterProfile.objects.create(
            user=instance,
            company_name=""
        )