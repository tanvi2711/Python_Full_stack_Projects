import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from .models import Job,Skill


@require_http_methods(["GET", "POST"])
@csrf_protect
def skills_view(request):

    # =========================
    # GET ALL SKILLS
    # =========================

    if request.method == "GET":

        skills = Skill.objects.all().order_by("name")

        skill_list = []

        for skill in skills:
            skill_list.append({
                "id": skill.id,
                "name": skill.name
            })

        return JsonResponse({
            "success": True,
            "skills": skill_list
        })

    # =========================
    # CREATE SKILL
    # =========================

    if request.method == "POST":

        # User must be logged in
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Authentication required"
                },
                status=401
            )

        # Only recruiter/admin can create skills
        if request.user.role not in ["recruiter", "admin"]:
            return JsonResponse(
                {
                    "success": False,
                    "message": "You do not have permission to create skills"
                },
                status=403
            )

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

        name = data.get("name", "").strip()

        if not name:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Skill name is required"
                },
                status=400
            )

        # Prevent duplicate skill
        if Skill.objects.filter(name__iexact=name).exists():
            return JsonResponse(
                {
                    "success": False,
                    "message": "Skill already exists"
                },
                status=400
            )

        skill = Skill.objects.create(name=name)

        return JsonResponse(
            {
                "success": True,
                "message": "Skill created successfully",
                "skill": {
                    "id": skill.id,
                    "name": skill.name
                }
            },
            status=201
        )

@require_http_methods(["POST"])
@csrf_protect
def create_job_view(request):

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

    if request.user.role != "recruiter":
        return JsonResponse(
            {
                "success": False,
                "message": "Only recruiters can create jobs"
            },
            status=403
        )

    # =========================
    # PARSE JSON
    # =========================

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

    # =========================
    # GET DATA
    # =========================

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    location = data.get("location", "").strip()
    job_type = data.get("job_type", "full-time")

    skills = data.get("skills", [])

    salary_min = data.get("salary_min")
    salary_max = data.get("salary_max")

    # =========================
    # REQUIRED FIELDS
    # =========================

    if not title:
        return JsonResponse(
            {
                "success": False,
                "message": "Job title is required"
            },
            status=400
        )

    if not description:
        return JsonResponse(
            {
                "success": False,
                "message": "Job description is required"
            },
            status=400
        )

    if not location:
        return JsonResponse(
            {
                "success": False,
                "message": "Location is required"
            },
            status=400
        )

    # =========================
    # VALIDATE JOB TYPE
    # =========================

    valid_job_types = [
        "full-time",
        "part-time",
        "internship",
        "remote"
    ]

    if job_type not in valid_job_types:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid job type"
            },
            status=400
        )

    # =========================
    # VALIDATE SKILLS
    # =========================

    if not isinstance(skills, list):
        return JsonResponse(
            {
                "success": False,
                "message": "Skills must be a list of skill IDs"
            },
            status=400
        )

    selected_skills = Skill.objects.filter(id__in=skills)

    if selected_skills.count() != len(set(skills)):
        return JsonResponse(
            {
                "success": False,
                "message": "One or more skills are invalid"
            },
            status=400
        )

    # =========================
    # CREATE JOB
    # =========================

    job = Job.objects.create(
        posted_by=request.user,
        title=title,
        description=description,
        location=location,
        job_type=job_type,
        salary_min=salary_min,
        salary_max=salary_max
    )

    # =========================
    # ADD SKILLS
    # =========================

    job.skills.set(selected_skills)

    return JsonResponse(
        {
            "success": True,
            "message": "Job created successfully",
            "job": {
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "location": job.location,
                "job_type": job.job_type,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "status": job.status,
                "skills": [
                    {
                        "id": skill.id,
                        "name": skill.name
                    }
                    for skill in selected_skills
                ],
                "posted_by": request.user.username
            }
        },
        status=201
    )

@require_http_methods(["GET"])
def jobs_list_view(request):

    # Start with open jobs only
    jobs = Job.objects.filter(
        status=Job.Status.OPEN
    ).select_related(
        "posted_by"
    ).prefetch_related(
        "skills"
    ).order_by("-created_at")

    # =========================
    # SEARCH
    # =========================

    search = request.GET.get("search", "").strip()

    if search:
        jobs = jobs.filter(
            title__icontains=search
        )

    # =========================
    # LOCATION FILTER
    # =========================

    location = request.GET.get("location", "").strip()

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    # =========================
    # JOB TYPE FILTER
    # =========================

    job_type = request.GET.get("job_type", "").strip()

    if job_type:
        valid_job_types = [
            choice[0]
            for choice in Job.JobType.choices
        ]

        if job_type not in valid_job_types:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Invalid job type"
                },
                status=400
            )

        jobs = jobs.filter(
            job_type=job_type
        )

    # =========================
    # SKILL FILTER
    # =========================

    skill = request.GET.get("skill", "").strip()

    if skill:
        jobs = jobs.filter(
            skills__name__iexact=skill
        )

    # =========================
    # SALARY FILTER
    # =========================

    salary_min = request.GET.get("salary_min", "").strip()

    if salary_min:
        try:
            salary_min = float(salary_min)
        except ValueError:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Invalid salary_min value"
                },
                status=400
            )

        jobs = jobs.filter(
            salary_min__gte=salary_min
        )

    # =========================
    # PAGINATION
    # =========================

    try:
        page = int(request.GET.get("page", 1))
    except ValueError:
        page = 1

    try:
        page_size = int(
            request.GET.get("page_size", 10)
        )
    except ValueError:
        page_size = 10

    # Keep pagination reasonable
    page_size = min(page_size, 50)

    if page < 1:
        page = 1

    total_jobs = jobs.count()

    start = (page - 1) * page_size
    end = start + page_size

    jobs_page = jobs[start:end]

    job_list = []

    for job in jobs_page:

        job_list.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "job_type": job.job_type,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "status": job.status,
            "created_at": job.created_at,
            "posted_by": job.posted_by.username,
            "skills": [
                {
                    "id": skill.id,
                    "name": skill.name
                }
                for skill in job.skills.all()
            ]
        })

    return JsonResponse({
        "success": True,
        "count": total_jobs,
        "page": page,
        "page_size": page_size,
        "jobs": job_list
    })

@require_http_methods(["GET", "PUT", "DELETE"])
@csrf_protect
def job_detail_view(request, job_id):

    # =========================
    # FIND JOB
    # =========================

    try:
        job = Job.objects.select_related(
            "posted_by"
        ).prefetch_related(
            "skills"
        ).get(id=job_id)

    except Job.DoesNotExist:
        return JsonResponse(
            {
                "success": False,
                "message": "Job not found"
            },
            status=404
        )

    # =========================
    # GET JOB
    # =========================

    if request.method == "GET":

        return JsonResponse({
            "success": True,
            "job": {
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "location": job.location,
                "job_type": job.job_type,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "status": job.status,
                "created_at": job.created_at,
                "updated_at": job.updated_at,
                "posted_by": job.posted_by.username,
                "skills": [
                    {
                        "id": skill.id,
                        "name": skill.name
                    }
                    for skill in job.skills.all()
                ]
            }
        })

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

    if request.user.role != "recruiter":
        return JsonResponse(
            {
                "success": False,
                "message": "Only recruiters can modify jobs"
            },
            status=403
        )

    # =========================
    # OWNERSHIP CHECK
    # =========================

    if job.posted_by_id != request.user.id:
        return JsonResponse(
            {
                "success": False,
                "message": "You can only modify your own jobs"
            },
            status=403
        )

    # =========================
    # DELETE
    # =========================

    if request.method == "DELETE":

        job.delete()

        return JsonResponse({
            "success": True,
            "message": "Job deleted successfully"
        })

    # =========================
    # UPDATE
    # =========================

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

    title = data.get(
        "title",
        job.title
    ).strip()

    description = data.get(
        "description",
        job.description
    ).strip()

    location = data.get(
        "location",
        job.location
    ).strip()

    job_type = data.get(
        "job_type",
        job.job_type
    )

    skills = data.get(
        "skills",
        None
    )

    salary_min = data.get(
        "salary_min",
        job.salary_min
    )

    salary_max = data.get(
        "salary_max",
        job.salary_max
    )

    # =========================
    # VALIDATION
    # =========================

    if not title:
        return JsonResponse(
            {
                "success": False,
                "message": "Job title is required"
            },
            status=400
        )

    if not description:
        return JsonResponse(
            {
                "success": False,
                "message": "Job description is required"
            },
            status=400
        )

    if not location:
        return JsonResponse(
            {
                "success": False,
                "message": "Location is required"
            },
            status=400
        )

    valid_job_types = [
        choice[0]
        for choice in Job.JobType.choices
    ]

    if job_type not in valid_job_types:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid job type"
            },
            status=400
        )

    # =========================
    # VALIDATE STATUS (OPTIONAL)
    # =========================

    status = data.get("status", job.status)

    valid_statuses = [
        choice[0]
        for choice in Job.Status.choices
    ]

    if status not in valid_statuses:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid job status"
            },
            status=400
        )

    # =========================
    # UPDATE JOB
    # =========================

    job.title = title
    job.description = description
    job.location = location
    job.job_type = job_type
    job.salary_min = salary_min
    job.salary_max = salary_max
    job.status = status

    job.save()

    # =========================
    # UPDATE SKILLS
    # =========================

    if skills is not None:

        if not isinstance(skills, list):
            return JsonResponse(
                {
                    "success": False,
                    "message": "Skills must be a list"
                },
                status=400
            )

        selected_skills = Skill.objects.filter(
            id__in=skills
        )

        if selected_skills.count() != len(set(skills)):
            return JsonResponse(
                {
                    "success": False,
                    "message": "One or more skills are invalid"
                },
                status=400
            )

        job.skills.set(selected_skills)

    return JsonResponse({
        "success": True,
        "message": "Job updated successfully"
    })

@require_http_methods(["GET"])
def recruiter_jobs_view(request):
    """Return every job owned by the authenticated recruiter."""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Authentication required"}, status=401)

    if request.user.role != "recruiter":
        return JsonResponse({"success": False, "message": "Only recruiters can access their jobs"}, status=403)

    jobs = (
        Job.objects.filter(posted_by=request.user)
        .prefetch_related("skills")
        .order_by("-created_at")
    )

    job_data = []
    for job in jobs:
        job_data.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "job_type": job.job_type,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "status": job.status,
            "created_at": job.created_at,
            "updated_at": job.updated_at,
            "applicant_count": job.applications.count(),
            "skills": [
                {"id": skill.id, "name": skill.name}
                for skill in job.skills.all()
            ],
        })

    return JsonResponse({
        "success": True,
        "count": len(job_data),
        "jobs": job_data,
    })


@require_http_methods(["GET"])
def recruiter_dashboard_view(request):
    """Return recruiter dashboard KPIs and recent jobs."""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Authentication required"}, status=401)

    if request.user.role != "recruiter":
        return JsonResponse({"success": False, "message": "Only recruiters can access this dashboard"}, status=403)

    from applications.models import Application

    jobs = Job.objects.filter(posted_by=request.user)
    applications = Application.objects.filter(job__posted_by=request.user)

    recent_jobs = (
        jobs.prefetch_related("skills")
        .order_by("-created_at")[:5]
    )

    recent_job_data = []
    for job in recent_jobs:
        recent_job_data.append({
            "id": job.id,
            "title": job.title,
            "location": job.location,
            "job_type": job.job_type,
            "status": job.status,
            "created_at": job.created_at,
            "applicant_count": job.applications.count(),
        })

    return JsonResponse({
        "success": True,
        "stats": {
            "total_jobs": jobs.count(),
            "open_jobs": jobs.filter(status=Job.Status.OPEN).count(),
            "closed_jobs": jobs.filter(status=Job.Status.CLOSED).count(),
            "total_applications": applications.count(),
            "shortlisted": applications.filter(status=Application.Status.SHORTLISTED).count(),
            "hired": applications.filter(status=Application.Status.HIRED).count(),
        },
        "recent_jobs": recent_job_data,
    })
