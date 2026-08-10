from django.urls import path
from . import views


urlpatterns = [

    path(
        'jobs/<int:job_id>/apply/',
        views.apply_job_view,
        name='apply-job'
    ),

    path(
        'applications/mine/',
        views.my_applications_view,
        name='my-applications'
    ),

    path(
        'jobs/<int:job_id>/applicants/',
        views.job_applicants_view,
        name='job-applicants'
    ),

    path(
        'applications/<int:application_id>/status/',
        views.update_application_status_view,
        name='update-application-status'
    ),

]