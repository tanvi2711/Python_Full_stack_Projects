from django.urls import path

from . import views


urlpatterns = [
    path(
        'skills/',
        views.skills_view,
        name='skills'
    ),

    path(
        'jobs/',
        views.create_job_view,
        name='create-job'
    ),

    path(
        'recruiter/jobs/',
        views.recruiter_jobs_view,
        name='recruiter-jobs'
    ),

    path(
        'recruiter/dashboard/',
        views.recruiter_dashboard_view,
        name='recruiter-dashboard'
    ),

    path(
        'jobs/list/',
        views.jobs_list_view,
        name='jobs-list'
    ),

    path(
        'jobs/<int:job_id>/',
        views.job_detail_view,
        name='job-detail'
    ),
]