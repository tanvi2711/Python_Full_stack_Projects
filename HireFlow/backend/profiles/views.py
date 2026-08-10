import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "PUT"])
@csrf_protect
def profile_view(request):

    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "message": "Authentication required"
            },
            status=401
        )

    user = request.user

    # =========================
    # GET PROFILE
    # =========================

    if request.method == "GET":

        if user.role == "candidate":

            profile = user.candidate_profile

            return JsonResponse({
                "success": True,
                "profile": {
                    "id": profile.id,
                    "full_name": profile.full_name,
                    "location": profile.location,
                    "education": profile.education,
                    "experience_years": profile.experience_years,
                    "bio": profile.bio
                }
            })

        if user.role == "recruiter":

            profile = user.recruiter_profile

            return JsonResponse({
                "success": True,
                "profile": {
                    "id": profile.id,
                    "company_name": profile.company_name,
                    "company_website": profile.company_website,
                    "designation": profile.designation,
                    "company_description": profile.company_description
                }
            })

    # =========================
    # UPDATE PROFILE
    # =========================

    if request.method == "PUT":

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

        if user.role == "candidate":

            profile = user.candidate_profile

            profile.full_name = data.get(
                "full_name",
                profile.full_name
            )

            profile.location = data.get(
                "location",
                profile.location
            )

            profile.education = data.get(
                "education",
                profile.education
            )

            profile.experience_years = data.get(
                "experience_years",
                profile.experience_years
            )

            profile.bio = data.get(
                "bio",
                profile.bio
            )

            profile.save()

            return JsonResponse({
                "success": True,
                "message": "Candidate profile updated successfully"
            })

        if user.role == "recruiter":

            profile = user.recruiter_profile

            profile.company_name = data.get(
                "company_name",
                profile.company_name
            )

            profile.company_website = data.get(
                "company_website",
                profile.company_website
            )

            profile.designation = data.get(
                "designation",
                profile.designation
            )

            profile.company_description = data.get(
                "company_description",
                profile.company_description
            )

            profile.save()

            return JsonResponse({
                "success": True,
                "message": "Recruiter profile updated successfully"
            })

    return JsonResponse(
        {
            "success": False,
            "message": "Invalid request"
        },
        status=400
    )