import os
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from jobs.models import Job

from .models import Application



@require_http_methods(["POST"])
@csrf_protect
def apply_job_view(request, job_id):

    # =========================
    # AUTHENTICATION
    # =========================

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "message": "Authentication required"
            },
            status=401
        )

    # =========================
    # ROLE CHECK
    # =========================

    if request.user.role != "candidate":
        return JsonResponse(
            {
                "success": False,
                "message": "Only candidates can apply for jobs"
            },
            status=403
        )

    # =========================
    # FIND JOB
    # =========================

    try:
        job = Job.objects.get(id=job_id)

    except Job.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "Job not found"
            },
            status=404
        )

    # =========================
    # CHECK JOB STATUS
    # =========================

    if job.status != Job.Status.OPEN:
        return JsonResponse(
            {
                "success": False,
                "message": "This job is no longer accepting applications"
            },
            status=400
        )

    # =========================
    # DUPLICATE APPLICATION
    # =========================

    if Application.objects.filter(
        job=job,
        candidate=request.user
    ).exists():

        return JsonResponse(
            {
                "success": False,
                "message": "You have already applied for this job"
            },
            status=400
        )

    # =========================
    # RESUME VALIDATION
    # =========================

    resume = request.FILES.get("resume")

    if not resume:
        return JsonResponse(
            {
                "success": False,
                "message": "Resume is required"
            },
            status=400
        )

    # =========================
    # FILE TYPE VALIDATION
    # =========================

    allowed_extensions = [
        ".pdf",
        ".doc",
        ".docx"
    ]

    extension = os.path.splitext(
        resume.name
    )[1].lower()

    if extension not in allowed_extensions:
        return JsonResponse(
            {
                "success": False,
                "message": "Only PDF, DOC and DOCX files are allowed"
            },
            status=400
        )

    # =========================
    # FILE SIZE VALIDATION
    # =========================

    max_size = 5 * 1024 * 1024

    if resume.size > max_size:
        return JsonResponse(
            {
                "success": False,
                "message": "Resume must be smaller than 5 MB"
            },
            status=400
        )

    # =========================
    # COVER LETTER
    # =========================

    cover_letter = request.POST.get(
        "cover_letter",
        ""
    ).strip()

    # =========================
    # CREATE APPLICATION
    # =========================

    application = Application.objects.create(
        job=job,
        candidate=request.user,
        resume_snapshot=resume,
        cover_letter=cover_letter
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Application submitted successfully",
            "application": {
                "id": application.id,
                "job_id": job.id,
                "job_title": job.title,
                "candidate": request.user.username,
                "status": application.status,
                "cover_letter": application.cover_letter,
                "applied_at": application.applied_at
            }
        },
        status=201
    )

@require_http_methods(["GET"])
def my_applications_view(request):

    # =========================
    # AUTHENTICATION
    # =========================

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "message": "Authentication required"
            },
            status=401
        )

    # =========================
    # ROLE CHECK
    # =========================

    if request.user.role != "candidate":
        return JsonResponse(
            {
                "success": False,
                "message": "Only candidates can view their applications"
            },
            status=403
        )

    # =========================
    # GET APPLICATIONS
    # =========================

    applications = Application.objects.filter(
        candidate=request.user
    ).select_related(
        "job"
    ).order_by(
        "-applied_at"
    )

    # =========================
    # RESPONSE
    # =========================

    application_data = []

    for application in applications:

        application_data.append(
            {
                "id": application.id,
                "job_id": application.job.id,
                "job_title": application.job.title,
                "location": application.job.location,
                "job_type": application.job.job_type,
                "status": application.status,
                "cover_letter": application.cover_letter,
                "resume": application.resume_snapshot.url
                if application.resume_snapshot
                else None,
                "applied_at": application.applied_at,
            }
        )

    return JsonResponse(
        {
            "success": True,
            "count": len(application_data),
            "applications": application_data
        },
        status=200
    )

@require_http_methods(["GET"])
def job_applicants_view(request, job_id):

    # Authentication check
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "message": "Authentication required"
            },
            status=401
        )

    # Recruiter check
    if request.user.role != "recruiter":
        return JsonResponse(
            {
                "success": False,
                "message": "Only recruiters can view applicants"
            },
            status=403
        )

    # Find job
    try:
        job = Job.objects.get(id=job_id)

    except Job.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "Job not found"
            },
            status=404
        )

    # Check job ownership
    if job.posted_by != request.user:
        return JsonResponse(
            {
                "success": False,
                "message": "You can only view applicants for your own jobs"
            },
            status=403
        )

    # Get applications
    applications = Application.objects.filter(
        job=job
    ).select_related(
        "candidate"
    ).order_by(
        "-applied_at"
    )

    # Prepare response
    applicant_data = []

    for application in applications:

        applicant_data.append(
            {
                "application_id": application.id,

                "candidate": {
                    "id": application.candidate.id,
                    "username": application.candidate.username,
                    "email": application.candidate.email,
                },

                "job_title": application.job.title,

                "status": application.status,

                "cover_letter": application.cover_letter,

                "resume": (
                    application.resume_snapshot.url
                    if application.resume_snapshot
                    else None
                ),

                "applied_at": application.applied_at,
            }
        )

    return JsonResponse(
        {
            "success": True,
            "count": len(applicant_data),
            "applicants": applicant_data
        },
        status=200
    )

@require_http_methods(["PATCH"])
def update_application_status_view(request, application_id):

    # Check login
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "message": "Authentication required"
            },
            status=401
        )

    # Only recruiter
    if request.user.role != "recruiter":
        return JsonResponse(
            {
                "success": False,
                "message": "Only recruiters can update application status"
            },
            status=403
        )

    # Find application
    try:
        application = Application.objects.select_related(
            "job",
            "candidate"
        ).get(id=application_id)

    except Application.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "Application not found"
            },
            status=404
        )

    # Recruiter can update only applications
    # belonging to their own job
    if application.job.posted_by != request.user:
        return JsonResponse(
            {
                "success": False,
                "message": "You can only update applications for your own jobs"
            },
            status=403
        )

    # Read JSON body
    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid JSON"
            },
            status=400
        )

    new_status = data.get("status")

    # Allowed statuses
    allowed_statuses = [
        "applied",
        "shortlisted",
        "rejected",
        "hired"
    ]

    if new_status not in allowed_statuses:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid application status"
            },
            status=400
        )

    # Update status
    application.status = new_status
    application.save()

    return JsonResponse(
        {
            "success": True,
            "message": "Application status updated successfully",
            "application": {
                "id": application.id,
                "candidate": application.candidate.username,
                "job_title": application.job.title,
                "status": application.status
            }
        },
        status=200
    )