import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie


User = get_user_model()


@require_POST
def register_view(request):

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

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    phone = data.get("phone", "").strip()
    role = data.get("role", "candidate")

    # Required fields
    if not username or not email or not password:
        return JsonResponse(
            {
                "success": False,
                "message": "Username, email and password are required"
            },
            status=400
        )

    # Validate role
    valid_roles = [
        User.Role.CANDIDATE,
        User.Role.RECRUITER,
    ]

    if role not in valid_roles:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid role"
            },
            status=400
        )

    # Check username
    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {
                "success": False,
                "message": "Username already exists"
            },
            status=400
        )

    # Check email
    if User.objects.filter(email=email).exists():
        return JsonResponse(
            {
                "success": False,
                "message": "Email already exists"
            },
            status=400
        )

    # Validate password
    try:
        validate_password(password)
    except ValidationError as error:
        return JsonResponse(
            {
                "success": False,
                "message": error.messages
            },
            status=400
        )

    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        phone=phone,
        role=role
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Registration successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        },
        status=201
    )

@ensure_csrf_cookie
@require_GET
def csrf_token_view(request):
    return JsonResponse({
        "success": True,
        "message": "CSRF cookie set"
    })

@require_POST
def login_view(request):

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

    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        return JsonResponse(
            {
                "success": False,
                "message": "Username and password are required"
            },
            status=400
        )

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is None:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid username or password"
            },
            status=401
        )

    login(request, user)

    return JsonResponse({
        "success": True,
        "message": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    })


@require_POST
def logout_view(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "message": "User is not logged in"
            },
            status=401
        )

    logout(request)

    return JsonResponse({
        "success": True,
        "message": "Logout successful"
    })


@require_GET
def me_view(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "success": False,
                "message": "Authentication required"
            },
            status=401
        )

    user = request.user

    return JsonResponse({
        "success": True,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "is_verified": user.is_verified
        }
    })